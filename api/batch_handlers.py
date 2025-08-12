from ._requests import BatchAnalysisRequest
from ..client import AhrefsClient


def handle_batch_analysis(payload: BatchAnalysisRequest, client: AhrefsClient):
    extra = payload.extra or {}
    # Allow extra to pass through to client.post_batch_analysis (e.g., path override or additional JSON fields)
    return client.post_batch_analysis(items=payload.items, **extra)
