import os
import spacy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER = int(os.getenv("AUTHORIZED_USER", ""))
SHEET_NAME = os.getenv("SHEET_NAME", "CEO Tasks")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", "credentials.json")

# Google Sheet Configuration

# Google Service Account Credentials
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_PRIVATE_KEY_ID = os.getenv("GOOGLE_PRIVATE_KEY_ID")
GOOGLE_PRIVATE_KEY = os.getenv("GOOGLE_PRIVATE_KEY")
GOOGLE_CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# Initialize SpaCy model once
nlp = spacy.load("en_core_web_sm")
