"""Sub-client for Ravelry Fiber Attribute Groups reference endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import FiberAttributeGroupsResponse, FiberAttributesResponse, FiberCategoriesResponse


class FiberAttributeGroups(Resource):
    """Wraps fiber attribute groups, attributes, and categories endpoints."""

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all fiber attribute groups (``GET /fiber_attribute_groups/list.json``)."""
        return self._get("/fiber_attribute_groups/list.json", etag=etag, model=FiberAttributeGroupsResponse)

    def attributes(self, etag: Optional[str] = None) -> ApiResult:
        """Return all fiber attributes (``GET /fiber_attributes.json``)."""
        return self._get("/fiber_attributes.json", etag=etag, model=FiberAttributesResponse)

    def categories(self, etag: Optional[str] = None) -> ApiResult:
        """Return all fiber categories (``GET /fiber_categories.json``)."""
        return self._get("/fiber_categories.json", etag=etag, model=FiberCategoriesResponse)
