from typing import Optional
from .base import ETagResult, Resource


class Photos(Resource):
    def dimensions(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/photos/dimensions.json", etag=etag)

    def sizes(self, photo_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/photos/{photo_id}/sizes.json", etag=etag)

    def status(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/photos/status.json", etag=etag)
