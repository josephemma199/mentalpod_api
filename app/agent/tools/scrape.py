import httpx
from bs4 import BeautifulSoup
from typing import Optional

class BasicScraper:
    async def fetch_text(self, url: str, max_chars: int = 5000) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(url)
                r.raise_for_status()
                html = r.text
            soup = BeautifulSoup(html, "lxml")
            text = soup.get_text("\n", strip=True)
            return text[:max_chars]
        except Exception:
            return None
