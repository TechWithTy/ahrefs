from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict


class DomainMetricsParams(TypedDict, total=False):
    domain: str
    metrics: List[str]


class BacklinksParams(TypedDict, total=False):
    target: str
    limit: int
    offset: int


class ReferringDomainsParams(TypedDict, total=False):
    target: str
    limit: int
    offset: int


class OrganicKeywordsParams(TypedDict, total=False):
    target: str
    country: Optional[str]
    limit: int
    offset: int


class PagesParams(TypedDict, total=False):
    target: str
    limit: int
    offset: int


JsonDict = Dict[str, Any]
