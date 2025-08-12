from ._requests import SerpOverviewRequest
from ..client import AhrefsClient


def handle_serp_overview(payload: SerpOverviewRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_serp_overview(query=payload.query, **extra)
