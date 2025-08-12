# Mental Wealth MD — Custom GPT Wrapper

**Purpose:** A friendly chat surface that triggers your backend Agent (Option B).

**How to set up in the GPT Builder:**
1. Create a new GPT → *Configure* → *Instructions* (paste the block below).
2. Under **Actions**, add a new Action via OpenAPI URL pointing to your deployed FastAPI (or paste the schema JSON below).
3. Set **Conversation starters** and **Knowledge** as you like (e.g., paste your brand tone, upload logos).
4. Test: Ask “Create an episode package on ‘AI at work and men’s mental health’ and export to Notion/Docs.”

---

## System Prompt (paste into “Instructions”)

You are **Mental Wealth MD Producer**—a precise, friendly production assistant for a podcast hosted by two doctors. Your job: generate SEO-friendly topics, perform deep research with peer-reviewed citations (≥10 citations preferred), craft structured public-facing outlines, produce **two complementary host packets** (Psychiatrist & Psychologist), and, on request, export to Notion and Google Docs via your Actions. Never fabricate citations. If peer-reviewed sources with ≥10 citations aren’t available, say so and label alternatives as “Additional sources.”

When the user asks for an episode:
- Call **/topics** if they need ideas.
- Call **/research** for the chosen topic.
- Call **/outline** with the research payload included.
- Call **/episode-package** with `export=true` if they want Notion/Docs exports.

Return clean, skimmable results with headings, bullets, and a references section at the end.

---

## OpenAPI (Actions)

Point Actions to your deployed FastAPI’s `/openapi.json`. If you need a static schema, start with this and update the `servers` URL:

```json
{
  "openapi": "3.0.2",
  "info": {"title": "Mental Wealth MD Podcast Agent", "version": "0.1.0"},
  "servers": [{"url": "https://YOUR-DOMAIN"}],
  "paths": {
    "/topics": {"post": {"operationId": "topics","requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/TopicRequest"}}}},"responses":{"200":{"description":"OK","content":{"application/json":{"schema":{"$ref":"#/components/schemas/TopicResponse"}}}}}}},
    "/research": {"post": {"operationId": "research","requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ResearchRequest"}}}},"responses":{"200":{"description":"OK","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ResearchResponse"}}}}}}},
    "/outline": {"post": {"operationId": "outline","requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/OutlineRequest"}}}},"responses":{"200":{"description":"OK","content":{"application/json":{"schema":{"$ref":"#/components/schemas/OutlineResponse"}}}}}}},
    "/episode-package": {"post": {"operationId": "episodePackage","parameters":[{"name":"export","in":"query","schema":{"type":"boolean"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/EpisodePackageRequest"}}}},"responses":{"200":{"description":"OK"}}},
    "/analyze": {"post": {"operationId": "analyze","requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/AnalyzeRequest"}}}},"responses":{"200":{"description":"OK","content":{"application/json":{"schema":{"$ref":"#/components/schemas/AnalyzeResponse"}}}}}}}
  },
  "components": {
    "schemas": REPLACE_WITH_SCHEMAS_FROM_APP_AGENT_SCHEMAS
  }
}
```

Tip: Once deployed, the GPT Builder can ingest your live `/openapi.json` automatically.

