from typing import Optional
from .base import ApiResult, Resource
from ..responses import MessageResponse, MessagesResponse


class Messages(Resource):
    def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get("/messages/list.json", {"page": page, "page_size": page_size}, etag=etag, model=MessagesResponse)

    def show(self, message_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/messages/{message_id}.json", etag=etag, model=MessageResponse)
