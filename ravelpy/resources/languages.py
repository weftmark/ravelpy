"""Sub-client for Ravelry Languages reference endpoint."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import LanguagesResponse


class Languages(Resource):
    """Wraps the languages list endpoint.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    async def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all supported languages (``GET /languages/list.json``)."""
        return await self._get("/languages/list.json", etag=etag, model=LanguagesResponse)
