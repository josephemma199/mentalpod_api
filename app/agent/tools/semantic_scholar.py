import os, httpx
from typing import List, Dict, Any

BASE = "https://api.semanticscholar.org/graph/v1/paper/search"

class SemanticScholarClient:
    def __init__(self):
        self.apikey = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    async def search(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,year,venue,url,doi,citationCount"
        }
        headers = {"x-api-key": self.apikey} if self.apikey else {}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(BASE, params=params, headers=headers)
            r.raise_for_status()
            data = r.json()
        items = data.get("data", [])
        out = []
        for it in items:
            out.append({
                "title": it.get("title",""),
                "authors": [a.get("name","") for a in (it.get("authors") or [])],
                "year": it.get("year"),
                "venue": it.get("venue"),
                "url": it.get("url"),
                "doi": it.get("doi"),
                "peer_reviewed": True if it.get("venue") else False,
                "citation_count": it.get("citationCount"),
                "source_type": "journal"
            })
        return out
