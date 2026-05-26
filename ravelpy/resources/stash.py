"""Sub-client for Ravelry Stash API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, StashListResponse, StashResponse, UnifiedStashResponse


class Stash(Resource):
    """Wraps stash list, show, search, unified view, and comment endpoints.

    Auth: *authenticated* — all five endpoints return 403 with the read-only Basic Auth
    key and require a personal key or OAuth 2.0.  This contradicts the official docs,
    which mark only ``list``, ``show``, and ``unified`` as *authenticated*; live testing
    confirms ``search`` and ``comments`` also require auth.
    """

    async def list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a user's stash (``GET /people/{username}/stash/list.json``)."""
        return await self._get(f"/people/{username}/stash/list.json", {"page": page, "page_size": page_size}, etag=etag, model=StashListResponse)

    async def show(self, username: str, stash_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single stash entry (``GET /people/{username}/stash/{id}.json``)."""
        return await self._get(f"/people/{username}/stash/{stash_id}.json", etag=etag, model=StashResponse)

    async def search(
        self,
        query: Optional[str] = None,
        username: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search stash entries across users (``GET /stash/search.json``)."""
        return await self._get("/stash/search.json", {
            "query": query, "username": username, "page": page, "page_size": page_size,
        }, etag=etag, model=StashListResponse)

    async def unified(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a user's unified stash (``GET /people/{username}/stash/unified/list.json``)."""
        return await self._get(f"/people/{username}/stash/unified/list.json", {"page": page, "page_size": page_size}, etag=etag, model=UnifiedStashResponse)

    async def create(self, username: str, payload: dict) -> ApiResult:
        """Create a stash entry (``POST /people/{username}/stash/create.json``)."""
        return await self._post(f"/people/{username}/stash/create.json", payload)

    async def comments(
        self,
        username: str,
        stash_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments on a stash entry (``GET /people/{username}/stash/{id}/comments.json``)."""
        return await self._get(f"/people/{username}/stash/{stash_id}/comments.json", {"page": page, "page_size": page_size}, etag=etag, model=CommentsResponse)
