from ._requests import BacklinksRequest, RefdomainsRequest, AnchorsRequest
from ..client import AhrefsClient


def handle_backlinks(payload: BacklinksRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_backlinks(target=payload.target, limit=payload.limit, offset=payload.offset, **extra)


def handle_broken_backlinks(payload: BacklinksRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_broken_backlinks(target=payload.target, **params)


def handle_refdomains(payload: RefdomainsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_refdomains(target=payload.target, **params)


def handle_anchors(payload: AnchorsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_anchors(target=payload.target, **params)
