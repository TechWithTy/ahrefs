from ._requests import (
    KeywordsOverviewRequest,
    KeywordsVolumeHistoryRequest,
    KeywordsVolumeByCountryRequest,
    MatchingTermsRequest,
    RelatedTermsRequest,
    SearchSuggestionsRequest,
)
from ..client import AhrefsClient


def handle_keywords_overview(payload: KeywordsOverviewRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_keywords_overview(query=payload.query, **extra)


def handle_keywords_volume_history(payload: KeywordsVolumeHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_keywords_volume_history(query=payload.query, **extra)


def handle_keywords_volume_by_country(payload: KeywordsVolumeByCountryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_keywords_volume_by_country(query=payload.query, country=payload.country, **extra)


def handle_matching_terms(payload: MatchingTermsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_matching_terms(query=payload.query, **params)


def handle_related_terms(payload: RelatedTermsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_related_terms(query=payload.query, **params)


def handle_search_suggestions(payload: SearchSuggestionsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    params = {"limit": payload.limit, "offset": payload.offset}
    params.update(extra)
    return client.get_search_suggestions(query=payload.query, **params)
