from typing import Optional
from .base import ETagResult, Resource


class YarnAttributes(Resource):
    def groups(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/yarn_attributes/groups.json", etag=etag)

    def weights(self, etag: Optional[str] = None) -> ETagResult:
        return self._get("/yarn_weights.json", etag=etag)
