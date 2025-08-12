import os, httpx
from typing import List, Dict, Any

BASE = "https://api.crossref.org/works"

class CrossrefClient:
    def __init__(self):
        self.mailto = os.getenv("CROSSREF_MAILTO","you@example.com")

    async def search(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        params = {"query.bibliographic": query, "rows": max_results, "mailto": self.mailto}
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(BASE, params=params)
            r.raise_for_status()
            data = r.json()
        items = (data.get("message", {}) or {}).get("items", [])
        out = []
        for it in items:
            typ = it.get("type","journal-article")
            out.append({
                "title": (it.get("title") or [""])[0],
                "authors": [f"{a.get('given','')} {a.get('family','')}".strip() for a in it.get("author",[])],
                "year": (it.get("issued",{}).get("date-parts") or [[None]])[0][0],
                "venue": (it.get("container-title") or [""])[0],
                "url": it.get("URL"),
                "doi": it.get("DOI"),
                "peer_reviewed": typ in ["journal-article","proceedings-article"],
                "citation_count": None,  # Crossref doesn't reliably return citation counts
                "source_type": "journal" if typ.endswith("article") else ("book" if "book" in typ else "other")
            })
        return out
