"""Sub-client for Ravelry Designers API endpoints."""

from typing import Optional
from .base import ApiResult, Resource


class Designers(Resource):
    """Wraps the designer show endpoint."""

    def show(
        self,
        designer_id: int,
        include: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        """Return a single designer (``GET /designers/{id}.json``)."""
        return self._get(f"/designers/{designer_id}.json", {"include": include}, etag=etag)
