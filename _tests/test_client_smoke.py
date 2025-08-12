from types import SimpleNamespace

from backend.app.core.landing_page.ahrefs.client import AhrefsClient


def test_get_crawler_ip_addresses(monkeypatch):
    client = AhrefsClient()

    captured = {}

    def fake_request(method, url, headers=None, params=None, json=None, timeout=None):
        captured.update({
            "method": method,
            "url": url,
            "headers": headers or {},
            "params": params or {},
            "json": json,
            "timeout": timeout,
        })
        return SimpleNamespace(
            status_code=200,
            text="{}",
            json=lambda: {"ok": True, "data": {"ips": ["1.2.3.4"]}},
        )

    monkeypatch.setattr(client.session, "request", fake_request)

    resp = client.get_crawler_ip_addresses()

    assert captured["method"] == "GET"
    assert "/public/crawler-ip-addresses" in captured["url"]
    assert resp["ok"] is True
    assert "data" in resp
