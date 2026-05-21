from typing import Optional
from .base import ApiResult, Resource
from ..responses import PackResponse


class Packs(Resource):
    def show(self, pack_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/packs/{pack_id}.json", etag=etag, model=PackResponse)
