from ._requests import RankTrackerOverviewRequest
from ..client import AhrefsClient


def handle_rank_tracker_overview(payload: RankTrackerOverviewRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_rank_tracker_overview(target=payload.target, **extra)
