"""Sub-client for Ravelry Packs API endpoints."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import PackResponse


class Packs(Resource):
    """Wraps the pack show endpoint."""

    def show(self, pack_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return a single pack (``GET /packs/{id}.json``)."""
        return self._get(f"/packs/{pack_id}.json", etag=etag, model=PackResponse)
