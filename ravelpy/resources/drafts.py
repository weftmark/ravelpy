"""Sub-client for Ravelry Draft Patterns API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import DraftPatternResponse, DraftPatternsResponse


class Drafts(Resource):
    """Wraps draft pattern list and show endpoints.

    Auth: *authenticated* — both endpoints return 403 with the read-only Basic Auth key
    despite not being marked *authenticated* in the official docs.  A personal key or
    OAuth 2.0 is required.

    Required OAuth scope (per API docs): ``patternstore-read`` or ``patternstore-write``.
    Scope matrix confirms ``drafts.list`` returns 200 with ``patternstore-read``, 403
    with baseline.  See ``docs/authentication.md``.

    Both endpoints are scoped to the **current user's pattern store** (pro account).
    Users without a pattern store receive an empty list or 404.  Draft IDs are separate
    from published pattern IDs — a published pattern ID will return 404 here.
    See GitHub issue #1 for ``drafts.show`` investigation status.
    """

    def list(self, business_id: Optional[int] = None, etag: Optional[str] = None) -> ApiResult:
        """Return the current user's draft patterns (``GET /drafts/patterns/list.json``).

        Requires ``patternstore-read`` or ``patternstore-write`` OAuth scope.
        Returns empty list if the user has no pattern store or no drafts.
        Scope matrix result: 200 with ``patternstore-read``. See ``docs/authentication.md``.
        """
        return self._get("/drafts/patterns/list.json", {"business_id": business_id}, etag=etag, model=DraftPatternsResponse)

    def show(self, pattern_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single draft pattern (``GET /drafts/patterns/{id}.json``).

        Requires ``patternstore-read`` or ``patternstore-write`` OAuth scope.
        The ``id`` must be a draft pattern ID owned by the current user — published
        pattern IDs return 404.

        TODO: validate with a real draft ID; no user with active drafts has been tested
        yet (live testing with this account returned empty list).  See GitHub issue #1.
        """
        return self._get(f"/drafts/patterns/{pattern_id}.json", etag=etag, model=DraftPatternResponse)
