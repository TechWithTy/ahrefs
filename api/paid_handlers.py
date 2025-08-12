from ._requests import PaidPagesRequest
from ..client import AhrefsClient


def handle_paid_pages(payload: PaidPagesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_paid_pages(target=payload.target, **params)
