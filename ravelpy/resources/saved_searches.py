from typing import Optional
from .base import ETagResult, Resource


class SavedSearches(Resource):
    def list(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/saved_searches/list.json", etag=etag)
