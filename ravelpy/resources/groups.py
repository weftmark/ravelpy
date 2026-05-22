"""Sub-client for Ravelry Groups API endpoints."""

from typing import Optional
from .base import ApiResult, AsyncResource, Resource
from ..responses import GroupsResponse


class Groups(Resource):
    """Wraps the group search endpoint.

    Auth: public catalog data — any valid developer credentials (read-only key or higher).
    """

    def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search groups (``GET /groups/search.json``)."""
        return self._get("/groups/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=GroupsResponse)


class AsyncGroups(AsyncResource):
    """Async version of :class:`Groups`."""

    async def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search groups (``GET /groups/search.json``)."""
        return await self._get("/groups/search.json", {"query": query, "page": page, "page_size": page_size}, etag=etag, model=GroupsResponse)
