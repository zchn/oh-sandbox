#!/usr/bin/env python3
"""
Example script demonstrating how to use the imap_to_mongo package.
"""

import os
import sys
import time
import logging
import signal
from datetime import datetime

# Add parent directory to path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from imap_to_mongo import ImapFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def email_callback(email_data):
    """
    Callback function that gets called when a new email is fetched.
    
    Args:
        email_data: Dictionary containing email data
    """
    logger.info(f"New email received: {email_data['subject']} from {email_data['from']}")
    
    # You can perform additional processing here
    # For example, send notifications, trigger workflows, etc.


def main():
    """Main function to run the email fetcher."""
    # Get configuration from environment variables or use defaults
    imap_host = os.environ.get('IMAP_HOST', 'imap.example.com')
    imap_port = int(os.environ.get('IMAP_PORT', '993'))
    imap_user = os.environ.get('IMAP_USER', 'user@example.com')
    imap_password = os.environ.get('IMAP_PASSWORD', 'password')
    mailbox = os.environ.get('IMAP_MAILBOX', 'INBOX')
    
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    mongo_db = os.environ.get('MONGO_DB', 'email_db')
    mongo_collection = os.environ.get('MONGO_COLLECTION', 'emails')
    
    # Create the fetcher
    fetcher = ImapFetcher(
        imap_host=imap_host,
        imap_port=imap_port,
        imap_user=imap_user,
        imap_password=imap_password,
        mailbox=mailbox,
        mongo_uri=mongo_uri,
        mongo_db=mongo_db,
        mongo_collection=mongo_collection,
        callback=email_callback
    )
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Shutting down...")
        fetcher.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the fetcher
        logger.info("Starting email fetcher...")
        fetcher.start()
        
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Stop the fetcher
        fetcher.stop()


if __name__ == "__main__":
    main()