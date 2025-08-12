from ._requests import OrganicKeywordsRequest, OrganicCompetitorsRequest, TopPagesRequest
from ..client import AhrefsClient


def handle_organic_keywords(payload: OrganicKeywordsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_organic_keywords(
        target=payload.target,
        country=payload.country,
        limit=payload.limit,
        offset=payload.offset,
        **extra,
    )


def handle_organic_competitors(payload: OrganicCompetitorsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_organic_competitors(target=payload.target, **params)


def handle_top_pages(payload: TopPagesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_top_pages(target=payload.target, **params)
