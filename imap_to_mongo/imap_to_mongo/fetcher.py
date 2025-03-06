import imaplib2
import email
import email.policy
from email.header import decode_header
import threading
import time
import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Callable
import socket

from .db import MongoEmailStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImapFetcher:
    """
    A class to fetch emails from an IMAP server and store them in MongoDB.
    Supports streaming mode and resuming from last fetch.
    """
    
    def __init__(
        self,
        imap_host: str,
        imap_user: str,
        imap_password: str,
        mongo_uri: str,
        mongo_db: str,
        mongo_collection: str,
        imap_port: int = 993,
        mailbox: str = "INBOX",
        use_ssl: bool = True,
        idle_timeout: int = 1800,
        fetch_on_start: bool = True,
        callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        """
        Initialize the IMAP fetcher.
        
        Args:
            imap_host: IMAP server hostname
            imap_user: IMAP username
            imap_password: IMAP password
            mongo_uri: MongoDB connection URI
            mongo_db: MongoDB database name
            mongo_collection: MongoDB collection name
            imap_port: IMAP server port (default: 993)
            mailbox: Mailbox to fetch from (default: "INBOX")
            use_ssl: Whether to use SSL (default: True)
            idle_timeout: IDLE command timeout in seconds (default: 1800)
            fetch_on_start: Whether to fetch existing emails on start (default: True)
            callback: Optional callback function to call when new emails are fetched
        """
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.imap_user = imap_user
        self.imap_password = imap_password
        self.mailbox = mailbox
        self.use_ssl = use_ssl
        self.idle_timeout = idle_timeout
        self.fetch_on_start = fetch_on_start
        self.callback = callback
        
        # Initialize MongoDB storage
        self.storage = MongoEmailStorage(mongo_uri, mongo_db, mongo_collection)
        
        # Initialize IMAP connection
        self.imap = None
        self.idle_thread = None
        self.running = False
        self.last_uid = None
    
    def _connect_imap(self) -> None:
        """Establish connection to the IMAP server."""
        try:
            if self.use_ssl:
                self.imap = imaplib2.IMAP4_SSL(self.imap_host, self.imap_port)
            else:
                self.imap = imaplib2.IMAP4(self.imap_host, self.imap_port)
            
            self.imap.login(self.imap_user, self.imap_password)
            self.imap.select(self.mailbox)
            logger.info(f"Connected to IMAP server {self.imap_host}")
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            raise
    
    def _disconnect_imap(self) -> None:
        """Disconnect from the IMAP server."""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
                logger.info("Disconnected from IMAP server")
            except Exception as e:
                logger.error(f"Error disconnecting from IMAP server: {e}")
    
    def _get_last_uid(self) -> Optional[int]:
        """
        Get the last UID from MongoDB or from the IMAP server.
        
        Returns:
            The last UID or None if no emails are found
        """
        # Try to get the last UID from MongoDB
        last_uid = self.storage.get_latest_uid(self.mailbox)
        
        # If no UID in MongoDB, get the last UID from IMAP
        if last_uid is None:
            try:
                result, data = self.imap.uid('search', None, 'ALL')
                if result == 'OK' and data[0]:
                    uids = data[0].split()
                    if uids:
                        last_uid = int(uids[-1])
                        logger.info(f"Last UID from IMAP: {last_uid}")
            except Exception as e:
                logger.error(f"Error getting last UID from IMAP: {e}")
        else:
            logger.info(f"Last UID from MongoDB: {last_uid}")
        
        return last_uid
    
    def _parse_email(self, raw_email: bytes) -> Dict[str, Any]:
        """
        Parse raw email data into a structured dictionary.
        
        Args:
            raw_email: Raw email data in bytes
            
        Returns:
            Dictionary containing parsed email data
        """
        msg = email.message_from_bytes(raw_email, policy=email.policy.default)
        
        # Extract basic headers
        email_data = {
            "message_id": msg.get("Message-ID", ""),
            "subject": self._decode_header(msg.get("Subject", "")),
            "from": self._decode_header(msg.get("From", "")),
            "to": self._decode_header(msg.get("To", "")),
            "cc": self._decode_header(msg.get("Cc", "")),
            "date": self._parse_date(msg.get("Date", "")),
            "mailbox": self.mailbox,
            "headers": dict(msg.items()),
        }
        
        # Extract body parts
        body_parts = []
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                self._process_part(part, body_parts, attachments)
        else:
            self._process_part(msg, body_parts, attachments)
        
        email_data["body_parts"] = body_parts
        email_data["attachments"] = attachments
        
        return email_data
    
    def _process_part(self, part, body_parts: List[Dict[str, Any]], attachments: List[Dict[str, Any]]) -> None:
        """
        Process an email part and add it to the appropriate list.
        
        Args:
            part: Email part
            body_parts: List to add body parts to
            attachments: List to add attachments to
        """
        content_type = part.get_content_type()
        content_disposition = part.get_content_disposition()
        
        if content_disposition == "attachment":
            # Handle attachment
            filename = part.get_filename()
            if filename:
                filename = self._decode_header(filename)
                payload = part.get_payload(decode=True)
                if payload:
                    attachments.append({
                        "filename": filename,
                        "content_type": content_type,
                        "size": len(payload),
                        "content": payload,
                    })
        elif content_type.startswith("text/"):
            # Handle text parts
            try:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        text = payload.decode(charset, errors='replace')
                        body_parts.append({
                            "content_type": content_type,
                            "content": text,
                        })
                    except Exception as e:
                        logger.warning(f"Error decoding email part: {e}")
                        body_parts.append({
                            "content_type": content_type,
                            "content": payload.decode('utf-8', errors='replace'),
                        })
            except Exception as e:
                logger.warning(f"Error processing email part: {e}")
    
    def _decode_header(self, header: str) -> str:
        """
        Decode email header.
        
        Args:
            header: Email header string
            
        Returns:
            Decoded header string
        """
        if not header:
            return ""
        
        decoded_parts = []
        for part, encoding in decode_header(header):
            if isinstance(part, bytes):
                if encoding:
                    try:
                        decoded_parts.append(part.decode(encoding))
                    except Exception:
                        decoded_parts.append(part.decode('utf-8', errors='replace'))
                else:
                    decoded_parts.append(part.decode('utf-8', errors='replace'))
            else:
                decoded_parts.append(part)
        
        return " ".join(decoded_parts)
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse email date string to datetime.
        
        Args:
            date_str: Date string from email header
            
        Returns:
            Datetime object or None if parsing fails
        """
        if not date_str:
            return None
        
        try:
            # Try to parse with email.utils
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except Exception:
            # Fallback to current time if parsing fails
            logger.warning(f"Failed to parse date: {date_str}")
            return datetime.utcnow()
    
    def _fetch_email(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a single email by UID.
        
        Args:
            uid: Email UID
            
        Returns:
            Parsed email data or None if fetch fails
        """
        try:
            result, data = self.imap.uid('fetch', uid, '(RFC822)')
            if result == 'OK' and data and data[0]:
                # The actual email is the second element of the first tuple
                raw_email = data[0][1]
                email_data = self._parse_email(raw_email)
                email_data["uid"] = int(uid)
                return email_data
        except Exception as e:
            logger.error(f"Error fetching email with UID {uid}: {e}")
        
        return None
    
    def _fetch_new_emails(self) -> List[Dict[str, Any]]:
        """
        Fetch new emails since the last UID.
        
        Returns:
            List of parsed email data
        """
        new_emails = []
        
        try:
            # Get emails with UID greater than the last one
            search_criteria = f'UID {self.last_uid+1}:*' if self.last_uid else 'ALL'
            result, data = self.imap.uid('search', None, search_criteria)
            
            if result == 'OK' and data and data[0]:
                uids = data[0].split()
                logger.info(f"Found {len(uids)} new emails")
                
                for uid in uids:
                    uid_str = uid.decode('utf-8')
                    email_data = self._fetch_email(uid_str)
                    
                    if email_data:
                        # Store in MongoDB
                        doc_id = self.storage.insert_email(email_data)
                        logger.info(f"Stored email with UID {uid_str}, MongoDB ID: {doc_id}")
                        
                        # Update last UID
                        self.last_uid = int(uid_str)
                        
                        # Add to result list
                        new_emails.append(email_data)
                        
                        # Call callback if provided
                        if self.callback:
                            self.callback(email_data)
        except Exception as e:
            logger.error(f"Error fetching new emails: {e}")
        
        return new_emails
    
    def _idle_callback(self, args) -> None:
        """
        Callback for IDLE command.
        
        Args:
            args: Arguments from IDLE command
        """
        if not self.running:
            return
        
        if args[0] == 'EXISTS':
            logger.info("New email notification received")
            # Temporarily exit IDLE mode
            self.imap.idle_done()
            # Fetch new emails
            self._fetch_new_emails()
            # Resume IDLE mode
            self._start_idle()
    
    def _idle_loop(self) -> None:
        """Main loop for IDLE mode."""
        while self.running:
            try:
                # Start IDLE mode
                self._start_idle()
                
                # Sleep to allow other threads to run
                time.sleep(1)
            except (imaplib2.IMAP4.abort, socket.error) as e:
                logger.error(f"IMAP connection lost: {e}")
                if self.running:
                    logger.info("Reconnecting to IMAP server...")
                    self._disconnect_imap()
                    self._connect_imap()
            except Exception as e:
                logger.error(f"Error in IDLE loop: {e}")
                time.sleep(5)  # Wait before retrying
    
    def _start_idle(self) -> None:
        """Start IDLE mode."""
        try:
            # Start IDLE command
            self.imap.idle(callback=self._idle_callback, timeout=self.idle_timeout)
        except Exception as e:
            logger.error(f"Error starting IDLE mode: {e}")
            raise
    
    def start(self) -> None:
        """Start the email fetcher."""
        if self.running:
            logger.warning("Fetcher is already running")
            return
        
        try:
            # Connect to IMAP server
            self._connect_imap()
            
            # Get the last UID
            self.last_uid = self._get_last_uid()
            
            # Fetch existing emails if requested
            if self.fetch_on_start:
                logger.info("Fetching existing emails")
                self._fetch_new_emails()
            
            # Start IDLE thread
            self.running = True
            self.idle_thread = threading.Thread(target=self._idle_loop)
            self.idle_thread.daemon = True
            self.idle_thread.start()
            
            logger.info("Email fetcher started")
        except Exception as e:
            logger.error(f"Error starting email fetcher: {e}")
            self._disconnect_imap()
            raise
    
    def stop(self) -> None:
        """Stop the email fetcher."""
        if not self.running:
            logger.warning("Fetcher is not running")
            return
        
        logger.info("Stopping email fetcher")
        self.running = False
        
        # Stop IDLE mode
        if self.imap:
            try:
                self.imap.idle_done()
            except Exception:
                pass
        
        # Wait for IDLE thread to finish
        if self.idle_thread and self.idle_thread.is_alive():
            self.idle_thread.join(timeout=5)
        
        # Disconnect from IMAP server
        self._disconnect_imap()
        
        # Close MongoDB connection
        self.storage.close()
        
        logger.info("Email fetcher stopped")
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()