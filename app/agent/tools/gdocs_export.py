import os, io
from typing import Optional, List
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive.file"]

def _creds():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=SCOPES,
    )
    return creds

class GoogleDocsExporter:
    def __init__(self):
        self.enabled = all([os.getenv("GOOGLE_CLIENT_ID"), os.getenv("GOOGLE_CLIENT_SECRET"), os.getenv("GOOGLE_REFRESH_TOKEN")])

    def create_doc(self, title: str, markdown: str) -> Optional[str]:
        if not self.enabled:
            return None
        creds = _creds()
        docs = build("docs","v1", credentials=creds)
        drive = build("drive","v3", credentials=creds)

        # 1) Create a blank doc
        doc = docs.documents().create(body={"title": title}).execute()
        doc_id = doc.get("documentId")

        # 2) Insert text (simple plain-text; Markdown not rendered natively)
        requests = [{
            "insertText": {"text": markdown, "location": {"index": 1}}
        }]
        docs.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

        # 3) Move to parent folder if provided
        parent = os.getenv("GOOGLE_DRIVE_PARENT_ID")
        if parent:
            drive.files().update(fileId=doc_id, addParents=parent, fields="id, parents").execute()

        return f"https://docs.google.com/document/d/{doc_id}/edit"
