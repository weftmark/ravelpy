"""Sub-client for Ravelry Pattern Categories reference endpoint."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternCategoriesResponse


class PatternCategories(Resource):
    """Wraps the pattern categories list endpoint."""

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all pattern categories (``GET /pattern_categories/list.json``)."""
        return self._get("/pattern_categories/list.json", etag=etag, model=PatternCategoriesResponse)
