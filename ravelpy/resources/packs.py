from typing import Optional
from .base import ETagResult, Resource


class Packs(Resource):
    def show(self, pack_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/packs/{pack_id}.json", etag=etag)
