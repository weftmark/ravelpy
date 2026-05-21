"""Sub-client for Ravelry Languages reference endpoint."""

from typing import Optional
from .base import ApiResult, Resource
from ..responses import LanguagesResponse


class Languages(Resource):
    """Wraps the languages list endpoint."""

    def list(self, etag: Optional[str] = None) -> ApiResult:
        """Return all supported languages (``GET /languages/list.json``)."""
        return self._get("/languages/list.json", etag=etag, model=LanguagesResponse)
