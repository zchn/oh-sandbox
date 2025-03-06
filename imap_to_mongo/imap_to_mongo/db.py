import pymongo
from datetime import datetime
from typing import Dict, Any, List, Optional


class MongoEmailStorage:
    """
    A class to handle storing and retrieving emails from MongoDB.
    """
    
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        """
        Initialize the MongoDB connection.
        
        Args:
            mongo_uri: MongoDB connection URI
            db_name: Database name
            collection_name: Collection name for storing emails
        """
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
        # Create indexes for efficient querying
        self.collection.create_index("message_id", unique=True)
        self.collection.create_index("date")
        self.collection.create_index("uid")
        
    def insert_email(self, email_data: Dict[str, Any]) -> str:
        """
        Insert an email into MongoDB.
        
        Args:
            email_data: Dictionary containing email data
            
        Returns:
            The inserted document ID
        """
        # Add timestamp for when the email was stored
        email_data["stored_at"] = datetime.utcnow()
        
        # Handle duplicate emails (same message_id)
        if "message_id" in email_data and email_data["message_id"]:
            try:
                result = self.collection.update_one(
                    {"message_id": email_data["message_id"]},
                    {"$set": email_data},
                    upsert=True
                )
                return str(result.upserted_id) if result.upserted_id else str(email_data["_id"])
            except pymongo.errors.DuplicateKeyError:
                # If there's a race condition, just get the existing document
                existing = self.collection.find_one({"message_id": email_data["message_id"]})
                return str(existing["_id"])
        else:
            # If no message_id, just insert as new
            result = self.collection.insert_one(email_data)
            return str(result.inserted_id)
    
    def get_latest_uid(self, mailbox: str) -> Optional[int]:
        """
        Get the highest UID stored for a specific mailbox.
        
        Args:
            mailbox: Name of the mailbox
            
        Returns:
            The highest UID or None if no emails are stored
        """
        result = self.collection.find_one(
            {"mailbox": mailbox},
            sort=[("uid", pymongo.DESCENDING)]
        )
        return result["uid"] if result else None
    
    def get_email_by_uid(self, mailbox: str, uid: int) -> Optional[Dict[str, Any]]:
        """
        Get an email by its UID and mailbox.
        
        Args:
            mailbox: Name of the mailbox
            uid: UID of the email
            
        Returns:
            The email document or None if not found
        """
        return self.collection.find_one({"mailbox": mailbox, "uid": uid})
    
    def get_emails_since_date(self, date: datetime) -> List[Dict[str, Any]]:
        """
        Get all emails received since a specific date.
        
        Args:
            date: The date to filter emails by
            
        Returns:
            List of email documents
        """
        return list(self.collection.find({"date": {"$gte": date}}))
    
    def close(self):
        """Close the MongoDB connection."""
        self.client.close()