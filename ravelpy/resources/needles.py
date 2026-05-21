from typing import Optional
from .base import ApiResult, Resource
from ..responses import NeedlesResponse, NeedleSizesResponse, NeedleTypesResponse


class Needles(Resource):
    def list(self, username: str, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/people/{username}/needles/list.json", etag=etag, model=NeedlesResponse)

    def sizes(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/needles/sizes.json", etag=etag, model=NeedleSizesResponse)

    def types(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/needles/types.json", etag=etag, model=NeedleTypesResponse)
