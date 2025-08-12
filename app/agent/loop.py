import os, asyncio
from typing import List
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from .schemas import (
    TopicRequest, TopicResponse, TopicIdea,
    ResearchRequest, ResearchResponse, Source, EvidenceRow,
    OutlineRequest, OutlineResponse, OutlineSection,
    EpisodePackageRequest, EpisodePackageResponse, HostDoc,
    AnalyzeRequest, AnalyzeResponse
)
from .tools.llm import ChatLLM
from .tools.semantic_scholar import SemanticScholarClient
from .tools.crossref import CrossrefClient
from .tools.scrape import BasicScraper
from .tools.youtube import YouTubeHelper
from .tools.notion_export import NotionExporter
from .tools.gdocs_export import GoogleDocsExporter
from .tools.transcription import Transcriber

from .tools.util import dedupe_sources

load_dotenv()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=False)

class AgentOrchestrator:
    def __init__(self):
        self.llm = ChatLLM()
        self.ss = SemanticScholarClient()
        self.cr = CrossrefClient()
        self.scraper = BasicScraper()
        self.ythelper = YouTubeHelper()
        self.notion = NotionExporter()
        self.gdocs = GoogleDocsExporter()
        self.transcriber = Transcriber()


    async def generate_topics(self, req: TopicRequest) -> TopicResponse:
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "prompts", "topic_engine.md")
        with open(prompt_path, "r") as f:
            topic_prompt = f.read()
        user = f"""Theme: {req.theme}
Audience: {req.audience}
Count: {req.count}
Finance lens: {req.include_finance_lens}
"""
        raw = await self.llm.complete(topic_prompt, user)
        # Expect JSON list of ideas; fallback to parsing lines.
        ideas = self.llm.safe_parse_topic_ideas(raw, default_count=req.count)
        return TopicResponse(theme=req.theme, ideas=ideas)

    async def research(self, req: ResearchRequest) -> ResearchResponse:
        # 1) Query sources (Semantic Scholar primary; Crossref fallback)
        results = await self.ss.search(req.topic_title, max_results=req.max_sources)
        if len(results) < req.max_sources // 2:
            results += await self.cr.search(req.topic_title, max_results=req.max_sources)

        # 2) Filter & normalize
        norm: List[Source] = []
        for r in results:
            src = Source(**r)
            norm.append(src)

        # 3) Enforce peer-reviewed (>= min citations) vs other
        peer = [s for s in norm if (s.citation_count or 0) >= req.require_min_citations and s.source_type == "journal"]
        other = [s for s in norm if s not in peer]

        peer, other = dedupe_sources(peer), dedupe_sources(other)

        # 4) Build evidence table skeleton (claims from subquestions)
        evidence = []
        for q in req.subquestions or [f"Key findings related to: {req.topic_title}"]:
            evidence.append(EvidenceRow(claim_or_question=q))

        return ResearchResponse(
            topic_title=req.topic_title,
            sources_peer_reviewed_10plus=peer,
            sources_other=other,
            evidence_table=evidence
        )

    async def outline(self, req: OutlineRequest) -> OutlineResponse:
        # Render outline via LLM with research baked in
        outline_tmpl = env.get_template("outline.md.j2")
        research_md = ""
        if req.research:
            def line(s):
                yr = f" ({s.year})" if s.year else ""
                cite = f" — cites: {s.citation_count}" if s.citation_count is not None else ""
                tag = "Peer-reviewed (≥10 cites)" if s in req.research.sources_peer_reviewed_10plus else "Additional source"
                return f"- {s.title}{yr}. {', '.join(s.authors)}. *{s.venue or ''}*. {s.doi or s.url or ''} [{tag}{cite}]"
            refs_md = ["### References", "#### Peer-reviewed (≥10 citations)"] +                       [line(s) for s in req.research.sources_peer_reviewed_10plus] +                       ["", "#### Additional sources"] +                       [line(s) for s in req.research.sources_other]
            research_md = "\n".join(refs_md)

        system = open(os.path.join(os.path.dirname(__file__), "..", "..", "data", "prompts", "system.md")).read()
        user = outline_tmpl.render(
            topic_title=req.topic_title,
            angle=req.angle or "Most engaging, evidence-forward angle for YouTube audiences",
            duration=req.target_duration_min,
            include_guest_variant=req.include_guest_variant,
            research_markdown=research_md
        )
        raw = await self.llm.complete(system, user)
        parsed = self.llm.safe_parse_outline(raw)

        # Build references_md from research_md (if provided)
        references_md = research_md or "### References\n_(Add research with /research and re-run /outline.)_"
        return OutlineResponse(
            topic_title=req.topic_title,
            youtube_titles=parsed.get("youtube_titles", []),
            sections=[OutlineSection(**s) for s in parsed.get("sections", [])],
            references_md=references_md
        )

    async def episode_package(self, req: EpisodePackageRequest) -> EpisodePackageResponse:
        outline = await self.outline(req.outline_request)

        # Generate complementary host docs
        host_docs: List[HostDoc] = []
        host_tmpl = env.get_template("host_packets.md.j2")
        for role in req.host_roles:
            user = host_tmpl.render(role=role, topic_title=outline.topic_title)
            system = "You are crafting a role-specific, collaborative host guide that complements the co-host, avoids redundancy, and encourages engaging, evidence-based discussion."
            raw = await self.llm.complete(system, user)
            host_docs.append(self.llm.safe_parse_hostdoc(raw, role))

        return EpisodePackageResponse(outline=outline, host_docs=host_docs)

    async def analyze(self, req: AnalyzeRequest) -> AnalyzeResponse:
        meta = await self.ythelper.fetch_metadata(req.youtube_url) if req.youtube_url else {}
        transcript_text = ""
        if req.youtube_url:
            # For now, expect user to provide a downloadable audio link or upload elsewhere;
            # future: add youtube-dl integration if permitted.
            pass
        # If a direct audio URL is provided, transcribe
        # (App could be extended to accept file upload via a different endpoint)
        # transcript_text, _ = self.transcriber.transcribe(audio_url=req.audio_url)

        system = "You are a podcast analyst. Produce a concise summary, 5-7 highlights, and 5 actionable takeaways for listeners."
        user = f"Title: {meta.get('title','(unknown)')}. Transcript: {transcript_text[:600]}"
        raw = await self.llm.complete(system, user)
        return self.llm.safe_parse_analysis(raw, fallback_title=meta.get('title'))
    