import poplib
import email
from email.parser import BytesParser
from email.policy import default
from typing import Dict, List, Optional
from pymongo import MongoClient

class MailToMongo:
    def __init__(self, pop3_host: str, pop3_port: int, username: str, password: str,
                 mongo_uri: str, db_name: str, collection_name: str,
                 use_ssl: bool = True):
        self.pop3_host = pop3_host
        self.pop3_port = pop3_port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl

        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]

    def connect_pop3(self) -> poplib.POP3:
        if self.use_ssl:
            server = poplib.POP3_SSL(self.pop3_host, self.pop3_port)
        else:
            server = poplib.POP3(self.pop3_host, self.pop3_port)

        server.user(self.username)
        server.pass_(self.password)
        return server

    def parse_email(self, raw_email: List[bytes]) -> Dict:
        email_content = b'\n'.join(raw_email)
        msg = BytesParser(policy=default).parsebytes(email_content)

        email_dict = {
            "subject": msg.get("subject", ""),
            "from": msg.get("from", ""),
            "to": msg.get("to", ""),
            "date": msg.get("date", ""),
            "body": "",
            "attachments": []
        }

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_dict["body"] = part.get_payload(decode=True).decode()
                elif part.get_content_type() != "multipart/mixed":
                    filename = part.get_filename()
                    if filename:
                        email_dict["attachments"].append({
                            "filename": filename,
                            "content_type": part.get_content_type()
                        })
        else:
            email_dict["body"] = msg.get_payload(decode=True).decode()

        return email_dict

    def fetch_and_store(self, limit: Optional[int] = None) -> int:
        server = self.connect_pop3()
        num_messages = len(server.list()[1])

        if limit is not None:
            num_messages = min(num_messages, limit)

        stored_count = 0
        for i in range(num_messages):
            msg_num = i + 1
            raw_email = server.retr(msg_num)[1]
            email_dict = self.parse_email(raw_email)

            self.collection.insert_one(email_dict)
            stored_count += 1

        server.quit()
        return stored_count
