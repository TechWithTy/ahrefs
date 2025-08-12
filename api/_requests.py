from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DomainMetricsRequest(BaseModel):
    domain: str
    metrics: Optional[List[str]] = None
    extra: Dict[str, Any] | None = Field(default=None, description="Additional provider-specific params")


class BacklinksRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class ReferringDomainsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class OrganicKeywordsRequest(BaseModel):
    target: str
    country: Optional[str] = None
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class PagesRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


# -----------------------------
# Site Explorer specific models
# -----------------------------
class DomainRatingRequest(BaseModel):
    domain: str
    extra: Dict[str, Any] | None = None


class BacklinksStatsRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class OutlinksStatsRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class MetricsRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class RefdomainsHistoryRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class DomainRatingHistoryRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class UrlRatingHistoryRequest(BaseModel):
    url: str
    extra: Dict[str, Any] | None = None


class PagesHistoryRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class MetricsHistoryRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class KeywordsHistoryRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class MetricsByCountryRequest(BaseModel):
    target: str
    country: Optional[str] = None
    extra: Dict[str, Any] | None = None


class PagesByTrafficRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class TotalSearchVolumeHistoryRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


# -----------------------------
# Category models
# -----------------------------
class RefdomainsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class AnchorsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class OrganicCompetitorsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class TopPagesRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class PaidPagesRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class BestByExternalLinksRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class BestByInternalLinksRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class LinkedDomainsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class OutgoingExternalAnchorsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class OutgoingInternalAnchorsRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


# -----------------------------
# Keywords Explorer models
# -----------------------------
class KeywordsOverviewRequest(BaseModel):
    query: str
    extra: Dict[str, Any] | None = None


class KeywordsVolumeHistoryRequest(BaseModel):
    query: str
    extra: Dict[str, Any] | None = None


class KeywordsVolumeByCountryRequest(BaseModel):
    query: str
    country: str | None = None
    extra: Dict[str, Any] | None = None


class MatchingTermsRequest(BaseModel):
    query: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class RelatedTermsRequest(BaseModel):
    query: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


class SearchSuggestionsRequest(BaseModel):
    query: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


# -----------------------------
# Rank Tracker models
# -----------------------------
class RankTrackerOverviewRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


# -----------------------------
# Overview group models
# -----------------------------
class OverviewRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class CompetitorsOverviewRequest(BaseModel):
    target: str
    extra: Dict[str, Any] | None = None


class CompetitorsPagesRequest(BaseModel):
    target: str
    limit: int = 100
    offset: int = 0
    extra: Dict[str, Any] | None = None


# -----------------------------
# SERP Overview models
# -----------------------------
class SerpOverviewRequest(BaseModel):
    query: str
    extra: Dict[str, Any] | None = None


# -----------------------------
# Batch Analysis models
# -----------------------------
class BatchAnalysisRequest(BaseModel):
    items: list[str]
    extra: Dict[str, Any] | None = None


# -----------------------------
# Subscription Information models
# -----------------------------
class LimitsAndUsageRequest(BaseModel):
    extra: Dict[str, Any] | None = None


# -----------------------------
# Management models
# -----------------------------
class ProjectsRequest(BaseModel):
    extra: Dict[str, Any] | None = None


class CreateProjectRequest(BaseModel):
    name: str
    target: str
    extra: Dict[str, Any] | None = None


class KeywordsGetRequest(BaseModel):
    project_id: str
    extra: Dict[str, Any] | None = None


class KeywordsPutRequest(BaseModel):
    project_id: str
    keywords: list[str]
    extra: Dict[str, Any] | None = None


class KeywordsDeleteRequest(BaseModel):
    project_id: str
    keywords: list[str]
    extra: Dict[str, Any] | None = None


class CompetitorsGetRequest(BaseModel):
    project_id: str
    extra: Dict[str, Any] | None = None


class CompetitorsAddRequest(BaseModel):
    project_id: str
    competitors: list[str]
    extra: Dict[str, Any] | None = None


class CompetitorsDeleteRequest(BaseModel):
    project_id: str
    competitors: list[str]
    extra: Dict[str, Any] | None = None


class LocationsAndLanguagesRequest(BaseModel):
    extra: Dict[str, Any] | None = None


class KeywordListsRequest(BaseModel):
    project_id: str | None = None
    extra: Dict[str, Any] | None = None


# -----------------------------
# Public models
# -----------------------------
class CrawlerIpAddressesRequest(BaseModel):
    extra: Dict[str, Any] | None = None


class CrawlerIpRangesRequest(BaseModel):
    extra: Dict[str, Any] | None = None
