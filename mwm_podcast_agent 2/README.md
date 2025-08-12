# Mental Wealth MD Podcast Agent (Option B)

A Python + FastAPI agent that:
- Suggests SEO-friendly podcast topics at the intersection of **mental health, culture, innovation, technology, males across the lifespan, psychiatry, psychology, and finance**.
- Performs **deep research** with peer‑reviewed sources (filters for **≥ 10 citations**).
- Crafts **structured episode outlines** with a **clean reference list** (peer‑reviewed vs. other sources labeled).
- Generates **two complementary host documents** (Psychiatrist & Psychologist perspectives) to guide conversation.
- Suggests **YouTube-ready titles** and **post-episode takeaways** from transcripts or YouTube links.

## Quickstart

```bash
# 1) Create env
python -m venv .venv && source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Set environment (copy and edit .env.example)
cp .env.example .env

# 4) Run dev server
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/docs

## Environment

Copy `.env.example` to `.env` and fill in keys you have:
- `OPENAI_API_KEY` (optional; for LLM generation)
- `OPENAI_MODEL` (default: `gpt-4o-mini` or any chat model you prefer)
- `SEMANTIC_SCHOLAR_API_KEY` (optional but recommended)
- `CROSSREF_MAILTO` (your email for polite Crossref usage)
- `YOUTUBE_API_KEY` (optional, if you plan to fetch transcripts/metadata)
- `NOTION_TOKEN`, `NOTION_DB_ID` (optional integration)

## Endpoints (high-level)

- `POST /topics` — generate 10–20 SEO-friendly titles and angles.
- `POST /research` — fetch and filter sources (peer-reviewed, ≥10 citations), produce evidence table.
- `POST /outline` — produce a public-facing episode outline + references.
- `POST /episode-package` — returns outline **and** two tailored host docs (Psychiatrist & Psychologist) with complementary prompts.
- `POST /analyze` — analyze podcast audio or YouTube URL → summary, highlights, takeaways.

See `app/agent/schemas.py` for request/response shapes and `tests/` for examples.

## Notes on Citations
- Journal sources with `citationCount >= 10` are labeled **Peer-reviewed (≥10 cites)** when possible (via Semantic Scholar or Crossref+OpenAlex).
- Non-journal sources (books, reputable articles) are listed under **Additional sources**.
- All references are returned in JSON and Markdown for easy export.

## Roadmap
- Add OpenAlex fallback for citation counts.
- Add Playwright-powered robust scraping with robots.txt respect.
- Add Notion/Docs export and scheduling integration.
- Add auto-short generation for YouTube/Shorts/TikTok.

---

**Built for Mental Wealth MD.**

