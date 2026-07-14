"""Tests"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "running"


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_info():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/info")
        assert r.status_code == 200
        data = r.json()
        assert data["features"]["ai_tools"] == 30


@pytest.mark.asyncio
async def test_ai_tools_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/ai/tools")
        assert r.status_code == 200
        tools = r.json()
        assert len(tools) >= 30
        assert any(t["id"] == "business-plan" for t in tools)


@pytest.mark.asyncio
async def test_payments_methods():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/payments/methods")
        assert r.status_code == 200
        methods = r.json()
        assert any(m["id"] == "payme" for m in methods)


@pytest.mark.asyncio
async def test_premium_plans():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/payments/premium/plans")
        assert r.status_code == 200
        plans = r.json()
        assert len(plans) == 3


@pytest.mark.asyncio
async def test_search_suggestions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/search/suggestions?q=test")
        assert r.status_code == 200
