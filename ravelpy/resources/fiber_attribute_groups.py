"""Sub-client for Ravelry Fiber Attribute Groups reference endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import FiberAttributeGroupsResponse, FiberAttributesResponse, FiberCategoriesResponse


class FiberAttributeGroups(Resource):
    """Wraps fiber attribute groups, attributes, and categories endpoints.

    Auth: ``attributes`` and ``categories`` are public catalog data accessible with the
    read-only Basic Auth key.  ``list`` redirects to the Ravelry login page with the
    read-only key — it requires a personal key or OAuth 2.0.
    """

    async def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all fiber attribute groups (``GET /fiber_attribute_groups/list.json``).

        Authenticated — requires a personal key or OAuth 2.0.
        """
        return await self._get("/fiber_attribute_groups/list.json", etag=etag, model=FiberAttributeGroupsResponse)

    async def attributes(self, etag: Optional[str] = None) -> ApiResult:
        """Return all fiber attributes (``GET /fiber_attributes.json``)."""
        return await self._get("/fiber_attributes.json", etag=etag, model=FiberAttributesResponse)

    async def categories(self, etag: Optional[str] = None) -> ApiResult:
        """Return all fiber categories (``GET /fiber_categories.json``)."""
        return await self._get("/fiber_categories.json", etag=etag, model=FiberCategoriesResponse)
