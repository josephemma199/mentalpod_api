import os
from typing import List, Optional
from notion_client import Client

class NotionExporter:
    def __init__(self):
        token = os.getenv("NOTION_TOKEN")
        self.db_id = os.getenv("NOTION_DB_ID")
        self.enabled = bool(token and self.db_id)
        self.client = Client(auth=token) if token else None

    def upsert_episode(self, title: str, youtube_titles: List[str], outline_md: str, references_md: str) -> Optional[str]:
        if not self.enabled:
            return None
        props = {
            "Name": {"title": [{"text": {"content": title}}]},
            "YouTube Titles": {"rich_text": [{"text": {"content": "; ".join(youtube_titles[:5])}}]},
        }
        children = [
            {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":"Outline"}}]}},
            {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content": outline_md[:1800]}}]}},
            {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":"References"}}]}},
            {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content": references_md[:1800]}}]}},
        ]
        page = self.client.pages.create(parent={"database_id": self.db_id}, properties=props, children=children)
        return page.get("url")
