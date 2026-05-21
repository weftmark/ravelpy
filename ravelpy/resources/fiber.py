"""Sub-client for Ravelry Fiber stash API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, FiberStashResponse


class Fiber(Resource):
    """Wraps fiber stash show and comment endpoints.

    Auth: ``show`` is marked *authenticated* and requires a personal key or
    OAuth 2.0.  ``comments`` is not marked authenticated and works with the
    read-only Basic Auth key.
    """

    def show(self, username: str, fiber_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single fiber stash entry (``GET /people/{username}/fiber/{id}.json``)."""
        return self._get(f"/people/{username}/fiber/{fiber_id}.json", etag=etag, model=FiberStashResponse)

    def comments(
        self,
        username: str,
        fiber_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments on a fiber entry (``GET /people/{username}/fiber/{id}/comments.json``)."""
        return self._get(
            f"/people/{username}/fiber/{fiber_id}/comments.json",
            {"page": page, "page_size": page_size, "sort": sort},
            etag=etag,
            model=CommentsResponse,
        )
