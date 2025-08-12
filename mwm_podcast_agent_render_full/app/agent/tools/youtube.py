import httpx
class YouTubeHelper:
    async def fetch_metadata(self,url):
        if not url: return {}
        try:
            o=f'https://www.youtube.com/oembed?url={url}&format=json'
            async with httpx.AsyncClient(timeout=15) as c:
                r=await c.get(o)
                if r.status_code==200:
                    d=r.json(); return {'title': d.get('title')}
        except Exception:
            pass
        return {}
