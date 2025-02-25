from googleapiclient.discovery import build
from google.oauth2 import service_account
import numpy as np
import faiss
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Google Service Account Authentication
# SERVICE_ACCOUNT_FILE = os.path.join("services", "credentials.json")
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES
# )

# Load credentials from environment variable instead of a file
credentials_json = os.getenv("GOOGLE_CREDENTIALS")

if credentials_json is None:
    raise ValueError("GOOGLE_CREDENTIALS environment variable is missing")

# Convert the credentials string into a dictionary
credentials_dict = json.loads(credentials_json)

# Create Google service credentials
credentials = service_account.Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)

# Build Google Drive and Docs service
drive_service = build('drive', 'v3', credentials=credentials)
docs_service = build('docs', 'v1', credentials=credentials)

# Fetch a specific document from Google Docs
CHAT_PROFILE_ID = '1uxGIwY9Xh87cmCfTJczUlAZ_P9A--36suw5UFLklyfs'
BATTLE_PROFILE_ID = '1GJAwcQMv_PDoB3CEU8LaTOI6xgG7fcc8UKEbnDDuduw'

SCORING_DOC_ID = '19myTnYWqKvp9VH9WOhW2PIyUoOgpCZuiYx1sOdDNjYk'


def extract_google_doc_content(target_doc: str):
    if target_doc == "battle":
        doc_id = BATTLE_PROFILE_ID
    elif target_doc == "chat":
        doc_id = CHAT_PROFILE_ID
    elif target_doc == "score":
        doc_id = SCORING_DOC_ID
    # Retrieve the document content
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = ''
    for element in doc.get('body').get('content'):
        if 'paragraph' in element:
            for text_run in element['paragraph']['elements']:
                content += text_run.get('textRun', {}).get('content', '')

    return content
