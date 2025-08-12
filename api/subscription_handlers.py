from ._requests import LimitsAndUsageRequest
from ..client import AhrefsClient


def handle_limits_and_usage(payload: LimitsAndUsageRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_limits_and_usage(**extra)
