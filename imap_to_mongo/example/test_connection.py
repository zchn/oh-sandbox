#!/usr/bin/env python3
"""
Test script to verify IMAP and MongoDB connections.
"""

import os
import sys
import logging
from pymongo import MongoClient
import imaplib2

# Add parent directory to path to import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imap_connection():
    """Test connection to the IMAP server."""
    imap_host = os.environ.get('IMAP_HOST', 'imap.example.com')
    imap_port = int(os.environ.get('IMAP_PORT', '993'))
    imap_user = os.environ.get('IMAP_USER', 'user@example.com')
    imap_password = os.environ.get('IMAP_PASSWORD', 'password')
    
    logger.info(f"Testing IMAP connection to {imap_host}:{imap_port}")
    
    try:
        # Connect to IMAP server
        imap = imaplib2.IMAP4_SSL(imap_host, imap_port)
        
        # Login
        imap.login(imap_user, imap_password)
        logger.info("IMAP login successful")
        
        # List mailboxes
        status, mailboxes = imap.list()
        if status == 'OK':
            logger.info(f"Available mailboxes: {[mb.decode() for mb in mailboxes]}")
        
        # Select INBOX
        status, data = imap.select('INBOX')
        if status == 'OK':
            logger.info(f"INBOX selected, message count: {data[0].decode()}")
        
        # Logout
        imap.logout()
        logger.info("IMAP connection test successful")
        return True
    except Exception as e:
        logger.error(f"IMAP connection test failed: {e}")
        return False


def test_mongo_connection():
    """Test connection to MongoDB."""
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    mongo_db = os.environ.get('MONGO_DB', 'email_db')
    
    logger.info(f"Testing MongoDB connection to {mongo_uri}")
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        
        # Check connection
        client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        # Get database
        db = client[mongo_db]
        
        # List collections
        collections = db.list_collection_names()
        logger.info(f"Collections in {mongo_db}: {collections}")
        
        # Close connection
        client.close()
        logger.info("MongoDB connection test successful")
        return True
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        return False


def main():
    """Main function to run the tests."""
    imap_success = test_imap_connection()
    mongo_success = test_mongo_connection()
    
    if imap_success and mongo_success:
        logger.info("All connection tests passed!")
        return 0
    else:
        logger.error("Some connection tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())