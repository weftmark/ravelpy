from typing import Optional
from .base import ETagResult, Resource


class Needles(Resource):
    def list(self, username: str, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}/needles/list.json", etag=etag)

    def sizes(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/needles/sizes.json", etag=etag)

    def types(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/needles/types.json", etag=etag)
