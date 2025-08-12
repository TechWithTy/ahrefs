from fastapi.testclient import TestClient
from backend.app.core.landing_page.ahrefs.client import AhrefsClient


def test_competitors_pages_route(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    def stub_competitors_pages(*, target: str, **extra):
        assert target == "example.com"
        assert extra.get("limit") == 50
        assert extra.get("offset") == 10
        return {"ok": True, "data": {"pages": ["/a", "/b"]}}

    monkeypatch.setattr(fake_client, "get_competitors_pages", stub_competitors_pages)

    r = client.get(
        "/ahrefs/overview/competitors-pages",
        params={"target": "example.com", "limit": 50, "offset": 10},
    )
    assert r.status_code == 200
    assert r.json()["data"]["pages"] == ["/a", "/b"]


def test_subscription_limits_and_usage_route(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    monkeypatch.setattr(fake_client, "get_limits_and_usage", lambda **k: {"ok": True, "data": {"remaining": 111}})
    r = client.get("/ahrefs/subscription/limits-and-usage")
    assert r.status_code == 200
    assert r.json()["data"]["remaining"] == 111


def test_management_keywords_endpoints(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    monkeypatch.setattr(fake_client, "get_keywords", lambda project_id, **k: {"ok": True, "data": ["kw1"]})
    r1 = client.get("/ahrefs/management/keywords", params={"project_id": "pid"})
    assert r1.status_code == 200
    assert r1.json()["data"] == ["kw1"]

    def stub_put_keywords(*, project_id: str, keywords: list[str], **extra):
        assert project_id == "pid"
        assert keywords == ["a", "b"]
        return {"ok": True, "data": {"updated": 2}}

    monkeypatch.setattr(fake_client, "put_keywords", stub_put_keywords)
    r2 = client.put("/ahrefs/management/keywords", json={"project_id": "pid", "keywords": ["a", "b"]})
    assert r2.status_code == 200
    assert r2.json()["data"]["updated"] == 2

    def stub_delete_keywords(*, project_id: str, keywords: list[str], **extra):
        assert project_id == "pid"
        assert keywords == ["x"]
        return {"ok": True, "data": {"deleted": 1}}

    monkeypatch.setattr(fake_client, "delete_keywords", stub_delete_keywords)
    r3 = client.put("/ahrefs/management/keywords/delete", json={"project_id": "pid", "keywords": ["x"]})
    assert r3.status_code == 200
    assert r3.json()["data"]["deleted"] == 1
