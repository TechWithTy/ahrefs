from ._requests import OverviewRequest, CompetitorsOverviewRequest, CompetitorsPagesRequest
from ..client import AhrefsClient


def handle_overview(payload: OverviewRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_overview(target=payload.target, **extra)


def handle_competitors_overview(payload: CompetitorsOverviewRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_competitors_overview(target=payload.target, **extra)


def handle_competitors_pages(payload: CompetitorsPagesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_competitors_pages(target=payload.target, **params)
