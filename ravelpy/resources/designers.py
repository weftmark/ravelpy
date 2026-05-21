from typing import Optional
from .base import ApiResult, Resource


class Designers(Resource):
    def show(
        self,
        designer_id: int,
        include: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ApiResult:
        return self._get(f"/designers/{designer_id}.json", {"include": include}, etag=etag)
