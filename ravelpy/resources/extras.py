from typing import Optional
from .base import ETagResult, Resource


class Extras(Resource):
    """Reference data and global endpoints not scoped to a specific resource."""

    def color_families(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/color_families.json", etag=etag)

    def search(
        self,
        query: str,
        types: Optional[str] = None,
        limit: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/search.json", {"query": query, "types": types, "limit": limit}, etag=etag)
