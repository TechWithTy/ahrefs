# Ahrefs Internal SDK + FastAPI API

Typed, production-ready internal Python SDK and FastAPI API for Ahrefs. Includes retries, rate limiting, clear error handling, and centralized routes with category-based handlers.

- SDK path: `backend/app/core/landing_page/ahrefs/`
- API path: `backend/app/core/landing_page/ahrefs/api/`
- Public endpoints covered: Site Explorer groups, Keywords Explorer, Rank Tracker, Overview (incl. competitors pages), SERP Overview, Batch Analysis, Subscription, Management (projects/keywords/competitors/locations-languages/keyword lists), and Public Crawler IPs.

## Features

- Typed request models and handler functions per category
- Centralized FastAPI routes with DI-based client access
- Configurable auth via header or query param
- Retries with backoff and robust error mapping
- Lightweight token/leaky-bucket rate limiter

## Environment Variables

Place in `.env` or environment:

- `AHREFS_API_KEY` (required)
- `AHREFS_BASE_URL` (default: Ahrefs API base or custom)
- `AHREFS_TIMEOUT_S` (default: `10`)
- `AHREFS_RATE_LIMIT_PER_MIN` (default: `120`)

Optional (if supported in your `config.py`):
- `AHREFS_AUTH_MODE` = `header` | `query` (default: `header`)

## SDK Usage

```python
from backend.app.core.landing_page.ahrefs.client import AhrefsClient

client = AhrefsClient()

# Site overview
ov = client.get_overview(target="example.com")
print(ov)

# Keywords Explorer
kw = client.get_keywords_overview(query="coffee")
print(kw)

# Management: create project
proj = client.create_project(name="Demo", target="example.com")
print(proj)

# Public: crawler IPs
ips = client.get_crawler_ip_addresses()
print(ips)
```

## FastAPI Routes

Router is registered under prefix `/ahrefs`.

Examples:
- `GET /ahrefs/overview/overview?target=example.com`
- `GET /ahrefs/serp/overview?query=best%20coffee`
- `POST /ahrefs/batch-analysis` body: `{ "items": ["a.com", "b.com"] }`
- `GET /ahrefs/subscription/limits-and-usage`
- `GET /ahrefs/management/projects`
- `POST /ahrefs/management/projects` body: `{ "name": "Demo", "target": "example.com" }`
- `GET /ahrefs/public/crawler-ip-addresses`
- `GET /ahrefs/public/crawler-ip-ranges`

All endpoints return a `GenericResponse` shape:

```json
{
  "ok": true,
  "data": { /* provider response payload */ }
}
```

## Handlers Organization

Category-specific handlers under `api/`:

- `backlinks_handlers.py`
- `organic_handlers.py`
- `paid_handlers.py`
- `pages_handlers.py`
- `outgoing_handlers.py`
- `keywords_explorer_handlers.py`
- `rank_tracker_handlers.py`
- `overview_handlers.py`
- `serp_handlers.py`
- `batch_handlers.py`
- `subscription_handlers.py`
- `management_handlers.py`
- `public_handlers.py`

All imported by `api/handlers.py`. Routes defined centrally in `api/routes.py`.

## Errors

Custom exceptions in `errors.py`:

- `AhrefsAuthError` → 401
- `AhrefsRateLimitError` → 429
- `AhrefsAPIError` → 4xx/5xx mapping

## Rate Limiting

Configured via `AHREFS_RATE_LIMIT_PER_MIN`. The SDK acquires a token per request and respects backpressure.

## Testing

Tests live in `ahrefs/_tests/`.

Run tests (PowerShell from repo root or tests dir):

```bash
pytest backend/app/core/landing_page/ahrefs/_tests -q
```

Coverage is configured in `ahrefs/_tests/pytest.ini` to target this module.

Included tests:
- Client: smoke + representative endpoint calls with monkeypatched HTTP
- API routes: FastAPI `TestClient` with DI override for the SDK
- Errors: exception mapping (401/429/5xx)

Add-on ideas:
- Config parsing and auth mode
- Rate limiter timing and refill
- More endpoint variations and edge cases

## Security Notes

- Never commit real API keys. Use `.env` and secret stores.
- Prefer header-based auth unless query-mode is required.

## Limitations

- Response models are currently generic (`GenericResponse`). For stricter typing, add per-endpoint response models in `api/_responses.py` and update routes.

## Changelog (high level)

- Modular handlers per category and centralized routes
- Implemented Site Explorer, Keywords Explorer, Rank Tracker, Overview, SERP, Batch, Subscription, Management, and Public Crawler endpoints
- Added test suite with coverage config
