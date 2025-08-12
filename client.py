from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import requests
from requests import Session, Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .errors import AhrefsAPIError, AhrefsAuthError, AhrefsRateLimitError
from .rate_limiter import RateLimiter

DEFAULT_BASE_URL = "https://api.ahrefs.com"


class AhrefsClient:
    """
    Internal SDK client for Ahrefs API.

    Authentication is flexible:
    - Header-based: {api_key_header: f"{api_key_prefix}{api_key}"}
    - Query param-based: {api_key_query_param: api_key}

    Configure using env vars (see config.py) or pass directly to constructor.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout_s: int = 30,
        rate_limit_per_min: int = 60,
        auth_in_header: bool = True,
        api_key_header: str = "Authorization",
        api_key_prefix: str = "Bearer ",
        api_key_query_param: str = "token",
        session: Optional[Session] = None,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> None:
        self.api_key = api_key or os.getenv("AHREFS_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.auth_in_header = auth_in_header
        self.api_key_header = api_key_header
        self.api_key_prefix = api_key_prefix
        self.api_key_query_param = api_key_query_param

        self.session = session or requests.Session()
        retry = Retry(
            total=max_retries,
            read=max_retries,
            connect=max_retries,
            status=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST"),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Token bucket per minute
        self._rate_limiter = RateLimiter(capacity=max(rate_limit_per_min, 1), refill_window_s=60)

    # ---------------
    # Public endpoints
    # ---------------
    def get_domain_metrics(self, *, domain: str, metrics: Optional[List[str]] = None, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"domain": domain}
        if metrics:
            params["metrics"] = ",".join(metrics)
        params.update(extra)
        return self._request("GET", "/v1/domain/metrics", params=params)

    def get_backlinks(self, *, target: str, limit: int = 100, offset: int = 0, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target, "limit": limit, "offset": offset}
        params.update(extra)
        return self._request("GET", "/v1/backlinks", params=params)

    def get_referring_domains(self, *, target: str, limit: int = 100, offset: int = 0, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target, "limit": limit, "offset": offset}
        params.update(extra)
        return self._request("GET", "/v1/referring-domains", params=params)

    def get_organic_keywords(self, *, target: str, country: Optional[str] = None, limit: int = 100, offset: int = 0, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target, "limit": limit, "offset": offset}
        if country:
            params["country"] = country
        params.update(extra)
        return self._request("GET", "/v1/organic-keywords", params=params)

    def get_pages(self, *, target: str, limit: int = 100, offset: int = 0, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target, "limit": limit, "offset": offset}
        params.update(extra)
        return self._request("GET", "/v1/pages", params=params)

    def batch(self, requests_: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # naive convenience: execute sequentially
        results: List[Dict[str, Any]] = []
        for req in requests_:
            method = req.get("method", "GET").upper()
            path = req.get("path", "")
            params = req.get("params") or {}
            json = req.get("json")
            results.append(self._request(method, path, params=params, json=json))
        return results

    # -----------------------------
    # Site Explorer convenience ops
    # -----------------------------
    def _get_site_explorer(self, op: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generic Site Explorer GET. By default, calls `/site-explorer/{op}`.
        You can override the vendor path by passing `path` inside params (will be popped).
        """
        params = dict(params) if params else {}
        # allow override of default path
        path = params.pop("path", f"/site-explorer/{op}")
        return self._request("GET", path, params=params)

    def get_domain_rating(self, *, domain: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"domain": domain}
        params.update(extra)
        return self._get_site_explorer("domain-rating", params)

    def get_backlinks_stats(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("backlinks-stats", params)

    def get_outlinks_stats(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("outlinks-stats", params)

    def get_metrics(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("metrics", params)

    def get_refdomains_history(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("refdomains-history", params)

    def get_domain_rating_history(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("domain-rating-history", params)

    def get_url_rating_history(self, *, url: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"url": url}
        params.update(extra)
        return self._get_site_explorer("url-rating-history", params)

    def get_pages_history(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("pages-history", params)

    def get_metrics_history(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("metrics-history", params)

    def get_keywords_history(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("keywords-history", params)

    def get_metrics_by_country(self, *, target: str, country: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        if country:
            params["country"] = country
        params.update(extra)
        return self._get_site_explorer("metrics-by-country", params)

    def get_pages_by_traffic(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("pages-by-traffic", params)

    def get_total_search_volume_history(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_site_explorer("total-search-volume-history", params)

    # ------------------
    # Internal helpers
    # ------------------
    def _auth_headers_and_params(self) -> tuple[Dict[str, str], Dict[str, Any]]:
        if not self.api_key:
            raise AhrefsAuthError("API key missing. Set AHREFS_API_KEY or pass api_key.")
        if self.auth_in_header:
            return ({self.api_key_header: f"{self.api_key_prefix}{self.api_key}"}, {})
        else:
            return ({}, {self.api_key_query_param: self.api_key})

    def _handle_response(self, resp: Response) -> Dict[str, Any]:
        if resp.status_code == 429:
            raise AhrefsRateLimitError("Rate limit exceeded", status_code=resp.status_code, response_text=resp.text)
        try:
            data = resp.json() if resp.content else {}
        except ValueError:
            data = {}
        if 200 <= resp.status_code < 300:
            return data
        if resp.status_code in (401, 403):
            raise AhrefsAuthError("Unauthorized or forbidden", status_code=resp.status_code, response_text=resp.text)
        raise AhrefsAPIError(
            f"HTTP {resp.status_code}", status_code=resp.status_code, response_text=resp.text, payload=data
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._rate_limiter.acquire()
        headers_auth, params_auth = self._auth_headers_and_params()

        url = f"{self.base_url}{path}"
        merged_params: Dict[str, Any] = {}
        if params:
            merged_params.update(params)
        merged_params.update(params_auth)

        resp = self.session.request(
            method=method.upper(),
            url=url,
            params=merged_params if merged_params else None,
            json=json,
            headers=headers_auth if headers_auth else None,
            timeout=self.timeout_s,
        )
        return self._handle_response(resp)

    # -----------------------------
    # Category helpers and methods
    # -----------------------------
    def _get_category(self, category: str, op: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generic category GET with default path `/{category}/{op}`.
        Overridable by passing `path` in params.
        """
        params = dict(params) if params else {}
        path = params.pop("path", f"/{category}/{op}")
        return self._request("GET", path, params=params)

    # Backlinks
    def get_broken_backlinks(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("backlinks", "broken", params)

    def get_refdomains(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("backlinks", "refdomains", params)

    def get_anchors(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("backlinks", "anchors", params)

    # Organic search
    def get_organic_competitors(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("organic", "competitors", params)

    def get_top_pages(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("organic", "top-pages", params)

    # Paid search
    def get_paid_pages(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("paid", "pages", params)

    # Pages
    def get_best_by_external_links(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("pages", "best-by-external-links", params)

    def get_best_by_internal_links(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("pages", "best-by-internal-links", params)

    # Outgoing links
    def get_linked_domains(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("outgoing", "linked-domains", params)

    def get_outgoing_external_anchors(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("outgoing", "external-anchors", params)

    def get_outgoing_internal_anchors(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("outgoing", "internal-anchors", params)

    # Keywords Explorer
    def get_keywords_overview(self, *, query: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        params.update(extra)
        return self._get_category("keywords-explorer", "overview", params)

    def get_keywords_volume_history(self, *, query: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        params.update(extra)
        return self._get_category("keywords-explorer", "volume-history", params)

    def get_keywords_volume_by_country(self, *, query: str, country: str | None = None, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        if country:
            params["country"] = country
        params.update(extra)
        return self._get_category("keywords-explorer", "volume-by-country", params)

    def get_matching_terms(self, *, query: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        params.update(extra)
        return self._get_category("keywords-explorer", "matching-terms", params)

    def get_related_terms(self, *, query: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        params.update(extra)
        return self._get_category("keywords-explorer", "related-terms", params)

    def get_search_suggestions(self, *, query: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        params.update(extra)
        return self._get_category("keywords-explorer", "search-suggestions", params)

    # Rank Tracker
    def get_rank_tracker_overview(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("rank-tracker", "overview", params)

    # Overview group
    def get_overview(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("overview", "overview", params)

    def get_competitors_overview(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("overview", "competitors-overview", params)

    def get_competitors_pages(self, *, target: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"target": target}
        params.update(extra)
        return self._get_category("overview", "competitors-pages", params)

    # SERP Overview
    def get_serp_overview(self, *, query: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"query": query}
        params.update(extra)
        return self._get_category("serp", "overview", params)

    # Batch Analysis (POST)
    def post_batch_analysis(self, *, items: list[str], **extra: Any) -> Dict[str, Any]:
        data: Dict[str, Any] = {"items": items}
        # Allow overriding path via extra.path
        path = (extra or {}).pop("path", "/batch-analysis")
        # Remaining extras treated as additional JSON fields
        if extra:
            data.update(extra)
        headers, params = self._auth_headers_and_params()
        if self._rate_limiter:
            self._rate_limiter.acquire()
        resp = self.session.request(
            "POST",
            url=f"{self.base_url}{path}",
            headers=headers,
            params=params,
            json=data,
            timeout=self.timeout_s,
        )
        return self._handle_response(resp)

    # Subscription Information
    def get_limits_and_usage(self, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        params.update(extra or {})
        return self._get_category("subscription", "limits-and-usage", params)

    # -----------------------------
    # Management
    # -----------------------------
    # Projects
    def get_projects(self, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        params.update(extra or {})
        return self._get_category("management", "projects", params)

    def create_project(self, *, name: str, target: str, **extra: Any) -> Dict[str, Any]:
        data: Dict[str, Any] = {"name": name, "target": target}
        if extra:
            data.update(extra)
        return self._request("POST", "/management/projects", json=data)

    # Keywords
    def get_keywords(self, *, project_id: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"project_id": project_id}
        params.update(extra or {})
        return self._get_category("management", "keywords", params)

    def put_keywords(self, *, project_id: str, keywords: list[str], **extra: Any) -> Dict[str, Any]:
        data: Dict[str, Any] = {"project_id": project_id, "keywords": keywords}
        if extra:
            data.update(extra)
        return self._request("PUT", "/management/keywords", json=data)

    def delete_keywords(self, *, project_id: str, keywords: list[str], **extra: Any) -> Dict[str, Any]:
        data: Dict[str, Any] = {"project_id": project_id, "keywords": keywords}
        if extra:
            data.update(extra)
        # API uses PUT for delete per spec provided
        return self._request("PUT", "/management/keywords/delete", json=data)

    # Competitors
    def get_competitors(self, *, project_id: str, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {"project_id": project_id}
        params.update(extra or {})
        return self._get_category("management", "competitors", params)

    def add_competitors(self, *, project_id: str, competitors: list[str], **extra: Any) -> Dict[str, Any]:
        data: Dict[str, Any] = {"project_id": project_id, "competitors": competitors}
        if extra:
            data.update(extra)
        return self._request("POST", "/management/competitors", json=data)

    def delete_competitors(self, *, project_id: str, competitors: list[str], **extra: Any) -> Dict[str, Any]:
        data: Dict[str, Any] = {"project_id": project_id, "competitors": competitors}
        if extra:
            data.update(extra)
        return self._request("POST", "/management/competitors/delete", json=data)

    # Locations and languages
    def get_locations_and_languages(self, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        params.update(extra or {})
        return self._get_category("management", "locations-and-languages", params)

    # Keyword lists
    def get_keyword_lists(self, *, project_id: str | None = None, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if project_id:
            params["project_id"] = project_id
        params.update(extra or {})
        return self._get_category("management", "keyword-lists", params)

    # -----------------------------
    # Public
    # -----------------------------
    def get_crawler_ip_addresses(self, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        params.update(extra or {})
        return self._get_category("public", "crawler-ip-addresses", params)

    def get_crawler_ip_ranges(self, **extra: Any) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        params.update(extra or {})
        return self._get_category("public", "crawler-ip-ranges", params)
