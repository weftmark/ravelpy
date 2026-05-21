from typing import Optional
from .base import ApiResult, Resource
from ..responses import SavedSearchesResponse


class SavedSearches(Resource):
    def list(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/saved_searches/list.json", etag=etag, model=SavedSearchesResponse)
