from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.app.core.landing_page.ahrefs import AhrefsClient
from .deps import get_client
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
    # New groups
    OverviewRequest,
    CompetitorsOverviewRequest,
    CompetitorsPagesRequest,
    SerpOverviewRequest,
    BatchAnalysisRequest,
    LimitsAndUsageRequest,
    # Management
    ProjectsRequest,
    CreateProjectRequest,
    KeywordsGetRequest,
    KeywordsPutRequest,
    KeywordsDeleteRequest,
    CompetitorsGetRequest,
    CompetitorsAddRequest,
    CompetitorsDeleteRequest,
    LocationsAndLanguagesRequest,
    KeywordListsRequest,
    CrawlerIpAddressesRequest,
    CrawlerIpRangesRequest,
)
from ._responses import GenericResponse
from .handlers import (
    handle_domain_metrics,
    handle_backlinks,
    handle_referring_domains,
    handle_organic_keywords,
    handle_pages,
    handle_domain_rating,
    handle_backlinks_stats,
    handle_outlinks_stats,
    handle_metrics,
    handle_refdomains_history,
    handle_domain_rating_history,
    handle_url_rating_history,
    handle_pages_history,
    handle_metrics_history,
    handle_keywords_history,
    handle_metrics_by_country,
    handle_pages_by_traffic,
    handle_total_search_volume_history,
    # New group handlers
    handle_overview,
    handle_competitors_overview,
    handle_competitors_pages,
    handle_serp_overview,
    handle_batch_analysis,
    handle_limits_and_usage,
    # Management
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
    handle_crawler_ip_addresses,
    handle_crawler_ip_ranges,
)

router = APIRouter(prefix="/ahrefs", tags=["ahrefs"])


@router.post("/domain/metrics", response_model=GenericResponse)
async def domain_metrics(payload: DomainMetricsRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_domain_metrics(payload, client))


@router.post("/backlinks", response_model=GenericResponse)
async def backlinks(payload: BacklinksRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_backlinks(payload, client))


@router.post("/referring-domains", response_model=GenericResponse)
async def referring_domains(payload: ReferringDomainsRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_referring_domains(payload, client))


@router.post("/organic-keywords", response_model=GenericResponse)
async def organic_keywords(payload: OrganicKeywordsRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_organic_keywords(payload, client))


@router.post("/pages", response_model=GenericResponse)
async def pages(payload: PagesRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_pages(payload, client))


# ----------------------------------
# Site Explorer operation routes
# ----------------------------------
@router.post("/site-explorer/domain-rating", response_model=GenericResponse)
async def domain_rating(payload: DomainRatingRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_domain_rating(payload, client))


@router.post("/site-explorer/backlinks-stats", response_model=GenericResponse)
async def backlinks_stats(payload: BacklinksStatsRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_backlinks_stats(payload, client))


@router.post("/site-explorer/outlinks-stats", response_model=GenericResponse)
async def outlinks_stats(payload: OutlinksStatsRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_outlinks_stats(payload, client))


@router.post("/site-explorer/metrics", response_model=GenericResponse)
async def metrics(payload: MetricsRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_metrics(payload, client))


@router.post("/site-explorer/refdomains-history", response_model=GenericResponse)
async def refdomains_history(payload: RefdomainsHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_refdomains_history(payload, client))


@router.post("/site-explorer/domain-rating-history", response_model=GenericResponse)
async def domain_rating_history(payload: DomainRatingHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_domain_rating_history(payload, client))


@router.post("/site-explorer/url-rating-history", response_model=GenericResponse)
async def url_rating_history(payload: UrlRatingHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_url_rating_history(payload, client))


@router.post("/site-explorer/pages-history", response_model=GenericResponse)
async def pages_history(payload: PagesHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_pages_history(payload, client))


@router.post("/site-explorer/metrics-history", response_model=GenericResponse)
async def metrics_history(payload: MetricsHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_metrics_history(payload, client))


@router.post("/site-explorer/keywords-history", response_model=GenericResponse)
async def keywords_history(payload: KeywordsHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_keywords_history(payload, client))


@router.post("/site-explorer/metrics-by-country", response_model=GenericResponse)
async def metrics_by_country(payload: MetricsByCountryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_metrics_by_country(payload, client))


@router.post("/site-explorer/pages-by-traffic", response_model=GenericResponse)
async def pages_by_traffic(payload: PagesByTrafficRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_pages_by_traffic(payload, client))


@router.post("/site-explorer/total-search-volume-history", response_model=GenericResponse)
async def total_search_volume_history(payload: TotalSearchVolumeHistoryRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_total_search_volume_history(payload, client))


# ----------------------------------
# Overview group (GET)
# ----------------------------------
@router.get("/overview/overview", response_model=GenericResponse)
async def overview(target: str, client: AhrefsClient = Depends(get_client)):
    payload = OverviewRequest(target=target)
    return GenericResponse(ok=True, data=handle_overview(payload, client))


@router.get("/overview/competitors-overview", response_model=GenericResponse)
async def competitors_overview(target: str, client: AhrefsClient = Depends(get_client)):
    payload = CompetitorsOverviewRequest(target=target)
    return GenericResponse(ok=True, data=handle_competitors_overview(payload, client))


@router.get("/overview/competitors-pages", response_model=GenericResponse)
async def competitors_pages(target: str, limit: int = 100, offset: int = 0, client: AhrefsClient = Depends(get_client)):
    payload = CompetitorsPagesRequest(target=target, limit=limit, offset=offset)
    return GenericResponse(ok=True, data=handle_competitors_pages(payload, client))


# ----------------------------------
# SERP Overview (GET)
# ----------------------------------
@router.get("/serp/overview", response_model=GenericResponse)
async def serp_overview(query: str, client: AhrefsClient = Depends(get_client)):
    payload = SerpOverviewRequest(query=query)
    return GenericResponse(ok=True, data=handle_serp_overview(payload, client))


# ----------------------------------
# Batch Analysis (POST)
# ----------------------------------
@router.post("/batch-analysis", response_model=GenericResponse)
async def batch_analysis(payload: BatchAnalysisRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_batch_analysis(payload, client))


# ----------------------------------
# Subscription Information (GET)
# ----------------------------------
@router.get("/subscription/limits-and-usage", response_model=GenericResponse)
async def limits_and_usage(client: AhrefsClient = Depends(get_client)):
    payload = LimitsAndUsageRequest()
    return GenericResponse(ok=True, data=handle_limits_and_usage(payload, client))


# ----------------------------------
# Management: Projects
# ----------------------------------
@router.get("/management/projects", response_model=GenericResponse)
async def projects(client: AhrefsClient = Depends(get_client)):
    payload = ProjectsRequest()
    return GenericResponse(ok=True, data=handle_projects(payload, client))


@router.post("/management/projects", response_model=GenericResponse)
async def create_project(payload: CreateProjectRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_create_project(payload, client))


# ----------------------------------
# Management: Keywords
# ----------------------------------
@router.get("/management/keywords", response_model=GenericResponse)
async def keywords_get(project_id: str, client: AhrefsClient = Depends(get_client)):
    payload = KeywordsGetRequest(project_id=project_id)
    return GenericResponse(ok=True, data=handle_keywords_get(payload, client))


@router.put("/management/keywords", response_model=GenericResponse)
async def keywords_put(payload: KeywordsPutRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_keywords_put(payload, client))


@router.put("/management/keywords/delete", response_model=GenericResponse)
async def keywords_delete(payload: KeywordsDeleteRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_keywords_delete(payload, client))


# ----------------------------------
# Management: Competitors
# ----------------------------------
@router.get("/management/competitors", response_model=GenericResponse)
async def competitors_get(project_id: str, client: AhrefsClient = Depends(get_client)):
    payload = CompetitorsGetRequest(project_id=project_id)
    return GenericResponse(ok=True, data=handle_competitors_get(payload, client))


@router.post("/management/competitors", response_model=GenericResponse)
async def competitors_add(payload: CompetitorsAddRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_competitors_add(payload, client))


@router.post("/management/competitors/delete", response_model=GenericResponse)
async def competitors_delete(payload: CompetitorsDeleteRequest, client: AhrefsClient = Depends(get_client)):
    return GenericResponse(ok=True, data=handle_competitors_delete(payload, client))


# ----------------------------------
# Management: Locations and languages
# ----------------------------------
@router.get("/management/locations-and-languages", response_model=GenericResponse)
async def locations_and_languages(client: AhrefsClient = Depends(get_client)):
    payload = LocationsAndLanguagesRequest()
    return GenericResponse(ok=True, data=handle_locations_and_languages(payload, client))


# ----------------------------------
# Management: Keyword lists
# ----------------------------------
@router.get("/management/keyword-lists", response_model=GenericResponse)
async def keyword_lists(project_id: str | None = None, client: AhrefsClient = Depends(get_client)):
    payload = KeywordListsRequest(project_id=project_id)
    return GenericResponse(ok=True, data=handle_keyword_lists(payload, client))


# ----------------------------------
# Public: Crawler
# ----------------------------------
@router.get("/public/crawler-ip-addresses", response_model=GenericResponse)
async def crawler_ip_addresses(client: AhrefsClient = Depends(get_client)):
    payload = CrawlerIpAddressesRequest()
    return GenericResponse(ok=True, data=handle_crawler_ip_addresses(payload, client))


@router.get("/public/crawler-ip-ranges", response_model=GenericResponse)
async def crawler_ip_ranges(client: AhrefsClient = Depends(get_client)):
    payload = CrawlerIpRangesRequest()
    return GenericResponse(ok=True, data=handle_crawler_ip_ranges(payload, client))
