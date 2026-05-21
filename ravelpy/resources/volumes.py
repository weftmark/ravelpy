from typing import Optional
from .base import ETagResult, Resource


class Volumes(Resource):
    def show(self, volume_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/volumes/{volume_id}.json", etag=etag)
