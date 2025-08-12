from ._requests import BestByExternalLinksRequest, BestByInternalLinksRequest
from ..client import AhrefsClient


def handle_best_by_external_links(payload: BestByExternalLinksRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_best_by_external_links(target=payload.target, **params)


def handle_best_by_internal_links(payload: BestByInternalLinksRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_best_by_internal_links(target=payload.target, **params)
