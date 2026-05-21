from typing import Optional
from .base import ETagResult, Resource


class Stash(Resource):
    def list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/people/{username}/stash/list.json", {"page": page, "page_size": page_size}, etag=etag)

    def show(self, username: str, stash_id: int, etag: Optional[str] = None) -> ETagResult:
        return self._get(f"/people/{username}/stash/{stash_id}.json", etag=etag)

    def search(
        self,
        query: Optional[str] = None,
        username: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get("/stash/search.json", {
            "query": query, "username": username, "page": page, "page_size": page_size,
        }, etag=etag)

    def unified(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/people/{username}/stash/unified/list.json", {"page": page, "page_size": page_size}, etag=etag)

    def comments(
        self,
        username: str,
        stash_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        return self._get(f"/people/{username}/stash/{stash_id}/comments.json", {"page": page, "page_size": page_size}, etag=etag)
