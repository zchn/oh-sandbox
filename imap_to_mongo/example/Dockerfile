FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY setup.py .
COPY README.md .
COPY imap_to_mongo ./imap_to_mongo

# Install the package
RUN pip install --no-cache-dir -e .

# Install MongoDB client for debugging
RUN apt-get update && apt-get install -y --no-install-recommends \
    mongodb-clients \
    && rm -rf /var/lib/apt/lists/*

# Copy the example script
COPY main.py .

# Set environment variables (these should be overridden at runtime)
ENV IMAP_HOST=imap.example.com
ENV IMAP_PORT=993
ENV IMAP_USER=user@example.com
ENV IMAP_PASSWORD=password
ENV IMAP_MAILBOX=INBOX
ENV MONGO_URI=mongodb://mongo:27017/
ENV MONGO_DB=email_db
ENV MONGO_COLLECTION=emails

# Run the example script
CMD ["python", "main.py"]