"""Sub-client for Ravelry Pattern Attributes API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import PatternAttributeGroupsResponse


class PatternAttributes(Resource):
    """Wraps the pattern attribute groups endpoint.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    def groups(self, etag: Optional[str] = None) -> ApiResult:
        """Return all pattern attribute groups (``GET /pattern_attributes/groups.json``)."""
        return self._get("/pattern_attributes/groups.json", etag=etag, model=PatternAttributeGroupsResponse)


class AsyncPatternAttributes(AsyncResource):
    """Async version of :class:`PatternAttributes`."""

    async def groups(self, etag: Optional[str] = None) -> ApiResult:
        """Return all pattern attribute groups (``GET /pattern_attributes/groups.json``)."""
        return await self._get("/pattern_attributes/groups.json", etag=etag, model=PatternAttributeGroupsResponse)
