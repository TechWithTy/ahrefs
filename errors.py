from __future__ import annotations

from typing import Any, Optional


class AhrefsError(Exception):
    """Base error for Ahrefs SDK."""


class AhrefsAuthError(AhrefsError):
    def __init__(self, message: str = "Unauthorized or forbidden", *, status_code: Optional[int] = None, response_text: Optional[str] = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class AhrefsRateLimitError(AhrefsError):
    def __init__(self, message: str = "Rate limit exceeded", *, status_code: Optional[int] = None, response_text: Optional[str] = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class AhrefsAPIError(AhrefsError):
    def __init__(self, message: str, *, status_code: Optional[int] = None, response_text: Optional[str] = None, payload: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text
        self.payload = payload or {}
