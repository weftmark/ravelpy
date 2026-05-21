from typing import Optional
from .base import ApiResult, Resource
from ..responses import PatternCategoriesResponse


class PatternCategories(Resource):
    def list(self, etag: Optional[str] = None) -> ApiResult:
        return self._get("/pattern_categories/list.json", etag=etag, model=PatternCategoriesResponse)
