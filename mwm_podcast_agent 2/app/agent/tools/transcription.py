import os, httpx, tempfile
from typing import Optional, Tuple
from openai import OpenAI

class Transcriber:
    def __init__(self):
        self.provider = os.getenv("TRANSCRIBE_PROVIDER", "openai")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _download(self, url: str) -> str:
        with httpx.Client(timeout=120) as client:
            r = client.get(url, follow_redirects=True)
            r.raise_for_status()
            fd, path = tempfile.mkstemp(suffix=".mp3")
            with os.fdopen(fd, "wb") as f:
                f.write(r.content)
        return path

    def transcribe(self, audio_url: Optional[str]=None, audio_path: Optional[str]=None) -> Tuple[str, Optional[float]]:
        if not (audio_url or audio_path):
            return ("", None)
        path = audio_path or self._download(audio_url)
        with open(path, "rb") as f:
            t = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        text = t.text if hasattr(t, "text") else getattr(t, "data", [{}])[0].get("text","")
        return (text, None)
