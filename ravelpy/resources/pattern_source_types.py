"""Sub-client for Ravelry Pattern Source Types reference endpoint."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternSourceTypesResponse


class PatternSourceTypes(Resource):
    """Wraps the pattern source types list endpoint.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    async def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all pattern source types (``GET /pattern_source_types/list.json``)."""
        return await self._get("/pattern_source_types/list.json", etag=etag, model=PatternSourceTypesResponse)
