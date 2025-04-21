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
PLAYER_SCORING_DOC_ID = '1WniCNo5TrszT6fgWpwgPVAFD17-RGwXCQM2Fq160FlY'
NPC_SCORING_DOC_ID = '1G8vf639dMVQT7g1nS0gsgNMaYhAMtTkLLbImq5OtNeM'
BYSTANDER_DOC_ID = '1-ApIS9gz6iWDzlbl5ywJnxcOHHc5LZbIe8aS1qGohzY'
FAN_DOC_ID = '1pVPPssCcUyHlX8a4u99IlsL4YoGnkcXDN2D5SyVupBk'
HATER_DOC_ID = '1ZKfqY_2Hxuvxtj61L-Yhzczq4Fq-HMrsCNONxH6H03o'


def extract_google_doc_content(target_doc: str):
    if target_doc == "battle":
        doc_id = BATTLE_PROFILE_ID
    elif target_doc == "player_score":
        doc_id = PLAYER_SCORING_DOC_ID
    elif target_doc == "npc_score":
        doc_id = NPC_SCORING_DOC_ID
    elif target_doc == "bystander":
        doc_id = BYSTANDER_DOC_ID
    elif target_doc == "fan":
        doc_id = FAN_DOC_ID
    elif target_doc == "hater":
        doc_id = HATER_DOC_ID
    elif target_doc == "rapper":
        doc_id = CHAT_PROFILE_ID
    # Retrieve the document content
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = ''
    for element in doc.get('body').get('content'):
        if 'paragraph' in element:
            for text_run in element['paragraph']['elements']:
                content += text_run.get('textRun', {}).get('content', '')

    return content
