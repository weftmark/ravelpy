from typing import Optional
from .base import ApiResult, Resource
from ..responses import ColorFamiliesResponse


class Extras(Resource):
    """Reference data and global endpoints not scoped to a specific resource."""

    def color_families(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/color_families.json", etag=etag, model=ColorFamiliesResponse)

    def search(
        self,
        query: str,
        types: Optional[str] = None,
        limit: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/search.json", {"query": query, "types": types, "limit": limit}, etag=etag)
