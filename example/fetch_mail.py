from mail_to_mongo import MailToMongo

def main():
    # Example configuration - replace with your actual values
    config = {
        "pop3_host": "pop.example.com",
        "pop3_port": 995,
        "username": "your_email@example.com",
        "password": "your_password",
        "mongo_uri": "mongodb://localhost:27017/",
        "db_name": "email_db",
        "collection_name": "emails"
    }

    # Create MailToMongo instance
    mail_fetcher = MailToMongo(**config)

    try:
        # Fetch and store the last 10 emails
        stored_count = mail_fetcher.fetch_and_store(limit=10)
        print(f"Successfully stored {stored_count} emails in MongoDB")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
