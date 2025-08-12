from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.core.landing_page.ahrefs import (
    AhrefsAPIError,
    AhrefsAuthError,
    AhrefsRateLimitError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AhrefsAuthError)
    async def handle_auth_error(_: Request, exc: AhrefsAuthError):
        return JSONResponse(
            status_code=exc.status_code or 401,
            content={
                "error": "ahrefs_auth_error",
                "message": str(exc),
            },
        )

    @app.exception_handler(AhrefsRateLimitError)
    async def handle_rl_error(_: Request, exc: AhrefsRateLimitError):
        return JSONResponse(
            status_code=429,
            content={
                "error": "ahrefs_rate_limited",
                "message": str(exc),
            },
        )

    @app.exception_handler(AhrefsAPIError)
    async def handle_api_error(_: Request, exc: AhrefsAPIError):
        return JSONResponse(
            status_code=getattr(exc, "status_code", None) or 500,
            content={
                "error": "ahrefs_api_error",
                "message": str(exc),
                "details": getattr(exc, "payload", None),
            },
        )
