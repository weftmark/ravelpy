"""Sub-client for Ravelry Draft Patterns API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import DraftPatternResponse, DraftPatternsResponse


class Drafts(Resource):
    """Wraps draft pattern list and show endpoints.

    Auth: not marked *authenticated* in the docs; the read-only Basic Auth key
    can call these endpoints but they return draft patterns for the credential's
    own pro account(s).  A personal key or OAuth 2.0 is needed to access a
    specific user's draft patterns in practice.
    """

    def list(self, business_id: Optional[int] = None, etag: Optional[str] = None) -> ApiResult:
        """Return draft patterns (``GET /drafts/patterns/list.json``)."""
        return self._get("/drafts/patterns/list.json", {"business_id": business_id}, etag=etag, model=DraftPatternsResponse)

    def show(self, pattern_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single draft pattern (``GET /drafts/patterns/{id}.json``)."""
        return self._get(f"/drafts/patterns/{pattern_id}.json", etag=etag, model=DraftPatternResponse)
