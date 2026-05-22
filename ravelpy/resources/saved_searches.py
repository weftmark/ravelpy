"""Sub-client for Ravelry Saved Searches API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import SavedSearchesResponse


class SavedSearches(Resource):
    """Wraps the saved searches list endpoint.

    Auth: *authenticated* — returns 403 with the read-only Basic Auth key despite not
    being marked *authenticated* in the official docs.  A personal key or OAuth 2.0
    is required.
    """

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return the authenticated user's saved searches (``GET /saved_searches/list.json``)."""
        return self._get("/saved_searches/list.json", etag=etag, model=SavedSearchesResponse)


class AsyncSavedSearches(AsyncResource):
    """Async version of :class:`SavedSearches`."""

    async def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return the authenticated user's saved searches (``GET /saved_searches/list.json``)."""
        return await self._get("/saved_searches/list.json", etag=etag, model=SavedSearchesResponse)
