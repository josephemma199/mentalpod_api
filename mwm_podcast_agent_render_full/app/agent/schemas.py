from typing import List, Optional, Literal
from pydantic import BaseModel, Field
class TopicRequest(BaseModel):
    theme: str
    audience: str = "YouTube general public"
    count: int = Field(12, ge=1, le=30)
    include_finance_lens: bool = True
class TopicIdea(BaseModel):
    title: str
    rationale: str
    seo_keywords: List[str]
    angle_tags: List[str]
class TopicResponse(BaseModel):
    theme: str
    ideas: List[TopicIdea]
class ResearchRequest(BaseModel):
    topic_title: str
    subquestions: List[str] = Field(default_factory=list)
    require_min_citations: int = Field(10, ge=0)
    max_sources: int = Field(25, ge=1, le=100)
class Source(BaseModel):
    title: str
    authors: List[str] = []
    year: Optional[int] = None
    venue: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    peer_reviewed: bool = False
    citation_count: Optional[int] = None
    source_type: Literal["journal","book","other"] = "journal"
class EvidenceRow(BaseModel):
    claim_or_question: str
    source_doi: Optional[str] = None
    study_design: Optional[str] = None
    n: Optional[str] = None
    key_findings: Optional[str] = None
    limitations: Optional[str] = None
class ResearchResponse(BaseModel):
    topic_title: str
    sources_peer_reviewed_10plus: List[Source]
    sources_other: List[Source]
    evidence_table: List[EvidenceRow]
class OutlineRequest(BaseModel):
    topic_title: str
    angle: Optional[str] = None
    target_duration_min: int = Field(60, ge=15, le=180)
    include_guest_variant: bool = True
    research: Optional[ResearchResponse] = None
class OutlineSection(BaseModel):
    heading: str
    bullets: List[str]
class OutlineResponse(BaseModel):
    topic_title: str
    youtube_titles: List[str]
    sections: List[OutlineSection]
    references_md: str
class EpisodePackageRequest(BaseModel):
    outline_request: OutlineRequest
    host_roles: List[str] = Field(default_factory=lambda: ["Psychiatrist","Psychologist"])
class HostDoc(BaseModel):
    role: str
    tone_notes: List[str]
    perspective_prompts: List[str]
    must_cover: List[str]
    caution_flags: List[str]
class EpisodePackageResponse(BaseModel):
    outline: OutlineResponse
    host_docs: List[HostDoc]
class AnalyzeRequest(BaseModel):
    audio_url: Optional[str] = None
    youtube_url: Optional[str] = None
class AnalyzeResponse(BaseModel):
    title: Optional[str] = None
    summary: str
    highlights: List[str]
    takeaways: List[str]
