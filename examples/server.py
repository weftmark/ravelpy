"""
Ravelry API proxy server with interactive Swagger UI.

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
from pydantic import BaseModel

from ravelpy import RavelryAPIError, RavelryClient
from ravelpy.responses import (
    BundledItemResponse,
    BundleResponse,
    BundlesResponse,
    ColorFamiliesResponse,
    CommentsResponse,
    DeliveriesResponse,
    DraftPatternResponse,
    DraftPatternsResponse,
    FavoriteResponse,
    FavoritesResponse,
    FiberAttributeGroupsResponse,
    FiberAttributesResponse,
    FiberCategoriesResponse,
    FiberStashResponse,
    ForumPostResponse,
    ForumPostsResponse,
    ForumSetsResponse,
    FriendActivityResponse,
    FriendsResponse,
    GroupsResponse,
    LanguagesResponse,
    LibraryResponse,
    MessageResponse,
    MessagesResponse,
    NeedleSizesResponse,
    NeedlesResponse,
    NeedleTypesResponse,
    PackResponse,
    PageResponse,
    PatternAttributeGroupsResponse,
    PatternCategoriesResponse,
    PatternHighlightsResponse,
    PatternResponse,
    PatternSearchResponse,
    PatternSourceResponse,
    PatternSourcesSearchResponse,
    PatternSourceTypesResponse,
    PatternsMultiResponse,
    ProductAttachmentResponse,
    ProductAttachmentsResponse,
    ProductResponse,
    ProjectCraftsResponse,
    ProjectResponse,
    ProjectsResponse,
    ProjectStatusesResponse,
    QueuedProjectResponse,
    QueueResponse,
    SavedSearchesResponse,
    ShopResponse,
    ShopsResponse,
    StashListResponse,
    StashResponse,
    StoreProductsResponse,
    StoresResponse,
    TopicResponse,
    TopicsResponse,
    ForumPostsResponse,
    UnifiedStashResponse,
    UserResponse,
    VolumeResponse,
    YarnAttributeGroupsResponse,
    YarnCompaniesResponse,
    YarnResponse,
    YarnSearchResponse,
    YarnsMultiResponse,
    YarnWeightsResponse,
)

load_dotenv()

_TAGS = [
    {"name": "App"},
    {"name": "Bundled Items"},
    {"name": "Bundles"},
    {"name": "Deliveries"},
    {"name": "Designers"},
    {"name": "Drafts"},
    {"name": "Extras"},
    {"name": "Favorites"},
    {"name": "Fiber"},
    {"name": "Fiber Attribute Groups"},
    {"name": "Forums"},
    {"name": "Friends"},
    {"name": "Groups"},
    {"name": "Languages"},
    {"name": "Library"},
    {"name": "Messages"},
    {"name": "Needles"},
    {"name": "Pages"},
    {"name": "Packs"},
    {"name": "Pattern Attributes"},
    {"name": "Pattern Categories"},
    {"name": "Pattern Source Types"},
    {"name": "Pattern Sources"},
    {"name": "Patterns"},
    {"name": "People"},
    {"name": "Photos"},
    {"name": "Product Attachments"},
    {"name": "Products"},
    {"name": "Projects"},
    {"name": "Queue"},
    {"name": "Saved Searches"},
    {"name": "Shops"},
    {"name": "Stash"},
    {"name": "Stores"},
    {"name": "Topics"},
    {"name": "Volumes"},
    {"name": "Yarn Attributes"},
    {"name": "Yarn Companies"},
    {"name": "Yarns"},
]

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
    openapi_tags=_TAGS,
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


async def _handle(fn):
    """Wrap a client call, unpack the (parsed, etag, raw) tuple, and convert RavelryAPIError to HTTPException."""
    try:
        data, _etag, _raw = await fn()
        return data
    except RavelryAPIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


# =============================================================================
# Extras (reference data + global search)
# =============================================================================

extras_tag = "Extras"


@app.get("/color-families", tags=[extras_tag], summary="List color families", response_model=ColorFamiliesResponse)
async def get_color_families(c: ClientDep):
    return await _handle(c.extras.color_families)


@app.get("/search", tags=[extras_tag], summary="Global search")
async def global_search(
    c: ClientDep,
    query: str = Query(..., description="Search query string"),
    types: Optional[str] = Query(None, description="Comma-separated resource types (e.g. patterns,yarns)"),
    limit: Optional[int] = Query(None, description="Maximum number of results"),
):
    return await _handle(lambda: c.extras.search(query=query, types=types, limit=limit))


# =============================================================================
# Fiber Attribute Groups
# =============================================================================

fiber_attr_tag = "Fiber Attribute Groups"


@app.get("/fiber-attribute-groups", tags=[fiber_attr_tag], summary="List fiber attribute groups", response_model=FiberAttributeGroupsResponse)
async def get_fiber_attribute_groups(c: ClientDep):
    return await _handle(c.fiber_attribute_groups.list)


@app.get("/fiber-attributes", tags=[fiber_attr_tag], summary="List fiber attributes", response_model=FiberAttributesResponse)
async def get_fiber_attributes(c: ClientDep):
    return await _handle(c.fiber_attribute_groups.attributes)


@app.get("/fiber-categories", tags=[fiber_attr_tag], summary="List fiber categories", response_model=FiberCategoriesResponse)
async def get_fiber_categories(c: ClientDep):
    return await _handle(c.fiber_attribute_groups.categories)


# =============================================================================
# Yarn Attributes
# =============================================================================

yarn_attr_tag = "Yarn Attributes"


@app.get("/yarn-attributes", tags=[yarn_attr_tag], summary="List yarn attribute groups", response_model=YarnAttributeGroupsResponse)
async def get_yarn_attributes(c: ClientDep):
    return await _handle(c.yarn_attributes.groups)


@app.get("/yarn-weights", tags=[yarn_attr_tag], summary="List yarn weights", response_model=YarnWeightsResponse)
async def get_yarn_weights(c: ClientDep):
    return await _handle(c.yarn_attributes.weights)


# =============================================================================
# Languages
# =============================================================================

languages_tag = "Languages"


@app.get("/languages", tags=[languages_tag], summary="List available languages", response_model=LanguagesResponse)
async def get_languages(c: ClientDep):
    return await _handle(c.languages.list)


# =============================================================================
# Needles
# =============================================================================

needles_tag = "Needles"


@app.get("/people/{username}/needles", tags=[needles_tag], summary="List a user's needle records", response_model=NeedlesResponse)
async def get_needles(c: ClientDep, username: str = Path(...)):
    return await _handle(lambda: c.needles.list(username=username))


@app.get("/needles/sizes", tags=[needles_tag], summary="List needle sizes", response_model=NeedleSizesResponse)
async def get_needle_sizes(c: ClientDep):
    return await _handle(c.needles.sizes)


@app.get("/needles/types", tags=[needles_tag], summary="List needle types", response_model=NeedleTypesResponse)
async def get_needle_types(c: ClientDep):
    return await _handle(c.needles.types)


# =============================================================================
# Pattern Attributes
# =============================================================================

pattern_attr_tag = "Pattern Attributes"


@app.get("/pattern-attributes", tags=[pattern_attr_tag], summary="List pattern attribute groups", response_model=PatternAttributeGroupsResponse)
async def get_pattern_attributes(c: ClientDep):
    return await _handle(c.pattern_attributes.groups)


# =============================================================================
# Pattern Categories
# =============================================================================

pattern_cat_tag = "Pattern Categories"


@app.get("/pattern-categories", tags=[pattern_cat_tag], summary="List pattern categories", response_model=PatternCategoriesResponse)
async def get_pattern_categories(c: ClientDep):
    return await _handle(c.pattern_categories.list)


# =============================================================================
# Pattern Source Types
# =============================================================================

pattern_src_type_tag = "Pattern Source Types"


@app.get("/pattern-source-types", tags=[pattern_src_type_tag], summary="List pattern source types", response_model=PatternSourceTypesResponse)
async def get_pattern_source_types(c: ClientDep):
    return await _handle(c.pattern_source_types.list)


# =============================================================================
# Pattern Sources
# =============================================================================

pattern_sources_tag = "Pattern Sources"


@app.get("/pattern-sources/search", tags=[pattern_sources_tag], summary="Search pattern sources", response_model=PatternSourcesSearchResponse)
async def search_pattern_sources(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.pattern_sources.search(query=query, page=page, page_size=page_size))


@app.get("/pattern-sources/{source_id}", tags=[pattern_sources_tag], summary="Get a pattern source", response_model=PatternSourceResponse)
async def get_pattern_source(
    c: ClientDep,
    source_id: int = Path(...),
):
    return await _handle(lambda: c.pattern_sources.show(source_id=source_id))


@app.get("/pattern-sources/{source_id}/patterns", tags=[pattern_sources_tag], summary="Get patterns from a source", response_model=PatternSearchResponse)
async def get_pattern_source_patterns(
    c: ClientDep,
    source_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.pattern_sources.patterns(source_id=source_id, page=page, page_size=page_size))


# =============================================================================
# Patterns
# =============================================================================

patterns_tag = "Patterns"


@app.get("/patterns/search", tags=[patterns_tag], summary="Search patterns", response_model=PatternSearchResponse)
async def search_patterns(
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
    return await _handle(lambda: c.patterns.search(
        query=query, page=page, page_size=page_size, sort=sort,
        craft=craft, weight=weight, colors=colors, fit=fit, gender=gender,
        availability=availability, language=language,
    ))


@app.get("/patterns/highlights", tags=[patterns_tag], summary="Get pattern highlights", response_model=PatternHighlightsResponse)
async def get_pattern_highlights(c: ClientDep):
    return await _handle(c.patterns.highlights)


@app.get("/patterns/multi", tags=[patterns_tag], summary="Get multiple patterns by ID", response_model=PatternsMultiResponse)
async def get_patterns(
    c: ClientDep,
    ids: str = Query(..., description="Comma-separated pattern IDs"),
):
    return await _handle(lambda: c.patterns.list(ids=ids))


@app.get("/patterns/{pattern_id}", tags=[patterns_tag], summary="Get a pattern", response_model=PatternResponse)
async def get_pattern(
    c: ClientDep,
    pattern_id: int = Path(...),
):
    return await _handle(lambda: c.patterns.show(pattern_id=pattern_id))


@app.get("/patterns/{pattern_id}/comments", tags=[patterns_tag], summary="Get pattern comments", response_model=CommentsResponse)
async def get_pattern_comments(
    c: ClientDep,
    pattern_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    return await _handle(lambda: c.patterns.comments(pattern_id=pattern_id, page=page, page_size=page_size, sort=sort))


@app.get("/patterns/{pattern_id}/projects", tags=[patterns_tag], summary="Get projects linked to a pattern", response_model=ProjectsResponse)
async def get_pattern_projects(
    c: ClientDep,
    pattern_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.patterns.projects(pattern_id=pattern_id, page=page, page_size=page_size))


# =============================================================================
# Yarns
# =============================================================================

yarns_tag = "Yarns"


@app.get("/yarns/search", tags=[yarns_tag], summary="Search yarns", response_model=YarnSearchResponse)
async def search_yarns(
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
    return await _handle(lambda: c.yarns.search(
        query=query, page=page, page_size=page_size, sort=sort, weight=weight,
        fiber_min_weight_pct=fiber_min_weight_pct, color_family_id=color_family_id,
        fiber_category_id=fiber_category_id, discontinued=discontinued,
        personal_attributes=personal_attributes,
    ))


@app.get("/yarns/multi", tags=[yarns_tag], summary="Get multiple yarns by ID", response_model=YarnsMultiResponse)
async def get_yarns(
    c: ClientDep,
    ids: str = Query(..., description="Comma-separated yarn IDs"),
):
    return await _handle(lambda: c.yarns.list(ids=ids))


@app.get("/yarns/{yarn_id}", tags=[yarns_tag], summary="Get a yarn", response_model=YarnResponse)
async def get_yarn(
    c: ClientDep,
    yarn_id: int = Path(...),
):
    return await _handle(lambda: c.yarns.show(yarn_id=yarn_id))


@app.get("/yarns/{yarn_id}/comments", tags=[yarns_tag], summary="Get yarn comments", response_model=CommentsResponse)
async def get_yarn_comments(
    c: ClientDep,
    yarn_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    return await _handle(lambda: c.yarns.comments(yarn_id=yarn_id, page=page, page_size=page_size, sort=sort))


# =============================================================================
# Yarn Companies
# =============================================================================

yarn_co_tag = "Yarn Companies"


@app.get("/yarn-companies/search", tags=[yarn_co_tag], summary="Search yarn companies", response_model=YarnCompaniesResponse)
async def search_yarn_companies(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.yarn_companies.search(query=query, page=page, page_size=page_size))


# =============================================================================
# People
# =============================================================================

people_tag = "People"


@app.get("/current-user", tags=[people_tag], summary="Get authenticated user profile", response_model=UserResponse)
async def get_current_user(c: ClientDep):
    return await _handle(c.people.me)


@app.get("/people/{username}", tags=[people_tag], summary="Get a user's profile", response_model=UserResponse)
async def get_person(
    c: ClientDep,
    username: str = Path(...),
):
    return await _handle(lambda: c.people.show(username=username))


@app.get("/people/{username}/comments", tags=[people_tag], summary="List comments by a user", response_model=CommentsResponse)
async def get_person_comments(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.people.comments(username=username, page=page, page_size=page_size))


# =============================================================================
# Friends
# =============================================================================

friends_tag = "Friends"


@app.get("/people/{username}/friends", tags=[friends_tag], summary="List a user's friends", response_model=FriendsResponse)
async def get_friends(
    c: ClientDep,
    username: str = Path(...),
):
    return await _handle(lambda: c.friends.list(username=username))


@app.get("/people/{username}/friends/activity", tags=[friends_tag], summary="Get friends' recent activity", response_model=FriendActivityResponse)
async def get_friends_activity(
    c: ClientDep,
    username: str = Path(...),
):
    return await _handle(lambda: c.friends.activity(username=username))


# =============================================================================
# Saved Searches
# =============================================================================

saved_searches_tag = "Saved Searches"


@app.get("/saved-searches", tags=[saved_searches_tag], summary="List saved searches for the authenticated user", response_model=SavedSearchesResponse)
async def get_saved_searches(c: ClientDep):
    return await _handle(c.saved_searches.list)


# =============================================================================
# Library
# =============================================================================

library_tag = "Library"


@app.get("/people/{username}/library/search", tags=[library_tag], summary="Search a user's library", response_model=LibraryResponse)
async def search_library(
    c: ClientDep,
    username: str = Path(...),
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.library.search(username=username, query=query, page=page, page_size=page_size))


# =============================================================================
# Projects
# =============================================================================

projects_tag = "Projects"


@app.get("/projects/search", tags=[projects_tag], summary="Search the project database", response_model=ProjectsResponse)
async def search_projects(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    craft: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    return await _handle(lambda: c.projects.search(query=query, page=page, page_size=page_size, craft=craft, status=status))


@app.get("/projects/crafts", tags=[projects_tag], summary="List valid project crafts", response_model=ProjectCraftsResponse)
async def get_project_crafts(c: ClientDep):
    return await _handle(c.projects.crafts)


@app.get("/projects/statuses", tags=[projects_tag], summary="List valid project statuses", response_model=ProjectStatusesResponse)
async def get_project_statuses(c: ClientDep):
    return await _handle(c.projects.statuses)


@app.get("/people/{username}/projects", tags=[projects_tag], summary="List a user's projects", response_model=ProjectsResponse)
async def get_projects(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.projects.list(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/projects/{project_id}", tags=[projects_tag], summary="Get a user's project", response_model=ProjectResponse)
async def get_project(
    c: ClientDep,
    username: str = Path(...),
    project_id: int = Path(...),
):
    return await _handle(lambda: c.projects.show(username=username, project_id=project_id))


@app.get("/people/{username}/projects/{project_id}/comments", tags=[projects_tag], summary="Get project comments", response_model=CommentsResponse)
async def get_project_comments(
    c: ClientDep,
    username: str = Path(...),
    project_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.projects.comments(username=username, project_id=project_id, page=page, page_size=page_size))


# =============================================================================
# Stash
# =============================================================================

stash_tag = "Stash"


class StashCreateIn(BaseModel):
    yarn_id: int
    colorway_name: Optional[str] = None
    dye_lot: Optional[str] = None
    notes: Optional[str] = None
    stash_status_id: Optional[int] = None
    skeins: Optional[float] = None
    grams_per_skein: Optional[float] = None
    yards_per_skein: Optional[float] = None


@app.get("/people/{username}/stash", tags=[stash_tag], summary="List a user's stash", response_model=StashListResponse)
async def get_stash_list(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.stash.list(username=username, page=page, page_size=page_size))


@app.post("/people/{username}/stash", tags=[stash_tag], summary="Create a stash entry", response_model=StashResponse)
async def create_stash(
    c: ClientDep,
    username: str = Path(...),
    body: StashCreateIn = ...,
):
    return await _handle(lambda: c.stash.create(username, body.model_dump(exclude_none=True)))


@app.get("/people/{username}/stash/search", tags=[stash_tag], summary="Search a user's stash", response_model=StashListResponse)
async def search_stash(
    c: ClientDep,
    username: str = Path(...),
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.stash.search(username=username, query=query, page=page, page_size=page_size))


@app.get("/people/{username}/stash/unified", tags=[stash_tag], summary="Get unified stash (yarn + fiber)", response_model=UnifiedStashResponse)
async def get_unified_stash(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.stash.unified(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/stash/{stash_id}", tags=[stash_tag], summary="Get a stash record", response_model=StashResponse)
async def get_stash(
    c: ClientDep,
    username: str = Path(...),
    stash_id: int = Path(...),
):
    return await _handle(lambda: c.stash.show(username=username, stash_id=stash_id))


@app.get("/people/{username}/stash/{stash_id}/comments", tags=[stash_tag], summary="Get stash comments", response_model=CommentsResponse)
async def get_stash_comments(
    c: ClientDep,
    username: str = Path(...),
    stash_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.stash.comments(username=username, stash_id=stash_id, page=page, page_size=page_size))


# =============================================================================
# Queue
# =============================================================================

queue_tag = "Queue"


@app.get("/people/{username}/queue", tags=[queue_tag], summary="List a user's queue", response_model=QueueResponse)
async def get_queue(
    c: ClientDep,
    username: str = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.queue.list(username=username, page=page, page_size=page_size))


@app.get("/people/{username}/queue/{queue_id}", tags=[queue_tag], summary="Get a queued project", response_model=QueuedProjectResponse)
async def get_queue_item(
    c: ClientDep,
    username: str = Path(...),
    queue_id: int = Path(...),
):
    return await _handle(lambda: c.queue.show(username=username, queue_id=queue_id))


# =============================================================================
# Favorites
# =============================================================================

favorites_tag = "Favorites"


@app.get("/people/{username}/favorites", tags=[favorites_tag], summary="List a user's favorites", response_model=FavoritesResponse)
async def get_favorites(
    c: ClientDep,
    username: str = Path(...),
    types: Optional[str] = Query(None, description="Resource types to filter (e.g. pattern, yarn)"),
    query: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.favorites.list(
        username=username, types=types, query=query, tag=tag, page=page, page_size=page_size,
    ))


@app.get("/people/{username}/favorites/{favorite_id}", tags=[favorites_tag], summary="Get a single favorite", response_model=FavoriteResponse)
async def get_favorite(
    c: ClientDep,
    username: str = Path(...),
    favorite_id: int = Path(...),
):
    return await _handle(lambda: c.favorites.show(username=username, favorite_id=favorite_id))


# =============================================================================
# Fiber
# =============================================================================

fiber_tag = "Fiber"


@app.get("/people/{username}/fiber/{fiber_id}", tags=[fiber_tag], summary="Get a fiber stash record", response_model=FiberStashResponse)
async def get_fiber(
    c: ClientDep,
    username: str = Path(...),
    fiber_id: int = Path(...),
):
    return await _handle(lambda: c.fiber.show(username=username, fiber_id=fiber_id))


@app.get("/people/{username}/fiber/{fiber_id}/comments", tags=[fiber_tag], summary="Get fiber stash comments", response_model=CommentsResponse)
async def get_fiber_comments(
    c: ClientDep,
    username: str = Path(...),
    fiber_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    sort: Optional[str] = Query(None),
):
    return await _handle(lambda: c.fiber.comments(username=username, fiber_id=fiber_id, page=page, page_size=page_size, sort=sort))


# =============================================================================
# Bundles
# =============================================================================

bundles_tag = "Bundles"


@app.get("/people/{username}/bundles", tags=[bundles_tag], summary="List a user's bundles", response_model=BundlesResponse)
async def get_bundles(
    c: ClientDep,
    username: str = Path(...),
    owner_types: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.bundles.list(
        username=username, owner_types=owner_types, query=query, page=page, page_size=page_size,
    ))


@app.get("/people/{username}/bundles/{bundle_id}", tags=[bundles_tag], summary="Get a bundle", response_model=BundleResponse)
async def get_bundle(
    c: ClientDep,
    username: str = Path(...),
    bundle_id: int = Path(...),
):
    return await _handle(lambda: c.bundles.show(username=username, bundle_id=bundle_id))


# =============================================================================
# Bundled Items
# =============================================================================

bundled_items_tag = "Bundled Items"


@app.get("/bundled-items/{bundled_item_id}", tags=[bundled_items_tag], summary="Get a single bundled item", response_model=BundledItemResponse)
async def get_bundled_item(
    c: ClientDep,
    bundled_item_id: int = Path(...),
):
    return await _handle(lambda: c.bundled_items.show(bundled_item_id=bundled_item_id))


# =============================================================================
# Packs
# =============================================================================

packs_tag = "Packs"


@app.get("/packs/{pack_id}", tags=[packs_tag], summary="Get a pack", response_model=PackResponse)
async def get_pack(
    c: ClientDep,
    pack_id: int = Path(...),
):
    return await _handle(lambda: c.packs.show(pack_id=pack_id))


# =============================================================================
# Forums
# =============================================================================

forums_tag = "Forums"


@app.get("/forums/sets", tags=[forums_tag], summary="Get forum sets for current user", response_model=ForumSetsResponse)
async def get_forum_sets(c: ClientDep):
    return await _handle(c.forums.sets)


@app.get("/forums/filtered-topics", tags=[forums_tag], summary="Get filtered topics across all forums", response_model=TopicsResponse)
async def get_filtered_topics(
    c: ClientDep,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.forums.filtered_topics(page=page, page_size=page_size))


@app.get("/forums/{forum_id}/topics", tags=[forums_tag], summary="Get topics in a forum", response_model=TopicsResponse)
async def get_forum_topics(
    c: ClientDep,
    forum_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.forums.topics(forum_id=forum_id, page=page, page_size=page_size))


@app.get("/forum-posts/unread", tags=[forums_tag], summary="Get unread forum posts", response_model=ForumPostsResponse)
async def get_unread_forum_posts(c: ClientDep):
    return await _handle(c.forums.unread_posts)


@app.get("/forum-posts/{post_id}", tags=[forums_tag], summary="Get a forum post", response_model=ForumPostResponse)
async def get_forum_post(
    c: ClientDep,
    post_id: int = Path(...),
):
    return await _handle(lambda: c.forums.post(post_id=post_id))


# =============================================================================
# Topics
# =============================================================================

topics_tag = "Topics"


@app.get("/topics/{topic_id}", tags=[topics_tag], summary="Get topic details", response_model=TopicResponse)
async def get_topic(
    c: ClientDep,
    topic_id: int = Path(...),
):
    return await _handle(lambda: c.topics.show(topic_id=topic_id))


@app.get("/topics/{topic_id}/posts", tags=[topics_tag], summary="Get posts in a topic", response_model=ForumPostsResponse)
async def get_topic_posts(
    c: ClientDep,
    topic_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.topics.posts(topic_id=topic_id, page=page, page_size=page_size))


# =============================================================================
# Messages
# =============================================================================

messages_tag = "Messages"


@app.get("/messages", tags=[messages_tag], summary="List private messages", response_model=MessagesResponse)
async def get_messages(
    c: ClientDep,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.messages.list(page=page, page_size=page_size))


@app.get("/messages/{message_id}", tags=[messages_tag], summary="Get a private message", response_model=MessageResponse)
async def get_message(
    c: ClientDep,
    message_id: int = Path(...),
):
    return await _handle(lambda: c.messages.show(message_id=message_id))


# =============================================================================
# Shops
# =============================================================================

shops_tag = "Shops"


@app.get("/shops/search", tags=[shops_tag], summary="Search shops", response_model=ShopsResponse)
async def search_shops(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.shops.search(query=query, page=page, page_size=page_size))


@app.get("/shops/{shop_id}", tags=[shops_tag], summary="Get shop details", response_model=ShopResponse)
async def get_shop(
    c: ClientDep,
    shop_id: int = Path(...),
):
    return await _handle(lambda: c.shops.show(shop_id=shop_id))


# =============================================================================
# Stores
# =============================================================================

stores_tag = "Stores"


@app.get("/stores", tags=[stores_tag], summary="List stores", response_model=StoresResponse)
async def get_stores(c: ClientDep):
    return await _handle(c.stores.list)


@app.get("/stores/{store_id}/products", tags=[stores_tag], summary="Get store products", response_model=StoreProductsResponse)
async def get_store_products(
    c: ClientDep,
    store_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.stores.products(store_id=store_id, page=page, page_size=page_size))


@app.get("/stores/{store_id}/purchases", tags=[stores_tag], summary="Get store purchases")
async def get_store_purchases(
    c: ClientDep,
    store_id: int = Path(...),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.stores.purchases(store_id=store_id, page=page, page_size=page_size))


# =============================================================================
# Groups
# =============================================================================

groups_tag = "Groups"


@app.get("/groups/search", tags=[groups_tag], summary="Search groups", response_model=GroupsResponse)
async def search_groups(
    c: ClientDep,
    query: Optional[str] = Query(None),
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.groups.search(query=query, page=page, page_size=page_size))


# =============================================================================
# Designers
# =============================================================================

designers_tag = "Designers"


@app.get("/designers/{designer_id}", tags=[designers_tag], summary="Get designer details")
async def get_designer(
    c: ClientDep,
    designer_id: int = Path(...),
    include: Optional[str] = Query(None, description="Extra data to include (e.g. featured_bundles)"),
):
    return await _handle(lambda: c.designers.show(designer_id=designer_id, include=include))


# =============================================================================
# Products
# =============================================================================

products_tag = "Products"


@app.get("/products/{product_id}", tags=[products_tag], summary="Get a product", response_model=ProductResponse)
async def get_product(
    c: ClientDep,
    product_id: int = Path(...),
):
    return await _handle(lambda: c.products.show(product_id=product_id))


@app.get("/products/{product_id}/attachments", tags=[products_tag], summary="Get product attachments", response_model=ProductAttachmentsResponse)
async def get_product_attachments(
    c: ClientDep,
    product_id: int = Path(...),
):
    return await _handle(lambda: c.products.attachments(product_id=product_id))


# =============================================================================
# Product Attachments
# =============================================================================

product_attach_tag = "Product Attachments"


@app.get("/product-attachments/{attachment_id}", tags=[product_attach_tag], summary="Get a product attachment", response_model=ProductAttachmentResponse)
async def get_product_attachment(
    c: ClientDep,
    attachment_id: int = Path(...),
):
    return await _handle(lambda: c.product_attachments.show(attachment_id=attachment_id))


# =============================================================================
# Deliveries
# =============================================================================

deliveries_tag = "Deliveries"


@app.get("/deliveries", tags=[deliveries_tag], summary="List deliveries (purchased/gifted products)", response_model=DeliveriesResponse)
async def get_deliveries(
    c: ClientDep,
    page: Optional[int] = Query(None, ge=1),
    page_size: Optional[int] = Query(None, ge=1, le=100),
):
    return await _handle(lambda: c.deliveries.list(page=page, page_size=page_size))


# =============================================================================
# Drafts
# =============================================================================

drafts_tag = "Drafts"


@app.get("/drafts/patterns", tags=[drafts_tag], summary="List draft patterns", response_model=DraftPatternsResponse)
async def get_draft_patterns(
    c: ClientDep,
    business_id: Optional[int] = Query(None),
):
    return await _handle(lambda: c.drafts.list(business_id=business_id))


@app.get("/drafts/patterns/{pattern_id}", tags=[drafts_tag], summary="Get a draft pattern", response_model=DraftPatternResponse)
async def get_draft_pattern(
    c: ClientDep,
    pattern_id: int = Path(...),
):
    return await _handle(lambda: c.drafts.show(pattern_id=pattern_id))


# =============================================================================
# Volumes
# =============================================================================

volumes_tag = "Volumes"


@app.get("/volumes/{volume_id}", tags=[volumes_tag], summary="Get volume details", response_model=VolumeResponse)
async def get_volume(
    c: ClientDep,
    volume_id: int = Path(...),
):
    return await _handle(lambda: c.volumes.show(volume_id=volume_id))


# =============================================================================
# Pages
# =============================================================================

pages_tag = "Pages"


@app.get("/pages/{page_id}", tags=[pages_tag], summary="Get a page", response_model=PageResponse)
async def get_page(
    c: ClientDep,
    page_id: int = Path(...),
):
    return await _handle(lambda: c.pages.show(page_id=page_id))


# =============================================================================
# Photos
# =============================================================================

photos_tag = "Photos"


@app.get("/photos/dimensions", tags=[photos_tag], summary="List photo thumbnail dimensions")
async def get_photo_dimensions(c: ClientDep):
    return await _handle(c.photos.dimensions)


@app.get("/photos/{photo_id}/sizes", tags=[photos_tag], summary="List available sizes for a photo")
async def get_photo_sizes(c: ClientDep, photo_id: int = Path(...)):
    return await _handle(lambda: c.photos.sizes(photo_id=photo_id))


# =============================================================================
# App Config
# =============================================================================

app_tag = "App"


@app.get("/app/config", tags=[app_tag], summary="Get application configuration")
async def get_app_config(
    c: ClientDep,
    keys: Optional[str] = Query(None, description="Comma-separated config keys to retrieve"),
):
    return await _handle(lambda: c.app.config(keys=keys))


@app.get("/app/data", tags=[app_tag], summary="Get app-specific user data")
async def get_app_data(
    c: ClientDep,
    keys: Optional[str] = Query(None, description="Comma-separated data keys to retrieve"),
):
    return await _handle(lambda: c.app.data(keys=keys))