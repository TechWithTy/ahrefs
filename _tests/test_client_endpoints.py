from types import SimpleNamespace

from backend.app.core.landing_page.ahrefs.client import AhrefsClient


def _ok_response(payload: dict):
    return SimpleNamespace(
        status_code=200,
        text="{}",
        json=lambda: {"ok": True, "data": payload},
    )


def test_keywords_overview(monkeypatch):
    client = AhrefsClient()

    def fake_request(method, url, headers=None, params=None, json=None, timeout=None):
        assert method == "GET"
        assert "/keywords-explorer/overview" in url
        assert params.get("query") == "coffee"
        return _ok_response({"search_volume": 123})

    monkeypatch.setattr(client.session, "request", fake_request)

    resp = client.get_keywords_overview(query="coffee")
    assert resp["ok"] is True
    assert resp["data"]["search_volume"] == 123


def test_create_project(monkeypatch):
    client = AhrefsClient()

    def fake_request(method, url, headers=None, params=None, json=None, timeout=None):
        assert method == "POST"
        assert "/management/projects" in url
        assert json == {"name": "Demo", "target": "example.com"}
        return _ok_response({"project_id": "p_1"})

    monkeypatch.setattr(client.session, "request", fake_request)

    resp = client.create_project(name="Demo", target="example.com")
    assert resp["data"]["project_id"] == "p_1"


def test_post_batch_analysis(monkeypatch):
    client = AhrefsClient()

    def fake_request(method, url, headers=None, params=None, json=None, timeout=None):
        assert method == "POST"
        assert "/batch-analysis" in url
        assert json == {"items": ["a.com", "b.com"]}
        return _ok_response({"results": [1, 2]})

    monkeypatch.setattr(client.session, "request", fake_request)

    resp = client.post_batch_analysis(items=["a.com", "b.com"])
    assert resp["data"]["results"] == [1, 2]


def test_serp_overview(monkeypatch):
    client = AhrefsClient()

    def fake_request(method, url, headers=None, params=None, json=None, timeout=None):
        assert method == "GET"
        assert "/serp/overview" in url
        assert params.get("query") == "best coffee"
        return _ok_response({"positions": []})

    monkeypatch.setattr(client.session, "request", fake_request)

    resp = client.get_serp_overview(query="best coffee")
    assert resp["ok"]


def test_limits_and_usage(monkeypatch):
    client = AhrefsClient()

    def fake_request(method, url, headers=None, params=None, json=None, timeout=None):
        assert method == "GET"
        assert "/subscription/limits-and-usage" in url
        return _ok_response({"remaining": 999})

    monkeypatch.setattr(client.session, "request", fake_request)

    resp = client.get_limits_and_usage()
    assert resp["data"]["remaining"] == 999
