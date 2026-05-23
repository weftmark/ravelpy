"""Sub-client for Ravelry Patterns API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import (
    CommentsResponse,
    PatternHighlightsResponse,
    PatternResponse,
    PatternSearchResponse,
    PatternsMultiResponse,
    ProjectsResponse,
)


class Patterns(Resource):
    """Wraps pattern show, multi-fetch, search, highlights, comments, and projects endpoints.

    Auth: ``show``, ``list``, ``search``, and ``highlights`` are public catalog data accessible
    with the read-only Basic Auth key.  ``comments`` and ``projects`` return 403 with the
    read-only key — they require a personal key or OAuth 2.0.  Any valid OAuth token
    (baseline or higher) is sufficient; no specific scope needed for read access.

    Write operations (create_photo, reorder_photos, update) require ``pattern-write`` or
    ``patternstore-write`` per API docs; not yet implemented in this library.
    """

    async def show(self, pattern_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single pattern by ID (``GET /patterns/{id}.json``)."""
        return await self._get(f"/patterns/{pattern_id}.json", etag=etag, model=PatternResponse)

    async def list(self, ids: str, etag: Optional[str] = None) -> ApiResult:
        """Return multiple patterns by comma-separated IDs (``GET /patterns.json``)."""
        return await self._get("/patterns.json", {"ids": ids}, etag=etag, model=PatternsMultiResponse)

    async def search(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        craft: Optional[str] = None,
        weight: Optional[str] = None,
        colors: Optional[int] = None,
        fit: Optional[str] = None,
        gender: Optional[str] = None,
        availability: Optional[str] = None,
        language: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Search patterns with optional filters (``GET /patterns/search.json``)."""
        return await self._get("/patterns/search.json", {
            "query": query, "page": page, "page_size": page_size, "sort": sort,
            "craft": craft, "weight": weight, "colors": colors, "fit": fit,
            "gender": gender, "availability": availability, "language": language,
        }, etag=etag, model=PatternSearchResponse)

    async def comments(
        self,
        pattern_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return comments for a pattern (``GET /patterns/{id}/comments.json``).

        Authenticated — any valid OAuth token works; no specific scope required.
        Confirmed 200 across all isolated scopes.  See ``docs/authentication.md``.
        """
        return await self._get(f"/patterns/{pattern_id}/comments.json", {"page": page, "page_size": page_size, "sort": sort}, etag=etag, model=CommentsResponse)

    async def highlights(self, etag: Optional[str] = None) -> ApiResult:
        """Return highlighted patterns (``GET /patterns/highlights.json``)."""
        return await self._get("/patterns/highlights.json", etag=etag, model=PatternHighlightsResponse)

    async def projects(
        self,
        pattern_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return projects using a pattern (``GET /patterns/{id}/projects.json``).

        Authenticated — any valid OAuth token works; no specific scope required.
        Confirmed 200 across all isolated scopes.  See ``docs/authentication.md``.
        """
        return await self._get(f"/patterns/{pattern_id}/projects.json", {"page": page, "page_size": page_size}, etag=etag, model=ProjectsResponse)
