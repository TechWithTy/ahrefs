from __future__ import annotations

from typing import Optional
from fastapi import Header, HTTPException, status

from backend.app.core.landing_page.ahrefs import AhrefsClient
from backend.app.core.landing_page.ahrefs.config import get_client as get_default_client


def get_client(authorization: Optional[str] = Header(None)) -> AhrefsClient:
    """
    Provide an AhrefsClient.
    - If Authorization: Bearer <token> is provided, build a per-request client using that token.
    - Otherwise, return the default client configured from env via config.get_client().
    """
    if not authorization:
        return get_default_client()

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format")
    token = parts[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Empty bearer token")

    # Use header-based auth by default for bearer tokens
    return AhrefsClient(api_key=token, auth_in_header=True, api_key_header="Authorization", api_key_prefix="Bearer ")
