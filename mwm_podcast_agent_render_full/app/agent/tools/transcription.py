import os, httpx, tempfile
from openai import OpenAI
class Transcriber:
    def __init__(self): self.client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    def _download(self,url):
        with httpx.Client(timeout=120) as c:
            r=c.get(url, follow_redirects=True); r.raise_for_status(); import os as _os
            fd, path=_os.tmpfile if hasattr(_os,'tmpfile') else __import__('tempfile').mkstemp(suffix='.mp3');
        return path
    def transcribe(self,audio_url=None,audio_path=None):
        if not (audio_url or audio_path): return ('', None)
        path=audio_path or self._download(audio_url)
        with open(path,'rb') as f:
            t=self.client.audio.transcriptions.create(model='whisper-1', file=f)
        text=getattr(t,'text','') or getattr(getattr(t,'data',[{}])[0],'text','')
        return (text, None)
