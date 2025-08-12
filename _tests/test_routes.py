from fastapi.testclient import TestClient
from backend.app.core.landing_page.ahrefs.client import AhrefsClient


def test_overview_route(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    def stub_overview(*, target: str, **extra):
        assert target == "example.com"
        return {"ok": True, "data": {"dr": 75}}

    monkeypatch.setattr(fake_client, "get_overview", stub_overview)

    res = client.get("/ahrefs/overview/overview", params={"target": "example.com"})
    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True
    assert body["data"]["dr"] == 75


def test_serp_overview_route(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    def stub_serp_overview(*, query: str, **extra):
        assert query == "coffee grinder"
        return {"ok": True, "data": {"positions": []}}

    monkeypatch.setattr(fake_client, "get_serp_overview", stub_serp_overview)

    res = client.get("/ahrefs/serp/overview", params={"query": "coffee grinder"})
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_batch_analysis_route(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    def stub_post_batch_analysis(*, items, **extra):
        assert items == ["a.com", "b.com"]
        return {"ok": True, "data": {"results": [1, 2]}}

    monkeypatch.setattr(fake_client, "post_batch_analysis", stub_post_batch_analysis)

    res = client.post("/ahrefs/batch-analysis", json={"items": ["a.com", "b.com"]})
    assert res.status_code == 200
    assert res.json()["data"]["results"] == [1, 2]


def test_management_projects_routes(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    monkeypatch.setattr(fake_client, "get_projects", lambda **kw: {"ok": True, "data": ["p1"]})
    res = client.get("/ahrefs/management/projects")
    assert res.status_code == 200
    assert res.json()["data"] == ["p1"]

    def stub_create_project(*, name: str, target: str, **extra):
        assert name == "Demo" and target == "example.com"
        return {"ok": True, "data": {"project_id": "p1"}}

    monkeypatch.setattr(fake_client, "create_project", stub_create_project)
    res = client.post("/ahrefs/management/projects", json={"name": "Demo", "target": "example.com"})
    assert res.status_code == 200
    assert res.json()["data"]["project_id"] == "p1"


def test_public_crawler_routes(client: TestClient, fake_client: AhrefsClient, monkeypatch):
    monkeypatch.setattr(fake_client, "get_crawler_ip_addresses", lambda **kw: {"ok": True, "data": {"ips": ["1.2.3.4"]}})
    r1 = client.get("/ahrefs/public/crawler-ip-addresses")
    assert r1.status_code == 200
    assert r1.json()["data"]["ips"] == ["1.2.3.4"]

    monkeypatch.setattr(fake_client, "get_crawler_ip_ranges", lambda **kw: {"ok": True, "data": {"ranges": ["1.2.3.0/24"]}})
    r2 = client.get("/ahrefs/public/crawler-ip-ranges")
    assert r2.status_code == 200
    assert r2.json()["data"]["ranges"] == ["1.2.3.0/24"]
