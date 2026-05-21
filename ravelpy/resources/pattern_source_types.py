"""Sub-client for Ravelry Pattern Source Types reference endpoint."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternSourceTypesResponse


class PatternSourceTypes(Resource):
    """Wraps the pattern source types list endpoint."""

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all pattern source types (``GET /pattern_source_types/list.json``)."""
        return self._get("/pattern_source_types/list.json", etag=etag, model=PatternSourceTypesResponse)
