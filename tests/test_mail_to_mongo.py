import pytest
from mail_to_mongo import MailToMongo
from unittest.mock import MagicMock, patch

@pytest.fixture
def mail_fetcher():
    config = {
        "pop3_host": "pop.example.com",
        "pop3_port": 995,
        "username": "test@example.com",
        "password": "password",
        "mongo_uri": "mongodb://localhost:27017/",
        "db_name": "test_db",
        "collection_name": "test_collection"
    }
    return MailToMongo(**config)

@pytest.fixture
def mock_email_data():
    return [
        b"Subject: Test Email",
        b"From: sender@example.com",
        b"To: recipient@example.com",
        b"Date: Wed, 6 Mar 2024 10:00:00 +0000",
        b"",
        b"This is a test email body"
    ]

def test_parse_email(mail_fetcher, mock_email_data):
    result = mail_fetcher.parse_email(mock_email_data)

    assert isinstance(result, dict)
    assert "subject" in result
    assert "from" in result
    assert "to" in result
    assert "date" in result
    assert "body" in result
    assert "attachments" in result

@patch('poplib.POP3_SSL')
def test_connect_pop3_ssl(mock_pop3_ssl, mail_fetcher):
    mock_server = MagicMock()
    mock_pop3_ssl.return_value = mock_server

    server = mail_fetcher.connect_pop3()

    mock_pop3_ssl.assert_called_once_with("pop.example.com", 995)
    mock_server.user.assert_called_once_with("test@example.com")
    mock_server.pass_.assert_called_once_with("password")
    assert server == mock_server

@patch('poplib.POP3')
def test_connect_pop3_no_ssl(mock_pop3, mail_fetcher):
    mail_fetcher.use_ssl = False
    mock_server = MagicMock()
    mock_pop3.return_value = mock_server

    server = mail_fetcher.connect_pop3()

    mock_pop3.assert_called_once_with("pop.example.com", 995)
    mock_server.user.assert_called_once_with("test@example.com")
    mock_server.pass_.assert_called_once_with("password")
    assert server == mock_server

@patch('mail_to_mongo.MailToMongo.connect_pop3')
@patch('pymongo.MongoClient')
def test_fetch_and_store(mock_mongo_client, mock_connect_pop3, mail_fetcher, mock_email_data):
    # Mock MongoDB
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_mongo_client.return_value.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    mail_fetcher.mongo_client = mock_mongo_client.return_value
    mail_fetcher.db = mock_db
    mail_fetcher.collection = mock_collection

    # Mock POP3 server
    mock_server = MagicMock()
    mock_server.list.return_value = (None, [b"1 1234"], None)
    mock_server.retr.return_value = (None, mock_email_data, None)
    mock_connect_pop3.return_value = mock_server

    stored_count = mail_fetcher.fetch_and_store(limit=1)

    assert stored_count == 1
    mock_server.quit.assert_called_once()
    mock_server.retr.assert_called_once_with(1)
    mock_collection.insert_one.assert_called_once()
