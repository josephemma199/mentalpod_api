import pytest, anyio
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_topics():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/topics", json={
            "theme": "AI at work and men's mental health",
            "audience": "YouTube general public",
            "count": 10
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "ideas" in data and isinstance(data["ideas"], list)
