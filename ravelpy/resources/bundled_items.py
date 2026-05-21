from typing import Optional
from .base import ApiResult, Resource
from ..responses import BundledItemResponse


class BundledItems(Resource):
    def show(self, bundled_item_id: int, etag: Optional[str] = None) -> ApiResult:
        return self._get(f"/bundled_items/{bundled_item_id}.json", etag=etag, model=BundledItemResponse)
