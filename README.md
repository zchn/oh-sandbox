# Mail to MongoDB

A Python package that fetches emails from a POP3 mail server and stores them in a MongoDB database.

## Features

- Fetch emails from POP3 servers (with SSL support)
- Parse email content including subject, sender, recipient, body, and attachments
- Store emails in MongoDB
- Configurable limit on number of emails to fetch
- Support for both plain text and multipart emails

## Installation

```bash
pip install mail_to_mongo
```

## Usage

Here's a basic example of how to use the package:

```python
from mail_to_mongo import MailToMongo

# Configure the connection
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

# Fetch and store the last 10 emails
stored_count = mail_fetcher.fetch_and_store(limit=10)
print(f"Successfully stored {stored_count} emails in MongoDB")
```

See the `example` folder for a complete working example.

## Development

1. Clone the repository
2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
