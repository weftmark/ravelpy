"""
Ravelry API proxy server — read-only access with interactive Swagger UI.

Run:
    uvicorn server:app --reload

Swagger UI: http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
"""

import os
from functools import lru_cache
from typing import Annotated, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware

from ravelpy import RavelryAPIError, RavelryClient

load_dotenv()

app = FastAPI(
    title="Ravelry API",
    description=(
        "Read-only access to the [Ravelry API](https://www.ravelry.com/api).\n\n"
        "Authenticates with developer credentials (HTTP Basic Auth) loaded from "
        "`RAVELRY_USERNAME` and `RAVELRY_API_KEY` environment variables.\n\n"
        "Set those variables in a `.env` file before starting the server."
    ),
    version="1.0.0",
    contact={"name": "Ravelry API Docs", "url": "https://www.ravelry.com/api"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def _make_client() -> RavelryClient:
    username = os.getenv("RAVELRY_USERNAME")
    api_key = os.getenv("RAVELRY_API_KEY")
    if not username or not api_key:
        raise RuntimeError("RAVELRY_USERNAME and RAVELRY_API_KEY must be set in the environment or .env file")
    return RavelryClient(username, api_key)


def client() -> RavelryClient:
    return _make_client()


ClientDep = Annotated[RavelryClient, Depends(client)]


def _handle(fn):
    """Wrap a client call, unpack the (data, etag) tuple, and convert RavelryAPIError to HTTPException."""
    try:
        data, _etag = fn()
        return data
    except RavelryAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


# =============================================================================
# Reference / Lookup Data
# =============================================================================

ref_tag = "Reference Data"


@app.get("/color-families", tags=[ref_tag], summary="List color families")
def get_color_families(c: ClientDep):
    return _handle(c.get_color_families)


@app.get("/fiber-attributes", tags=[ref_tag], summary="List fiber attributes")
def get_fiber_attributes(c: ClientDep):
    return _handle(c.get_fiber_attributes)


@app.get("/fiber-categories", tags=[ref_tag], summary="List fiber categories")
def get_fiber_categories(c: ClientDep):
    return _handle(c.get_fiber_categories)


@app.get("/fiber-attribute-groups", tags=[ref_tag], summary="List fiber attribute groups")
def get_fiber_attribute_groups(c: ClientDep):
    return _handle(c.get_fiber_attribute_groups)


@app.get("/yarn-weights", tags=[ref_tag], summary="List yarn weights")
def get_yarn_weights(c: ClientDep):
    return _handle(c.get_yarn_weights)


@app.get("/yarn-attributes", tags=[ref_tag], summary="List yarn attributes")
def get_yarn_attributes(c: ClientDep):
    return _handle(c.get_yarn_attributes)


@app.get("/languages", tags=[ref_tag], summary="List available languages")
def get_languages(c: ClientDep):
    return _handle(c.get_languages)


@app.get("/needles", tags=[ref_tag], summary="List needle records")
def get_needles(c: ClientDep):
    return _handle(c.get_needles)


@app.get("/needles/sizes", tags=[ref_tag], summary="List needle sizes")
def get_needle_sizes(c: ClientDep):
    return _handle(c.get_needle_sizes)


@app.get("/needles/types", tags=[ref_tag], summary="List needle types")
def get_needle_types(c: ClientDep):
    return _handle(c.get_needle_types)


@app.get("/pattern-attributes", tags=[ref_tag], summary="List pattern attributes")
def get_pattern_attributes(c: ClientDep):
    return _handle(c.get_pattern_attributes)


@app.get("/pattern-categories", tags=[ref_tag], summary="List pattern categories")
def get_pattern_categories(c: ClientDep):
    return _handle(c.get_pattern_categories)


@app.get("/pattern-source-types", tags=[ref_tag], summary="List pattern source types")
def get_pattern_source_types(c: ClientDep):
    return _handle(c.get_pattern_source_types)


@app.get("/project-crafts", tags=[ref_tag], summary="List valid project crafts")
def get_project_crafts(c: ClientDep):
    return _handle(c.get_project_crafts)


@app.get("/project-statuses", tags=[ref_tag], summary="List valid project statuses")
def get_project_statuses(c: ClientDep):
    return _handle(c.get_project_statuses)


@app.get("/photo-dimensions", tags=[ref_tag], summary="List photo thumbnail dimensions")
def get_photo_dimensions(c: ClientDep):
    return _handle(c.get_photo_dimensions)


@app.get("/photo-sizes", tags=[ref_tag], summary="List available photo sizes")
def get_photo_sizes(c: ClientDep):
    return _handle(c.get_photo_sizes)


# =============================================================================
# Global Search
# =============================================================================

search_tag = "Search"


@app.get("/search", tags=[search_tag], summary="Global search")
def global_search(
    c: ClientDep,
    query: str = Query(..., description="Search query string"),
    types: Optional[str] = Query(None, description="Comma-separated resource types (e.g. patterns,yarns)"),
    limit: Optional[int] = Query(None, description="Maximum number of results"),
):
    return _handle(lambda: c.search(query=query, types=types, limit=limit))


# =============================================================================
# Patterns
# =============================================================================

patterns_tag = "Patterns"


@app.get("/patterns/search", tags=[patterns_tag], summary="Search patterns")
def search_patterns(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None, description="Sort field (e.g. best, popularity, created)"),
    craft: Optional[str] = Query(None, description="Craft type (e.g. knitting, crochet)"),
    weight: Optional[str] = Query(None, description="Yarn weight (e.g. dk, worsted, fingering)"),
    colors: Optional[int] = Query(None),
    fit: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    availability: Optional[str] = Query(None, description="e.g. free, ravelry"),
    language: Optional[str] = Query(None),
):
    return _handle(lambda: c.search_patterns(
        query=query, page=page, page_size=page_size, sort=sort,
        craft=craft, weight=weight, colors=colors, fit=fit, gender=gender,
        availability=availability, language=language,
    ))


@app.get("/patterns/multi", tags=[patterns_tag], summary="Get multiple patterns by ID")
def get_patterns(
    c: ClientDep,
    ids: str = Query(..., description="Comma-separated pattern IDs"),
):
    return _handle(lambda: c.get_patterns(ids=ids))


@app.get("/patterns/{pattern_id}", tags=[patterns_tag], summary="Get a pattern")
def get_pattern(
    c: ClientDep,
    pattern_id: int = Path(...),
):
    return _handle(lambda: c.get_pattern(pattern_id=pattern_id))


@app.get("/patterns/{pattern_id}/comments", tags=[patterns_tag], summary="Get pattern comments")
def get_pattern_comments(
    c: ClientDep,
    pattern_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    return _handle(lambda: c.get_pattern_comments(pattern_id=pattern_id, page=page, page_size=page_size, sort=sort))


@app.get("/patterns/{pattern_id}/highlights", tags=[patterns_tag], summary="Get pattern highlights")
def get_pattern_highlights(
    c: ClientDep,
    pattern_id: int = Path(...),
):
    return _handle(lambda: c.get_pattern_highlights(pattern_id=pattern_id))


@app.get("/patterns/{pattern_id}/projects", tags=[patterns_tag], summary="Get projects linked to a pattern")
def get_pattern_projects(
    c: ClientDep,
    pattern_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_pattern_projects(pattern_id=pattern_id, page=page, page_size=page_size))


@app.get("/pattern-sources/search", tags=[patterns_tag], summary="Search pattern sources")
def search_pattern_sources(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.search_pattern_sources(query=query, page=page, page_size=page_size))


@app.get("/pattern-sources/{source_id}", tags=[patterns_tag], summary="Get a pattern source")
def get_pattern_source(
    c: ClientDep,
    source_id: int = Path(...),
):
    return _handle(lambda: c.get_pattern_source(source_id=source_id))


@app.get("/pattern-sources/{source_id}/patterns", tags=[patterns_tag], summary="Get patterns from a source")
def get_pattern_source_patterns(
    c: ClientDep,
    source_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_pattern_source_patterns(source_id=source_id, page=page, page_size=page_size))


# =============================================================================
# Yarns
# =============================================================================

yarns_tag = "Yarns"


@app.get("/yarns/search", tags=[yarns_tag], summary="Search yarns")
def search_yarns(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
    weight: Optional[str] = Query(None),
    fiber_min_weight_pct: Optional[int] = Query(None, ge=0, le=100),
    color_family_id: Optional[int] = Query(None),
    fiber_category_id: Optional[int] = Query(None),
    discontinued: Optional[bool] = Query(None),
    personal_attributes: Optional[str] = Query(None),
):
    return _handle(lambda: c.search_yarns(
        query=query, page=page, page_size=page_size, sort=sort, weight=weight,
        fiber_min_weight_pct=fiber_min_weight_pct, color_family_id=color_family_id,
        fiber_category_id=fiber_category_id, discontinued=discontinued,
        personal_attributes=personal_attributes,
    ))


@app.get("/yarns/multi", tags=[yarns_tag], summary="Get multiple yarns by ID")
def get_yarns(
    c: ClientDep,
    ids: str = Query(..., description="Comma-separated yarn IDs"),
):
    return _handle(lambda: c.get_yarns(ids=ids))


@app.get("/yarns/{yarn_id}", tags=[yarns_tag], summary="Get a yarn")
def get_yarn(
    c: ClientDep,
    yarn_id: int = Path(...),
):
    return _handle(lambda: c.get_yarn(yarn_id=yarn_id))


@app.get("/yarns/{yarn_id}/comments", tags=[yarns_tag], summary="Get yarn comments")
def get_yarn_comments(
    c: ClientDep,
    yarn_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    return _handle(lambda: c.get_yarn_comments(yarn_id=yarn_id, page=page, page_size=page_size, sort=sort))


@app.get("/yarn-companies/search", tags=[yarns_tag], summary="Search yarn companies")
def search_yarn_companies(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.search_yarn_companies(query=query, page=page, page_size=page_size))


# =============================================================================
# People / Users
# =============================================================================

people_tag = "People"


@app.get("/current-user", tags=[people_tag], summary="Get authenticated user profile")
def get_current_user(c: ClientDep):
    return _handle(c.get_current_user)


@app.get("/people/{username}", tags=[people_tag], summary="Get a user's profile")
def get_person(
    c: ClientDep,
    username: str = Path(...),
):
    return _handle(lambda: c.get_person(username=username))


@app.get("/people/{username}/comments", tags=[people_tag], summary="List comments by a user")
def get_person_comments(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_person_comments(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/saved-searches", tags=[people_tag], summary="List a user's saved searches")
def get_saved_searches(
    c: ClientDep,
    username: str = Path(...),
):
    return _handle(lambda: c.get_saved_searches(username=username))


@app.get("/people/{username}/friends", tags=[people_tag], summary="List a user's friends")
def get_friends(
    c: ClientDep,
    username: str = Path(...),
):
    return _handle(lambda: c.get_friends(username=username))


@app.get("/people/{username}/friends/activity", tags=[people_tag], summary="Get friends' recent activity")
def get_friends_activity(
    c: ClientDep,
    username: str = Path(...),
):
    return _handle(lambda: c.get_friends_activity(username=username))


@app.get("/people/{username}/library/search", tags=[people_tag], summary="Search a user's library")
def search_library(
    c: ClientDep,
    username: str = Path(...),
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.search_library(username=username, query=query, page=page, page_size=page_size))


# =============================================================================
# Projects
# =============================================================================

projects_tag = "Projects"


@app.get("/projects/search", tags=[projects_tag], summary="Search the project database")
def search_projects(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    craft: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    return _handle(lambda: c.search_projects(query=query, page=page, page_size=page_size, craft=craft, status=status))


@app.get("/people/{username}/projects", tags=[projects_tag], summary="List a user's projects")
def get_projects(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_projects(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/projects/{project_id}", tags=[projects_tag], summary="Get a user's project")
def get_project(
    c: ClientDep,
    username: str = Path(...),
    project_id: int = Path(...),
):
    return _handle(lambda: c.get_project(username=username, project_id=project_id))


@app.get("/projects/{project_id}/comments", tags=[projects_tag], summary="Get project comments")
def get_project_comments(
    c: ClientDep,
    project_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_project_comments(project_id=project_id, page=page, page_size=page_size))


# =============================================================================
# Stash
# =============================================================================

stash_tag = "Stash"


@app.get("/people/{username}/stash", tags=[stash_tag], summary="List a user's stash")
def get_stash_list(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_stash_list(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/stash/search", tags=[stash_tag], summary="Search a user's stash")
def search_stash(
    c: ClientDep,
    username: str = Path(...),
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.search_stash(username=username, query=query, page=page, page_size=page_size))


@app.get("/people/{username}/stash/unified", tags=[stash_tag], summary="Get unified stash (yarn + fiber)")
def get_unified_stash(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_unified_stash(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/stash/{stash_id}", tags=[stash_tag], summary="Get a stash record")
def get_stash(
    c: ClientDep,
    username: str = Path(...),
    stash_id: int = Path(...),
):
    return _handle(lambda: c.get_stash(username=username, stash_id=stash_id))


@app.get("/people/{username}/stash/{stash_id}/comments", tags=[stash_tag], summary="Get stash comments")
def get_stash_comments(
    c: ClientDep,
    username: str = Path(...),
    stash_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_stash_comments(username=username, stash_id=stash_id, page=page, page_size=page_size))


# =============================================================================
# Queue
# =============================================================================

queue_tag = "Queue"


@app.get("/people/{username}/queue", tags=[queue_tag], summary="List a user's queue")
def get_queue(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_queue(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/queue/{queue_id}", tags=[queue_tag], summary="Get a queued project")
def get_queue_item(
    c: ClientDep,
    username: str = Path(...),
    queue_id: int = Path(...),
):
    return _handle(lambda: c.get_queue_item(username=username, queue_id=queue_id))


# =============================================================================
# Favorites
# =============================================================================

favorites_tag = "Favorites"


@app.get("/people/{username}/favorites", tags=[favorites_tag], summary="List a user's favorites")
def get_favorites(
    c: ClientDep,
    username: str = Path(...),
    types: Optional[str] = Query(None, description="Resource types to filter (e.g. pattern, yarn)"),
    query: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_favorites(
        username=username, types=types, query=query, tag=tag, page=page, page_size=page_size,
    ))


@app.get("/people/{username}/favorites/{favorite_id}", tags=[favorites_tag], summary="Get a single favorite")
def get_favorite(
    c: ClientDep,
    username: str = Path(...),
    favorite_id: int = Path(...),
):
    return _handle(lambda: c.get_favorite(username=username, favorite_id=favorite_id))


# =============================================================================
# Fiber
# =============================================================================

fiber_tag = "Fiber"


@app.get("/people/{username}/fiber/{fiber_id}", tags=[fiber_tag], summary="Get a fiber stash record")
def get_fiber(
    c: ClientDep,
    username: str = Path(...),
    fiber_id: int = Path(...),
):
    return _handle(lambda: c.get_fiber(username=username, fiber_id=fiber_id))


@app.get("/people/{username}/fiber/{fiber_id}/comments", tags=[fiber_tag], summary="Get fiber stash comments")
def get_fiber_comments(
    c: ClientDep,
    username: str = Path(...),
    fiber_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    return _handle(lambda: c.get_fiber_comments(username=username, fiber_id=fiber_id, page=page, page_size=page_size, sort=sort))


# =============================================================================
# Bundles
# =============================================================================

bundles_tag = "Bundles"


@app.get("/people/{username}/bundles", tags=[bundles_tag], summary="List a user's bundles")
def get_bundles(
    c: ClientDep,
    username: str = Path(...),
    owner_types: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_bundles(
        username=username, owner_types=owner_types, query=query, page=page, page_size=page_size,
    ))


@app.get("/people/{username}/bundles/{bundle_id}", tags=[bundles_tag], summary="Get a bundle")
def get_bundle(
    c: ClientDep,
    username: str = Path(...),
    bundle_id: int = Path(...),
):
    return _handle(lambda: c.get_bundle(username=username, bundle_id=bundle_id))


@app.get("/bundled-items/{bundled_item_id}", tags=[bundles_tag], summary="Get a single bundled item")
def get_bundled_item(
    c: ClientDep,
    bundled_item_id: int = Path(...),
):
    return _handle(lambda: c.get_bundled_item(bundled_item_id=bundled_item_id))


@app.get("/people/{username}/packs/{pack_id}", tags=[bundles_tag], summary="Get a pack")
def get_pack(
    c: ClientDep,
    username: str = Path(...),
    pack_id: int = Path(...),
):
    return _handle(lambda: c.get_pack(username=username, pack_id=pack_id))


# =============================================================================
# Forums & Topics
# =============================================================================

forums_tag = "Forums"


@app.get("/forums/sets", tags=[forums_tag], summary="Get forum sets for current user")
def get_forum_sets(c: ClientDep):
    return _handle(c.get_forum_sets)


@app.get("/forums/filtered-topics", tags=[forums_tag], summary="Get filtered topics across all forums")
def get_filtered_topics(
    c: ClientDep,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_filtered_topics(page=page, page_size=page_size))


@app.get("/forums/{forum_id}/topics", tags=[forums_tag], summary="Get topics in a forum")
def get_forum_topics(
    c: ClientDep,
    forum_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_forum_topics(forum_id=forum_id, page=page, page_size=page_size))


@app.get("/forum-posts/unread", tags=[forums_tag], summary="Get unread forum posts")
def get_unread_forum_posts(c: ClientDep):
    return _handle(c.get_unread_forum_posts)


@app.get("/forum-posts/{post_id}", tags=[forums_tag], summary="Get a forum post")
def get_forum_post(
    c: ClientDep,
    post_id: int = Path(...),
):
    return _handle(lambda: c.get_forum_post(post_id=post_id))


@app.get("/topics/{topic_id}", tags=[forums_tag], summary="Get topic details")
def get_topic(
    c: ClientDep,
    topic_id: int = Path(...),
):
    return _handle(lambda: c.get_topic(topic_id=topic_id))


@app.get("/topics/{topic_id}/posts", tags=[forums_tag], summary="Get posts in a topic")
def get_topic_posts(
    c: ClientDep,
    topic_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_topic_posts(topic_id=topic_id, page=page, page_size=page_size))


# =============================================================================
# Messages
# =============================================================================

messages_tag = "Messages"


@app.get("/messages", tags=[messages_tag], summary="List private messages")
def get_messages(
    c: ClientDep,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_messages(page=page, page_size=page_size))


@app.get("/messages/{message_id}", tags=[messages_tag], summary="Get a private message")
def get_message(
    c: ClientDep,
    message_id: int = Path(...),
):
    return _handle(lambda: c.get_message(message_id=message_id))


# =============================================================================
# Shops, Stores & Groups
# =============================================================================

shops_tag = "Shops & Groups"


@app.get("/shops/search", tags=[shops_tag], summary="Search shops")
def search_shops(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.search_shops(query=query, page=page, page_size=page_size))


@app.get("/shops/{shop_id}", tags=[shops_tag], summary="Get shop details")
def get_shop(
    c: ClientDep,
    shop_id: int = Path(...),
):
    return _handle(lambda: c.get_shop(shop_id=shop_id))


@app.get("/stores", tags=[shops_tag], summary="List stores")
def get_stores(c: ClientDep):
    return _handle(c.get_stores)


@app.get("/stores/{store_id}/products", tags=[shops_tag], summary="Get store products")
def get_store_products(
    c: ClientDep,
    store_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_store_products(store_id=store_id, page=page, page_size=page_size))


@app.get("/stores/{store_id}/purchases", tags=[shops_tag], summary="Get store purchases")
def get_store_purchases(
    c: ClientDep,
    store_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_store_purchases(store_id=store_id, page=page, page_size=page_size))


@app.get("/groups/search", tags=[shops_tag], summary="Search groups")
def search_groups(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.search_groups(query=query, page=page, page_size=page_size))


# =============================================================================
# Designers
# =============================================================================

designers_tag = "Designers"


@app.get("/designers/{designer_id}", tags=[designers_tag], summary="Get designer details")
def get_designer(
    c: ClientDep,
    designer_id: int = Path(...),
    include: Optional[str] = Query(None, description="Extra data to include (e.g. featured_bundles)"),
):
    return _handle(lambda: c.get_designer(designer_id=designer_id, include=include))


# =============================================================================
# Products & Deliveries
# =============================================================================

products_tag = "Products & Deliveries"


@app.get("/products/{product_id}", tags=[products_tag], summary="Get a product")
def get_product(
    c: ClientDep,
    product_id: int = Path(...),
):
    return _handle(lambda: c.get_product(product_id=product_id))


@app.get("/products/{product_id}/attachments", tags=[products_tag], summary="Get product attachments")
def get_product_attachments(
    c: ClientDep,
    product_id: int = Path(...),
):
    return _handle(lambda: c.get_product_attachments(product_id=product_id))


@app.get("/product-attachments/{attachment_id}", tags=[products_tag], summary="Get a product attachment")
def get_product_attachment(
    c: ClientDep,
    attachment_id: int = Path(...),
):
    return _handle(lambda: c.get_product_attachment(attachment_id=attachment_id))


@app.get("/deliveries", tags=[products_tag], summary="List deliveries (purchased/gifted products)")
def get_deliveries(
    c: ClientDep,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return _handle(lambda: c.get_deliveries(page=page, page_size=page_size))


# =============================================================================
# Draft Patterns, Volumes & Pages
# =============================================================================

drafts_tag = "Drafts & Volumes"


@app.get("/drafts/patterns", tags=[drafts_tag], summary="List draft patterns")
def get_draft_patterns(
    c: ClientDep,
    business_id: Optional[int] = Query(None),
):
    return _handle(lambda: c.get_draft_patterns(business_id=business_id))


@app.get("/drafts/patterns/{pattern_id}", tags=[drafts_tag], summary="Get a draft pattern")
def get_draft_pattern(
    c: ClientDep,
    pattern_id: int = Path(...),
):
    return _handle(lambda: c.get_draft_pattern(pattern_id=pattern_id))


@app.get("/volumes/{volume_id}", tags=[drafts_tag], summary="Get volume details")
def get_volume(
    c: ClientDep,
    volume_id: int = Path(...),
):
    return _handle(lambda: c.get_volume(volume_id=volume_id))


@app.get("/pages/{page_id}", tags=[drafts_tag], summary="Get a page")
def get_page(
    c: ClientDep,
    page_id: int = Path(...),
):
    return _handle(lambda: c.get_page(page_id=page_id))


# =============================================================================
# App Config
# =============================================================================

config_tag = "App Config"


@app.get("/app/config", tags=[config_tag], summary="Get application configuration")
def get_app_config(
    c: ClientDep,
    keys: Optional[str] = Query(None, description="Comma-separated config keys to retrieve"),
):
    return _handle(lambda: c.get_app_config(keys=keys))


@app.get("/app/data", tags=[config_tag], summary="Get app-specific user data")
def get_app_data(
    c: ClientDep,
    keys: Optional[str] = Query(None, description="Comma-separated data keys to retrieve"),
):
    return _handle(lambda: c.get_app_data(keys=keys))
