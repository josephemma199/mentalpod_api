import httpx, re
from typing import Optional, Dict

class YouTubeHelper:
    async def fetch_metadata(self, url: Optional[str]) -> Dict:
        if not url:
            return {}
        try:
            # Lightweight oEmbed metadata (no API key required)
            oembed = f"https://www.youtube.com/oembed?url={url}&format=json"
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(oembed)
                if r.status_code == 200:
                    data = r.json()
                    return {"title": data.get("title")}
        except Exception:
            pass
        return {}
