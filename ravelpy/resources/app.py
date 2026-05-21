from typing import Optional
from .base import ApiResult, Resource


class App(Resource):
    def config(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ApiResult:
        return self._get("/app/config/get.json", {"keys": keys}, etag=etag)

    def data(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ApiResult:
        return self._get("/app/data/get.json", {"keys": keys}, etag=etag)
