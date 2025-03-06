# IMAP to MongoDB Examples

This directory contains examples of how to use the `imap_to_mongo` package.

## Basic Example

The `main.py` script demonstrates how to use the `ImapFetcher` class to fetch emails from an IMAP server and store them in MongoDB.

### Running the Basic Example

1. Install the package:
   ```bash
   pip install -e ..
   ```

2. Set the environment variables:
   ```bash
   export IMAP_HOST=imap.example.com
   export IMAP_PORT=993
   export IMAP_USER=your_email@example.com
   export IMAP_PASSWORD=your_password
   export MONGO_URI=mongodb://localhost:27017/
   export MONGO_DB=email_db
   export MONGO_COLLECTION=emails
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Docker Example

The `Dockerfile` and `docker-compose.yml` files demonstrate how to run the package in a containerized environment.

### Running with Docker Compose

1. Set the environment variables in a `.env` file:
   ```
   IMAP_HOST=imap.example.com
   IMAP_PORT=993
   IMAP_USER=your_email@example.com
   IMAP_PASSWORD=your_password
   MONGO_DB=email_db
   MONGO_COLLECTION=emails
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Check the logs:
   ```bash
   docker-compose logs -f imap-fetcher
   ```

4. Stop the containers:
   ```bash
   docker-compose down
   ```

## Customizing the Example

You can customize the example by modifying the `email_callback` function in `main.py` to perform additional processing when new emails are received.

For example, you could:
- Send notifications
- Trigger workflows
- Extract specific information from emails
- Forward emails to other systems