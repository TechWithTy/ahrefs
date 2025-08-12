from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel


class GenericResponse(BaseModel):
    ok: bool
    data: Optional[Any] = None
    error: Optional[str] = None
