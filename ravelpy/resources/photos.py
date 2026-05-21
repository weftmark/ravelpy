"""Sub-client for Ravelry Photos API endpoints."""

from typing import Optional
from .base import ApiResult, Resource


class Photos(Resource):
    """Wraps photo dimensions, sizes, and status endpoints."""

    def dimensions(self, etag: Optional[str] = None) -> ApiResult:
        """Return available photo dimension definitions (``GET /photos/dimensions.json``)."""
        return self._get("/photos/dimensions.json", etag=etag)

    def sizes(self, photo_id: int, etag: Optional[str] = None) -> ApiResult:
        """Return size variants for a photo (``GET /photos/{id}/sizes.json``)."""
        return self._get(f"/photos/{photo_id}/sizes.json", etag=etag)

    def status(self, etag: Optional[str] = None) -> ApiResult:
        """Return the photo upload service status (``GET /photos/status.json``)."""
        return self._get("/photos/status.json", etag=etag)
