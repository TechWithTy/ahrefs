from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from .client import AhrefsClient


class AhrefsSettings:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: str = "https://api.ahrefs.com",
        timeout_s: int = 30,
        rate_limit_per_min: int = 60,
        auth_in_header: bool = True,  # if False, use query param
        api_key_header: str = "Authorization",  # used when auth_in_header=True
        api_key_prefix: str = "Bearer ",  # e.g., "Bearer " or "Ahrefs ", can be empty
        api_key_query_param: str = "token",  # used when auth_in_header=False
    ) -> None:
        self.api_key = api_key or os.getenv("AHREFS_API_KEY")
        self.base_url = os.getenv("AHREFS_BASE_URL", base_url)
        self.timeout_s = int(os.getenv("AHREFS_TIMEOUT_S", str(timeout_s)))
        self.rate_limit_per_min = int(os.getenv("AHREFS_RATE_LIMIT_PER_MIN", str(rate_limit_per_min)))
        self.auth_in_header = (os.getenv("AHREFS_AUTH_IN_HEADER", str(int(auth_in_header))) in {"1", "true", "True"})
        self.api_key_header = os.getenv("AHREFS_API_KEY_HEADER", api_key_header)
        self.api_key_prefix = os.getenv("AHREFS_API_KEY_PREFIX", api_key_prefix)
        self.api_key_query_param = os.getenv("AHREFS_API_KEY_QUERY_PARAM", api_key_query_param)


@lru_cache(maxsize=1)
def get_settings() -> AhrefsSettings:
    return AhrefsSettings()


def get_client() -> AhrefsClient:
    s = get_settings()
    return AhrefsClient(
        api_key=s.api_key,
        base_url=s.base_url,
        timeout_s=s.timeout_s,
        rate_limit_per_min=s.rate_limit_per_min,
        auth_in_header=s.auth_in_header,
        api_key_header=s.api_key_header,
        api_key_prefix=s.api_key_prefix,
        api_key_query_param=s.api_key_query_param,
    )
