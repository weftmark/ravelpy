from typing import Optional
from .base import ApiResult, Resource
from ..responses import LanguagesResponse


class Languages(Resource):
    def list(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/languages/list.json", etag=etag, model=LanguagesResponse)
