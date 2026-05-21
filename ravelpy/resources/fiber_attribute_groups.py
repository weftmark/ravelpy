from typing import Optional
from .base import ETagResult, Resource


class FiberAttributeGroups(Resource):
    def list(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/fiber_attribute_groups/list.json", etag=etag)

    def attributes(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/fiber_attributes.json", etag=etag)

    def categories(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/fiber_categories.json", etag=etag)
