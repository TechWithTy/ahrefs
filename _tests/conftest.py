import os
import types
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.core.landing_page.ahrefs.api.routes import router as ahrefs_router
from backend.app.core.landing_page.ahrefs.api import deps as api_deps
from backend.app.core.landing_page.ahrefs.client import AhrefsClient


@pytest.fixture(autouse=True)
def _env_defaults(monkeypatch):
    monkeypatch.setenv("AHREFS_API_KEY", os.getenv("AHREFS_API_KEY", "test_key"))
    monkeypatch.setenv("AHREFS_BASE_URL", os.getenv("AHREFS_BASE_URL", "https://example.local"))
    monkeypatch.setenv("AHREFS_TIMEOUT_S", os.getenv("AHREFS_TIMEOUT_S", "10"))
    monkeypatch.setenv("AHREFS_RATE_LIMIT_PER_MIN", os.getenv("AHREFS_RATE_LIMIT_PER_MIN", "120"))
    yield


@pytest.fixture()
def fake_client() -> AhrefsClient:
    # Real client, but we'll stub methods at test-time
    return AhrefsClient()


@pytest.fixture()
def app(fake_client: AhrefsClient):
    app = FastAPI()

    # Override dependency to return our fake_client
    def _override_get_client():
        return fake_client

    app.dependency_overrides[api_deps.get_client] = _override_get_client
    app.include_router(ahrefs_router)
    return app


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
