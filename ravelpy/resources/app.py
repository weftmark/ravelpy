"""Sub-client for Ravelry App config/data endpoints."""

from typing import Optional
from .base import ApiResult, Resource


class App(Resource):
    """Wraps application config and data endpoints."""

    def config(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ApiResult:
        """Return app configuration values (``GET /app/config/get.json``)."""
        return self._get("/app/config/get.json", {"keys": keys}, etag=etag)

    def data(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ApiResult:
        """Return app data values (``GET /app/data/get.json``)."""
        return self._get("/app/data/get.json", {"keys": keys}, etag=etag)
