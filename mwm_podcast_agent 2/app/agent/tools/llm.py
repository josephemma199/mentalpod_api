import os, json, re, asyncio
from typing import List, Dict, Any
from openai import AsyncOpenAI

class ChatLLM:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY", None)
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def complete(self, system: str, user: str) -> str:
        if not self.client:
            # Offline/dev fallback (echoes an instructive stub)
            return f"""{{"youtube_titles": ["Sample Title"], "sections": [{{"heading": "Intro", "bullets": ["Hook", "Context"]}}]}}"""
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role":"system","content":system},
                {"role":"user","content":user}
            ],
            temperature=0.7
        )
        return resp.choices[0].message.content

    # ---- Parsing helpers ----

    def safe_parse_topic_ideas(self, text: str, default_count: int = 12):
        try:
            data = json.loads(text)
            ideas = []
            for item in data:
                ideas.append({
                    "title": item.get("title",""),
                    "rationale": item.get("rationale",""),
                    "seo_keywords": item.get("seo_keywords",[]),
                    "angle_tags": item.get("angle_tags",[])
                })
            return ideas
        except Exception:
            # naive fallback
            lines = [l.strip("- ").strip() for l in text.splitlines() if l.strip()]
            ideas = []
            for i, l in enumerate(lines[:default_count]):
                ideas.append({"title": l, "rationale": "N/A", "seo_keywords": [], "angle_tags": []})
            return ideas

    def safe_parse_outline(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            # Extract simple sections
            sections = []
            current = {"heading":"Section","bullets":[]}
            for line in text.splitlines():
                if line.startswith("#"):
                    if current["bullets"]:
                        sections.append(current)
                    current = {"heading": line.strip("# ").strip(), "bullets":[]}
                elif line.startswith("- "):
                    current["bullets"].append(line[2:].strip())
            if current["bullets"]:
                sections.append(current)
            return {"youtube_titles": ["Draft Title"], "sections": sections}

    def safe_parse_hostdoc(self, text: str, role: str):
        try:
            data = json.loads(text)
            return type("HostDocObj",(object,),{"role":role, **data})()
        except Exception:
            tone = ["Warm, curious, collaborative"]
            prompts = ["Open with a personal vignette that tees up the evidence."]
            must = ["Hit the core evidence and define terms clearly."]
            flags = ["Avoid overgeneralizing from single studies."]
            return type("HostDocObj",(object,),{
                "role": role,
                "tone_notes": tone,
                "perspective_prompts": prompts,
                "must_cover": must,
                "caution_flags": flags
            })()

    def safe_parse_analysis(self, text: str, fallback_title=None):
        try:
            data = json.loads(text)
            return type("Analysis",(object,),{
                "title": data.get("title", fallback_title),
                "summary": data.get("summary", ""),
                "highlights": data.get("highlights", []),
                "takeaways": data.get("takeaways", [])
            })()
        except Exception:
            return type("Analysis",(object,),{
                "title": fallback_title,
                "summary": text[:400],
                "highlights": [],
                "takeaways": []
            })()
