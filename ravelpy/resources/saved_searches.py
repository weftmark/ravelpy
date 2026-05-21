"""Sub-client for Ravelry Saved Searches API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import SavedSearchesResponse


class SavedSearches(Resource):
    """Wraps the saved searches list endpoint."""

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return the authenticated user's saved searches (``GET /saved_searches/list.json``)."""
        return self._get("/saved_searches/list.json", etag=etag, model=SavedSearchesResponse)
