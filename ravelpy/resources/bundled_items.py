from typing import Optional
from .base import ETagResult, Resource


class BundledItems(Resource):
    def show(self, bundled_item_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/bundled_items/{bundled_item_id}.json", etag=etag)
