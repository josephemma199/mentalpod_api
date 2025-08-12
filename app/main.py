from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.agent.schemas import TopicRequest, TopicResponse, ResearchRequest, ResearchResponse, OutlineRequest, OutlineResponse, EpisodePackageRequest, EpisodePackageResponse, AnalyzeRequest, AnalyzeResponse
from app.agent.loop import AgentOrchestrator

app = FastAPI(title="Mental Wealth MD Podcast Agent", version="0.1.0")

agent = AgentOrchestrator()

@app.post("/topics", response_model=TopicResponse)
async def generate_topics(req: TopicRequest):
    return await agent.generate_topics(req)

@app.post("/research", response_model=ResearchResponse)
async def research(req: ResearchRequest):
    return await agent.research(req)

@app.post("/outline", response_model=OutlineResponse)
async def outline(req: OutlineRequest):
    return await agent.outline(req)

@app.post("/episode-package", response_model=EpisodePackageResponse)
async def episode_package(req: EpisodePackageRequest, export: bool = False):
    pkg = await agent.episode_package(req)
    if export:
        outline_md = "\n\n".join([f"# {s.heading}\n- " + "\n- ".join(s.bullets) for s in pkg.outline.sections])
        links = await agent.export_outputs(pkg.outline.topic_title, outline_md, pkg.outline.references_md, pkg.outline.youtube_titles)
        return {"outline": pkg.outline.model_dump(), "host_docs": [d.model_dump() for d in pkg.host_docs], "exports": links}
    return pkg

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    return await agent.analyze(req)

@app.get("/healthz")
async def healthz():
    return JSONResponse({"status": "ok"})
