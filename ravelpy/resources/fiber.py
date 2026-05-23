"""Sub-client for Ravelry Fiber stash API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, FiberStashResponse


class Fiber(Resource):
    """Wraps fiber stash show and comment endpoints.

    Auth: public catalog data — both endpoints are accessible with the read-only Basic
    Auth key.  ``show`` is marked *authenticated* in the official docs but returns 200
    or 404 (not 403) in live testing, indicating auth is not enforced.
    """

    async def show(self, username: str, fiber_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single fiber stash entry (``GET /people/{username}/fiber/{id}.json``)."""
        return await self._get(f"/people/{username}/fiber/{fiber_id}.json", etag=etag, model=FiberStashResponse)

    async def comments(
        self,
        username: str,
        fiber_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments on a fiber entry (``GET /people/{username}/fiber/{id}/comments.json``)."""
        return await self._get(
            f"/people/{username}/fiber/{fiber_id}/comments.json",
            {"page": page, "page_size": page_size, "sort": sort},
            etag=etag,
            model=CommentsResponse,
        )
