from __future__ import annotations

from backend.app.core.landing_page.ahrefs import AhrefsClient
from ._requests import (
    DomainMetricsRequest,
    BacklinksRequest,
    ReferringDomainsRequest,
    OrganicKeywordsRequest,
    PagesRequest,
    DomainRatingRequest,
    BacklinksStatsRequest,
    OutlinksStatsRequest,
    MetricsRequest,
    RefdomainsHistoryRequest,
    DomainRatingHistoryRequest,
    UrlRatingHistoryRequest,
    PagesHistoryRequest,
    MetricsHistoryRequest,
    KeywordsHistoryRequest,
    MetricsByCountryRequest,
    PagesByTrafficRequest,
    TotalSearchVolumeHistoryRequest,
    RefdomainsRequest,
    AnchorsRequest,
    OrganicCompetitorsRequest,
    TopPagesRequest,
    PaidPagesRequest,
    BestByExternalLinksRequest,
    BestByInternalLinksRequest,
    LinkedDomainsRequest,
    OutgoingExternalAnchorsRequest,
    OutgoingInternalAnchorsRequest,
)

# Import category-specific handlers to keep this module lean
from .backlinks_handlers import (
    handle_backlinks,
    handle_broken_backlinks,
    handle_refdomains,
    handle_anchors,
)
from .organic_handlers import (
    handle_organic_keywords,
    handle_organic_competitors,
    handle_top_pages,
)
from .paid_handlers import handle_paid_pages
from .pages_handlers import (
    handle_best_by_external_links,
    handle_best_by_internal_links,
)
from .outgoing_handlers import (
    handle_linked_domains,
    handle_outgoing_external_anchors,
    handle_outgoing_internal_anchors,
)
from .keywords_explorer_handlers import (
    handle_keywords_overview,
    handle_keywords_volume_history,
    handle_keywords_volume_by_country,
    handle_matching_terms,
    handle_related_terms,
    handle_search_suggestions,
)
from .rank_tracker_handlers import handle_rank_tracker_overview
from .overview_handlers import (
    handle_overview,
    handle_competitors_overview,
    handle_competitors_pages,
)
from .serp_handlers import handle_serp_overview
from .batch_handlers import handle_batch_analysis
from .subscription_handlers import handle_limits_and_usage
from .management_handlers import (
    handle_projects,
    handle_create_project,
    handle_keywords_get,
    handle_keywords_put,
    handle_keywords_delete,
    handle_competitors_get,
    handle_competitors_add,
    handle_competitors_delete,
    handle_locations_and_languages,
    handle_keyword_lists,
)
from .public_handlers import (
    handle_crawler_ip_addresses,
    handle_crawler_ip_ranges,
)


def handle_domain_metrics(payload: DomainMetricsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_domain_metrics(domain=payload.domain, metrics=payload.metrics, **extra)


def handle_referring_domains(payload: ReferringDomainsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_referring_domains(target=payload.target, limit=payload.limit, offset=payload.offset, **extra)


def handle_pages(payload: PagesRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_pages(target=payload.target, limit=payload.limit, offset=payload.offset, **extra)


# ----------------------------------
# Site Explorer operation handlers
# ----------------------------------
def handle_domain_rating(payload: DomainRatingRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_domain_rating(domain=payload.domain, **extra)


def handle_backlinks_stats(payload: BacklinksStatsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_backlinks_stats(target=payload.target, **extra)


def handle_outlinks_stats(payload: OutlinksStatsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_outlinks_stats(target=payload.target, **extra)


def handle_metrics(payload: MetricsRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_metrics(target=payload.target, **extra)


def handle_refdomains_history(payload: RefdomainsHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_refdomains_history(target=payload.target, **extra)


def handle_domain_rating_history(payload: DomainRatingHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_domain_rating_history(target=payload.target, **extra)


def handle_url_rating_history(payload: UrlRatingHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_url_rating_history(url=payload.url, **extra)


def handle_pages_history(payload: PagesHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_pages_history(target=payload.target, **extra)


def handle_metrics_history(payload: MetricsHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_metrics_history(target=payload.target, **extra)


def handle_keywords_history(payload: KeywordsHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_keywords_history(target=payload.target, **extra)


def handle_metrics_by_country(payload: MetricsByCountryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_metrics_by_country(target=payload.target, country=payload.country, **extra)


def handle_pages_by_traffic(payload: PagesByTrafficRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_pages_by_traffic(target=payload.target, **extra)


def handle_total_search_volume_history(payload: TotalSearchVolumeHistoryRequest, client: AhrefsClient):
    extra = payload.extra or {}
    return client.get_total_search_volume_history(target=payload.target, **extra)


# ----------------------------------
# Category handlers
# ----------------------------------
