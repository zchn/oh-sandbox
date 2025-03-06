# IMAP to MongoDB

A Python package to fetch emails from an IMAP server and store them in MongoDB.

## Features

- Stream emails from an IMAP server in real-time
- Store emails in MongoDB for persistence
- Resume capability to continue from where it left off
- Support for various email formats and attachments

## Installation

```bash
pip install imap-to-mongo
```

## Usage

```python
from imap_to_mongo import ImapFetcher

# Configure the fetcher
fetcher = ImapFetcher(
    imap_host="imap.example.com",
    imap_port=993,
    imap_user="your_email@example.com",
    imap_password="your_password",
    mongo_uri="mongodb://localhost:27017/",
    mongo_db="email_db",
    mongo_collection="emails"
)

# Start fetching emails
fetcher.start()

# To stop fetching
fetcher.stop()
```

See the `example` directory for more detailed usage examples.

## License

MIT