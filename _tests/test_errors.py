from types import SimpleNamespace
import pytest

from backend.app.core.landing_page.ahrefs.client import AhrefsClient
from backend.app.core.landing_page.ahrefs.errors import (
    AhrefsAuthError,
    AhrefsRateLimitError,
    AhrefsAPIError,
)


def _resp(status: int, body: dict | None = None):
    return SimpleNamespace(
        status_code=status,
        text="{}" if body is None else str(body),
        json=(lambda: body) if body is not None else (lambda: {}),
    )


def test_auth_error_raises(monkeypatch):
    client = AhrefsClient()
    monkeypatch.setattr(client.session, "request", lambda *a, **k: _resp(401, {"message": "unauthorized"}))
    with pytest.raises(AhrefsAuthError):
        client.get_domain_rating(target="example.com")


def test_rate_limit_error_raises(monkeypatch):
    client = AhrefsClient()
    monkeypatch.setattr(client.session, "request", lambda *a, **k: _resp(429, {"message": "too many"}))
    with pytest.raises(AhrefsRateLimitError):
        client.get_domain_rating(target="example.com")


def test_server_error_maps(monkeypatch):
    client = AhrefsClient()
    monkeypatch.setattr(client.session, "request", lambda *a, **k: _resp(500, {"error": "boom"}))
    with pytest.raises(AhrefsAPIError):
        client.get_domain_rating(target="example.com")
