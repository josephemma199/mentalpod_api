import httpx
from bs4 import BeautifulSoup
class BasicScraper:
    async def fetch_text(self,url,max_chars=5000):
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                r=await c.get(url); r.raise_for_status(); html=r.text
            soup=BeautifulSoup(html,'lxml'); text=soup.get_text('\n',strip=True); return text[:max_chars]
        except Exception:
            return None
