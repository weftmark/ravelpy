from typing import Optional
from .base import ApiResult, Resource
from ..responses import VolumeResponse


class Volumes(Resource):
    def show(self, volume_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/volumes/{volume_id}.json", etag=etag, model=VolumeResponse)
