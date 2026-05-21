from typing import Optional
from .base import ETagResult, Resource


class App(Resource):
    def config(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ETagResult:
        return self._get("/app/config/get.json", {"keys": keys}, etag=etag)

    def data(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ETagResult:
        return self._get("/app/data/get.json", {"keys": keys}, etag=etag)
