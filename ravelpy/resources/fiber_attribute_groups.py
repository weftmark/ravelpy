from typing import Optional
from .base import ApiResult, Resource
from ..responses import FiberAttributeGroupsResponse, FiberAttributesResponse, FiberCategoriesResponse


class FiberAttributeGroups(Resource):
    def list(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/fiber_attribute_groups/list.json", etag=etag, model=FiberAttributeGroupsResponse)

    def attributes(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/fiber_attributes.json", etag=etag, model=FiberAttributesResponse)

    def categories(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/fiber_categories.json", etag=etag, model=FiberCategoriesResponse)
