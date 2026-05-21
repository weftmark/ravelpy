import httpx
from typing import Optional

from .exceptions import RavelryAPIError

# Every method returns (data, etag).
# On a 200 response: (response_json, etag_string_or_None)
# On a 304 Not Modified: (None, etag) — caller should use its cached data
ETagResult = tuple[Optional[dict], Optional[str]]


class RavelryClient:
    """Read-only client for the Ravelry API using developer credentials (HTTP Basic Auth)."""

    BASE_URL = "https://api.ravelry.com"

    def __init__(self, username: str, api_key: str):
        self.session = httpx.Client(auth=(username, api_key), headers={"Accept": "application/json"})

    def _get(self, path: str, params: Optional[dict] = None, etag: Optional[str] = None) -> ETagResult:
        url = f"{self.BASE_URL}{path}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        headers = {"If-None-Match": etag} if etag else {}
        response = self.session.get(url, params=clean_params, headers=headers)
        returned_etag = response.headers.get("ETag")
        if response.status_code == 304:
            return None, etag
        if not response.is_success:
            raise RavelryAPIError(response.status_code, response.text)
        return response.json(), returned_etag

    # -------------------------------------------------------------------------
    # Reference / Lookup Data
    # -------------------------------------------------------------------------

    def get_color_families(self, etag: Optional[str] = None) -> ETagResult:
        """List all color families."""
        return self._get("/color_families.json", etag=etag)

    def get_fiber_attributes(self, etag: Optional[str] = None) -> ETagResult:
        """List current fiber attributes."""
        return self._get("/fiber_attributes.json", etag=etag)

    def get_fiber_categories(self, etag: Optional[str] = None) -> ETagResult:
        """List current fiber categories."""
        return self._get("/fiber_categories.json", etag=etag)

    def get_fiber_attribute_groups(self, etag: Optional[str] = None) -> ETagResult:
        """List fiber attribute groups."""
        return self._get("/fiber_attribute_groups/list.json", etag=etag)

    def get_yarn_weights(self, etag: Optional[str] = None) -> ETagResult:
        """List active yarn weights."""
        return self._get("/yarn_weights.json", etag=etag)

    def get_yarn_attributes(self, etag: Optional[str] = None) -> ETagResult:
        """List yarn attributes."""
        return self._get("/yarn_attributes/list.json", etag=etag)

    def get_languages(self, etag: Optional[str] = None) -> ETagResult:
        """List available languages."""
        return self._get("/languages/languages.json", etag=etag)

    def get_needles(self, etag: Optional[str] = None) -> ETagResult:
        """List needle records."""
        return self._get("/needles/list.json", etag=etag)

    def get_needle_sizes(self, etag: Optional[str] = None) -> ETagResult:
        """List available needle sizes."""
        return self._get("/needles/sizes.json", etag=etag)

    def get_needle_types(self, etag: Optional[str] = None) -> ETagResult:
        """List needle types."""
        return self._get("/needles/types.json", etag=etag)

    def get_pattern_attributes(self, etag: Optional[str] = None) -> ETagResult:
        """List current pattern attributes."""
        return self._get("/pattern_attributes/list.json", etag=etag)

    def get_pattern_categories(self, etag: Optional[str] = None) -> ETagResult:
        """List current pattern categories."""
        return self._get("/pattern_categories/list.json", etag=etag)

    def get_pattern_source_types(self, etag: Optional[str] = None) -> ETagResult:
        """List current pattern source types."""
        return self._get("/pattern_source_types/list.json", etag=etag)

    def get_project_crafts(self, etag: Optional[str] = None) -> ETagResult:
        """List valid crafts for projects."""
        return self._get("/projects/crafts.json", etag=etag)

    def get_project_statuses(self, etag: Optional[str] = None) -> ETagResult:
        """List valid project statuses."""
        return self._get("/projects/project_statuses.json", etag=etag)

    def get_photo_dimensions(self, etag: Optional[str] = None) -> ETagResult:
        """List photo thumbnail dimensions."""
        return self._get("/photos/dimensions.json", etag=etag)

    def get_photo_sizes(self, etag: Optional[str] = None) -> ETagResult:
        """List available photo sizes."""
        return self._get("/photos/sizes.json", etag=etag)

    # -------------------------------------------------------------------------
    # Global Search
    # -------------------------------------------------------------------------

    def search(
        self,
        query: str,
        types: Optional[str] = None,
        limit: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Global search across multiple resource types."""
        return self._get("/search.json", {"query": query, "types": types, "limit": limit}, etag=etag)

    # -------------------------------------------------------------------------
    # Patterns
    # -------------------------------------------------------------------------

    def get_pattern(self, pattern_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get pattern details by ID."""
        return self._get(f"/patterns/{pattern_id}.json", etag=etag)

    def get_patterns(self, ids: str, etag: Optional[str] = None) -> ETagResult:
        """Get pattern details for multiple patterns (comma-separated IDs)."""
        return self._get("/patterns/patterns.json", {"ids": ids}, etag=etag)

    def search_patterns(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        craft: Optional[str] = None,
        weight: Optional[str] = None,
        colors: Optional[int] = None,
        fit: Optional[str] = None,
        gender: Optional[str] = None,
        availability: Optional[str] = None,
        language: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search the pattern database."""
        return self._get("/patterns/search.json", {
            "query": query, "page": page, "page_size": page_size, "sort": sort,
            "craft": craft, "weight": weight, "colors": colors, "fit": fit,
            "gender": gender, "availability": availability, "language": language,
        }, etag=etag)

    def get_pattern_comments(
        self,
        pattern_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Retrieve comments for a pattern."""
        return self._get(f"/patterns/{pattern_id}/comments.json",
                         {"page": page, "page_size": page_size, "sort": sort}, etag=etag)

    def get_pattern_highlights(self, pattern_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get pattern highlights for the current user."""
        return self._get(f"/patterns/{pattern_id}/highlights.json", etag=etag)

    def get_pattern_projects(
        self,
        pattern_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Retrieve projects linked to a pattern."""
        return self._get(f"/patterns/{pattern_id}/projects.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_pattern_source(self, source_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get pattern source details."""
        return self._get(f"/pattern_sources/{source_id}.json", etag=etag)

    def search_pattern_sources(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search the pattern source database."""
        return self._get("/pattern_sources/search.json",
                         {"query": query, "page": page, "page_size": page_size}, etag=etag)

    def get_pattern_source_patterns(
        self,
        source_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get patterns from a pattern source."""
        return self._get(f"/pattern_sources/{source_id}/patterns.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Yarns
    # -------------------------------------------------------------------------

    def get_yarn(self, yarn_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get yarn details by ID."""
        return self._get(f"/yarns/{yarn_id}.json", etag=etag)

    def get_yarns(self, ids: str, etag: Optional[str] = None) -> ETagResult:
        """Get yarn details for multiple yarns (comma-separated IDs)."""
        return self._get("/yarns/yarns.json", {"ids": ids}, etag=etag)

    def search_yarns(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        weight: Optional[str] = None,
        fiber_min_weight_pct: Optional[int] = None,
        color_family_id: Optional[int] = None,
        fiber_category_id: Optional[int] = None,
        discontinued: Optional[bool] = None,
        personal_attributes: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search the yarn database."""
        return self._get("/yarns/search.json", {
            "query": query, "page": page, "page_size": page_size, "sort": sort,
            "weight": weight, "fiber_min_weight_pct": fiber_min_weight_pct,
            "color_family_id": color_family_id, "fiber_category_id": fiber_category_id,
            "discontinued": discontinued, "personal_attributes": personal_attributes,
        }, etag=etag)

    def get_yarn_comments(
        self,
        yarn_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Retrieve comments for a yarn."""
        return self._get(f"/yarns/{yarn_id}/comments.json",
                         {"page": page, "page_size": page_size, "sort": sort}, etag=etag)

    def search_yarn_companies(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search yarn companies."""
        return self._get("/yarn_companies/search.json",
                         {"query": query, "page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # People / Users
    # -------------------------------------------------------------------------

    def get_current_user(self, etag: Optional[str] = None) -> ETagResult:
        """Get the authenticated user's profile."""
        return self._get("/current_user.json", etag=etag)

    def get_person(self, username: str, etag: Optional[str] = None) -> ETagResult:
        """Get a user's profile by username."""
        return self._get(f"/people/{username}.json", etag=etag)

    def get_person_comments(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List comments made by a user."""
        return self._get(f"/people/{username}/comments/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_saved_searches(self, username: str, etag: Optional[str] = None) -> ETagResult:
        """List a user's saved searches."""
        return self._get(f"/people/{username}/saved_searches/list.json", etag=etag)

    # -------------------------------------------------------------------------
    # Friends
    # -------------------------------------------------------------------------

    def get_friends(self, username: str, etag: Optional[str] = None) -> ETagResult:
        """List a user's friends."""
        return self._get(f"/people/{username}/friends/list.json", etag=etag)

    def get_friends_activity(self, username: str, etag: Optional[str] = None) -> ETagResult:
        """Get recent activity from a user's friends."""
        return self._get(f"/people/{username}/friends/activity.json", etag=etag)

    # -------------------------------------------------------------------------
    # Projects
    # -------------------------------------------------------------------------

    def get_projects(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List a user's projects."""
        return self._get(f"/people/{username}/projects/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_project(self, username: str, project_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a user's project details."""
        return self._get(f"/people/{username}/projects/{project_id}.json", etag=etag)

    def search_projects(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        craft: Optional[str] = None,
        status: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search the project database."""
        return self._get("/projects/search.json", {
            "query": query, "page": page, "page_size": page_size,
            "craft": craft, "status": status,
        }, etag=etag)

    def get_project_comments(
        self,
        project_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Retrieve comments for a project."""
        return self._get(f"/projects/{project_id}/comments.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Stash
    # -------------------------------------------------------------------------

    def get_stash_list(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List a user's stash."""
        return self._get(f"/people/{username}/stash/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_stash(self, username: str, stash_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a stash record."""
        return self._get(f"/people/{username}/stash/{stash_id}.json", etag=etag)

    def search_stash(
        self,
        username: str,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search a user's stash."""
        return self._get(f"/people/{username}/stash/search.json",
                         {"query": query, "page": page, "page_size": page_size}, etag=etag)

    def get_unified_stash(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get a user's unified stash list (yarn + fiber combined)."""
        return self._get(f"/people/{username}/stash/unified/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_stash_comments(
        self,
        username: str,
        stash_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Retrieve comments for a stash entry."""
        return self._get(f"/people/{username}/stash/{stash_id}/comments.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Queue
    # -------------------------------------------------------------------------

    def get_queue(
        self,
        username: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List a user's queue."""
        return self._get(f"/people/{username}/queue/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_queue_item(self, username: str, queue_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a queued project."""
        return self._get(f"/people/{username}/queue/{queue_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Favorites
    # -------------------------------------------------------------------------

    def get_favorites(
        self,
        username: str,
        types: Optional[str] = None,
        query: Optional[str] = None,
        tag: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List a user's favorites."""
        return self._get(f"/people/{username}/favorites/list.json", {
            "types": types, "query": query, "tag": tag,
            "page": page, "page_size": page_size,
        }, etag=etag)

    def get_favorite(self, username: str, favorite_id: int, etag: Optional[str] = None) -> ETagResult:
        """Retrieve a single favorite."""
        return self._get(f"/people/{username}/favorites/{favorite_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Fiber
    # -------------------------------------------------------------------------

    def get_fiber(self, username: str, fiber_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a fiber stash record."""
        return self._get(f"/people/{username}/fiber/{fiber_id}.json", etag=etag)

    def get_fiber_comments(
        self,
        username: str,
        fiber_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Retrieve comments for a fiber stash entry."""
        return self._get(f"/people/{username}/fiber/{fiber_id}/comments.json",
                         {"page": page, "page_size": page_size, "sort": sort}, etag=etag)

    # -------------------------------------------------------------------------
    # Bundles
    # -------------------------------------------------------------------------

    def get_bundles(
        self,
        username: str,
        owner_types: Optional[str] = None,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List a user's bundles."""
        return self._get(f"/people/{username}/bundles/list.json", {
            "owner_types": owner_types, "query": query,
            "page": page, "page_size": page_size,
        }, etag=etag)

    def get_bundle(self, username: str, bundle_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a bundle record."""
        return self._get(f"/people/{username}/bundles/{bundle_id}.json", etag=etag)

    def get_bundled_item(self, bundled_item_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a single bundled item."""
        return self._get(f"/bundled_items/{bundled_item_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Packs
    # -------------------------------------------------------------------------

    def get_pack(self, username: str, pack_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a single pack."""
        return self._get(f"/people/{username}/packs/{pack_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Forums & Topics
    # -------------------------------------------------------------------------

    def get_forum_sets(self, etag: Optional[str] = None) -> ETagResult:
        """Get forum sets for the current user."""
        return self._get("/forums/sets.json", etag=etag)

    def get_forum_topics(
        self,
        forum_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get topic list for a specific forum."""
        return self._get(f"/forums/{forum_id}/topics.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_filtered_topics(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get filtered topics across all forums for the authenticated user."""
        return self._get("/forums/filtered_topics.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_forum_post(self, post_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a single forum post."""
        return self._get(f"/forum_posts/{post_id}.json", etag=etag)

    def get_unread_forum_posts(self, etag: Optional[str] = None) -> ETagResult:
        """Get unread posts across all forums."""
        return self._get("/forum_posts/unread.json", etag=etag)

    def get_topic(self, topic_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get topic details."""
        return self._get(f"/topics/{topic_id}.json", etag=etag)

    def get_topic_posts(
        self,
        topic_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get posts for a topic."""
        return self._get(f"/topics/{topic_id}/posts.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Messages
    # -------------------------------------------------------------------------

    def get_messages(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List private messages."""
        return self._get("/messages/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_message(self, message_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a specific private message."""
        return self._get(f"/messages/{message_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Shops & Stores
    # -------------------------------------------------------------------------

    def search_shops(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search shops."""
        return self._get("/shops/search.json",
                         {"query": query, "page": page, "page_size": page_size}, etag=etag)

    def get_shop(self, shop_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get shop details."""
        return self._get(f"/shops/{shop_id}.json", etag=etag)

    def get_stores(self, etag: Optional[str] = None) -> ETagResult:
        """List stores."""
        return self._get("/stores/list.json", etag=etag)

    def get_store_products(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get a store's products."""
        return self._get(f"/stores/{store_id}/products.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    def get_store_purchases(
        self,
        store_id: int,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get a store's purchases."""
        return self._get(f"/stores/{store_id}/purchases.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Groups
    # -------------------------------------------------------------------------

    def search_groups(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search the group directory."""
        return self._get("/groups/groups.json",
                         {"query": query, "page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Library
    # -------------------------------------------------------------------------

    def search_library(
        self,
        username: str,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Search a user's library."""
        return self._get(f"/library/{username}/search.json",
                         {"query": query, "page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Designers
    # -------------------------------------------------------------------------

    def get_designer(
        self,
        designer_id: int,
        include: Optional[str] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """Get designer details. Pass include='featured_bundles' for extra data."""
        return self._get(f"/designers/{designer_id}.json", {"include": include}, etag=etag)

    # -------------------------------------------------------------------------
    # Products & Deliveries
    # -------------------------------------------------------------------------

    def get_product(self, product_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a product."""
        return self._get(f"/products/{product_id}.json", etag=etag)

    def get_product_attachments(self, product_id: int, etag: Optional[str] = None) -> ETagResult:
        """Retrieve attachments for a product."""
        return self._get(f"/products/{product_id}/attachments.json", etag=etag)

    def get_product_attachment(self, attachment_id: int, etag: Optional[str] = None) -> ETagResult:
        """Retrieve a product attachment."""
        return self._get(f"/product_attachments/{attachment_id}.json", etag=etag)

    def get_deliveries(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List products purchased or gifted to the current user."""
        return self._get("/deliveries/list.json",
                         {"page": page, "page_size": page_size}, etag=etag)

    # -------------------------------------------------------------------------
    # Draft Patterns
    # -------------------------------------------------------------------------

    def get_draft_patterns(
        self,
        business_id: Optional[int] = None,
        etag: Optional[str] = None,
    ) -> ETagResult:
        """List draft patterns."""
        return self._get("/drafts/patterns/list.json", {"business_id": business_id}, etag=etag)

    def get_draft_pattern(self, pattern_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a draft pattern."""
        return self._get(f"/drafts/patterns/{pattern_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Volumes & Pages
    # -------------------------------------------------------------------------

    def get_volume(self, volume_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get volume details."""
        return self._get(f"/volumes/{volume_id}.json", etag=etag)

    def get_page(self, page_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get a page."""
        return self._get(f"/pages/{page_id}.json", etag=etag)

    # -------------------------------------------------------------------------
    # Photos
    # -------------------------------------------------------------------------

    def get_photo_status(self, photo_id: int, etag: Optional[str] = None) -> ETagResult:
        """Get photo creation status."""
        return self._get(f"/photos/{photo_id}/status.json", etag=etag)

    # -------------------------------------------------------------------------
    # App Config
    # -------------------------------------------------------------------------

    def get_app_config(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ETagResult:
        """Get application configuration settings."""
        return self._get("/app/config/get.json", {"keys": keys}, etag=etag)

    def get_app_data(self, keys: Optional[str] = None, etag: Optional[str] = None) -> ETagResult:
        """Get user/app-specific data."""
        return self._get("/app/data/get.json", {"keys": keys}, etag=etag)
