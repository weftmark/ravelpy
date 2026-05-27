"""Sub-client for Ravelry Stash API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import CommentsResponse, StashListResponse, StashResponse, UnifiedStashResponse


class Stash(Resource):
    """Wraps stash list, show, search, unified view, comment, and create endpoints.

    Auth: *authenticated* — all endpoints return 403 with the read-only Basic Auth
    key and require a personal key or OAuth 2.0.  This contradicts the official docs,
    which mark only ``list``, ``show``, and ``unified`` as *authenticated*; live testing
    confirms ``search`` and ``comments`` also require auth.  ``create`` additionally
    requires write access — a personal key or an OAuth token with the ``offline`` scope
    is sufficient.
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
        """Create a stash entry (``POST /people/{username}/stash/create.json``).

        Requires a personal key or OAuth 2.0 Bearer token; the ``offline`` scope is
        sufficient.  The response envelope is ``{"stash": {...}}`` — the new entry's
        ID is at ``raw["stash"]["id"]``.

        Args:
            username: Ravelry username of the account to add the stash entry to.
            payload:  Dict of fields to set.  Common fields:

                      * ``yarn_id`` (int, required) — Ravelry yarn ID.
                      * ``colorway_name`` (str) — colour name as shown on the label.
                      * ``dye_lot`` (str) — dye lot identifier.
                      * ``notes`` (str) — free-text notes.
                      * ``stash_status_id`` (int) — ``1`` = in stock, ``2`` = used up,
                        ``3`` = gifted/sold.
                      * ``skeins`` (float) — number of skeins.
                      * ``grams_per_skein`` / ``yards_per_skein`` (float).

        Returns:
            :data:`~ravelpy.resources.base.ApiResult` 3-tuple ``(parsed, etag, raw)``.
            ``raw["stash"]["id"]`` is the new stash entry ID.

        Raises:
            :class:`~ravelpy.exceptions.RavelryAPIError`: On any non-2xx response
            (e.g. 403 when using a read-only key).
        """
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
