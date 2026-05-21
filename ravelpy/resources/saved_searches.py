"""Sub-client for Ravelry Saved Searches API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import SavedSearchesResponse


class SavedSearches(Resource):
    """Wraps the saved searches list endpoint.

    Auth: not marked *authenticated* in the docs; the read-only Basic Auth key
    can call this endpoint but will return the saved searches for the credential's
    own account (typically empty for a read-only app key).  A personal key or
    OAuth 2.0 returns the relevant user's saved searches.
    """

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return the authenticated user's saved searches (``GET /saved_searches/list.json``)."""
        return self._get("/saved_searches/list.json", etag=etag, model=SavedSearchesResponse)
