from ._requests import LinkedDomainsRequest, OutgoingExternalAnchorsRequest, OutgoingInternalAnchorsRequest
from ..client import AhrefsClient


def handle_linked_domains(payload: LinkedDomainsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_linked_domains(target=payload.target, **params)


def handle_outgoing_external_anchors(payload: OutgoingExternalAnchorsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_outgoing_external_anchors(target=payload.target, **params)


def handle_outgoing_internal_anchors(payload: OutgoingInternalAnchorsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_outgoing_internal_anchors(target=payload.target, **params)
