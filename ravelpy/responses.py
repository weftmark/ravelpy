"""Pydantic response envelope models that mirror the top-level JSON objects returned by the Ravelry API.

Each class wraps one or more entity models from :mod:`ravelpy.models` in the
same structure the API sends over the wire.  These models are used both to
parse :meth:`~ravelpy.resources.base.Resource._get` responses and to drive
FastAPI ``response_model=`` for Swagger schema generation.

:class:`Paginator` is shared across all paginated list responses.
"""

from typing import Optional
from pydantic import BaseModel

from .models import (
    Activity,
    AttributeGroup,
    Bookmark,
    Bundle,
    BundledItem,
    ColorFamily,
    Colorway,
    Comment,
    Craft,
    Delivery,
    DraftPattern,
    FiberAttribute,
    FiberAttributeGroup,
    FiberCategory,
    FiberStash,
    ForumPost,
    ForumSet,
    Friendship,
    Group,
    Language,
    Message,
    NeedleRecord,
    NeedleSize,
    NeedleType,
    Pack,
    Page,
    Pattern,
    PatternCategory,
    PatternSource,
    PatternSourceType,
    Product,
    ProductAttachment,
    Project,
    ProjectStatus,
    QueuedProject,
    SavedSearch,
    Shop,
    Stash,
    Store,
    Topic,
    UnifiedStash,
    User,
    Volume,
    Yarn,
    YarnAttributeGroup,
    YarnCompany,
    YarnWeight,
)


class Paginator(BaseModel):
    """Pagination metadata included in list and search responses."""

    page: Optional[int] = None
    page_count: Optional[int] = None
    page_size: Optional[int] = None
    results: Optional[int] = None
    last_page: Optional[bool] = None


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------


class ColorFamiliesResponse(BaseModel):
    """Response envelope for ``GET /color_families.json``."""

    color_families: list[ColorFamily]


class FiberAttributeGroupsResponse(BaseModel):
    """Response envelope for ``GET /fiber_attribute_groups/list.json``."""

    fiber_attribute_groups: list[FiberAttributeGroup]


class FiberAttributesResponse(BaseModel):
    """Response envelope for ``GET /fiber_attributes.json``."""

    fiber_attributes: list[FiberAttribute]


class FiberCategoriesResponse(BaseModel):
    """Response envelope for ``GET /fiber_categories.json``."""

    fiber_categories: list[FiberCategory]


class YarnAttributeGroupsResponse(BaseModel):
    """Response envelope for ``GET /yarn_attributes/groups.json``."""

    yarn_attribute_groups: list[YarnAttributeGroup]


class YarnWeightsResponse(BaseModel):
    """Response envelope for ``GET /yarn_weights.json``."""

    yarn_weights: list[YarnWeight]


class LanguagesResponse(BaseModel):
    """Response envelope for ``GET /languages/list.json``."""

    languages: list[Language]


class NeedlesResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/needles/list.json``."""

    needles: list[NeedleRecord]


class NeedleSizesResponse(BaseModel):
    """Response envelope for ``GET /needles/sizes.json``."""

    needle_sizes: list[NeedleSize]


class NeedleTypesResponse(BaseModel):
    """Response envelope for ``GET /needles/types.json``."""

    needle_types: list[NeedleType]


class PatternAttributeGroupsResponse(BaseModel):
    """Response envelope for ``GET /pattern_attributes/groups.json``."""

    attribute_groups: list[AttributeGroup]


class PatternCategoriesResponse(BaseModel):
    """Response envelope for ``GET /pattern_categories/list.json``."""

    pattern_categories: list[PatternCategory]


class PatternSourceTypesResponse(BaseModel):
    """Response envelope for ``GET /pattern_source_types/list.json``."""

    pattern_source_types: list[PatternSourceType]


class ProjectCraftsResponse(BaseModel):
    """Response envelope for ``GET /projects/crafts.json``."""

    crafts: list[Craft]


class ProjectStatusesResponse(BaseModel):
    """Response envelope for ``GET /projects/project_statuses.json``."""

    project_statuses: list[ProjectStatus]


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------


class PatternResponse(BaseModel):
    """Response envelope for ``GET /patterns/{id}.json``."""

    pattern: Pattern


class PatternsMultiResponse(BaseModel):
    """Response envelope for ``GET /patterns.json`` (multi-fetch by ID)."""

    patterns: dict[str, Pattern]


class PatternSearchResponse(BaseModel):
    """Response envelope for ``GET /patterns/search.json``."""

    patterns: list[Pattern]
    paginator: Optional[Paginator] = None


class PatternHighlightsResponse(BaseModel):
    """Response envelope for ``GET /patterns/highlights.json``."""

    patterns: list[Pattern]


class PatternSourceResponse(BaseModel):
    """Response envelope for ``GET /pattern_sources/{id}.json``."""

    pattern_source: PatternSource


class PatternSourcesSearchResponse(BaseModel):
    """Response envelope for ``GET /pattern_sources/search.json``."""

    pattern_sources: list[PatternSource]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Yarns
# ---------------------------------------------------------------------------


class YarnResponse(BaseModel):
    """Response envelope for ``GET /yarns/{id}.json``."""

    yarn: Yarn
    colorways: Optional[list[Colorway]] = None  # present when include="colorways"


class YarnsMultiResponse(BaseModel):
    """Response envelope for ``GET /yarns.json`` (multi-fetch by ID)."""

    yarns: dict[str, Yarn]


class YarnSearchResponse(BaseModel):
    """Response envelope for ``GET /yarns/search.json``."""

    yarns: list[Yarn]
    paginator: Optional[Paginator] = None


class YarnCompaniesResponse(BaseModel):
    """Response envelope for ``GET /yarn_companies/search.json``."""

    yarn_companies: list[YarnCompany]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------


class CommentsResponse(BaseModel):
    """Response envelope for comment list sub-resources (patterns, yarns, projects, etc.)."""

    comments: list[Comment]


# ---------------------------------------------------------------------------
# People / social
# ---------------------------------------------------------------------------


class UserResponse(BaseModel):
    """Response envelope for ``GET /people/{username}.json``."""

    user: User


class FriendsResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/friends/list.json``."""

    users: list[User]


class FriendActivityResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/friends/activity.json``."""

    activities: list[Activity]


class SavedSearchesResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/saved_searches/list.json``."""

    saved_searches: list[SavedSearch]


class LibraryResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/library/search.json``."""

    volumes: list[Volume]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


class ProjectResponse(BaseModel):
    """Response envelope for ``GET /projects/{username}/{id}.json``."""

    project: Project


class ProjectsResponse(BaseModel):
    """Response envelope for ``GET /projects/search.json`` and related project list endpoints."""

    projects: list[Project]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Stash
# ---------------------------------------------------------------------------


class StashResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/stash/{id}.json``."""

    stash: Stash


class StashListResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/stash/list.json``."""

    stash: list[Stash]
    paginator: Optional[Paginator] = None


class UnifiedStashResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/stash/unified.json``."""

    stash: list[UnifiedStash]


# ---------------------------------------------------------------------------
# Queue
# ---------------------------------------------------------------------------


class QueuedProjectResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/queue/{id}.json``."""

    queued_project: QueuedProject


class QueueResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/queue/list.json``."""

    queued_projects: list[QueuedProject]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Favorites
# ---------------------------------------------------------------------------


class FavoriteResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/favorites/{id}.json``."""

    favorite: Bookmark


class FavoritesResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/favorites/list.json``."""

    favorites: list[Bookmark]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Fiber stash
# ---------------------------------------------------------------------------


class FiberStashResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/fiber/{id}.json``."""

    fiber: FiberStash


# ---------------------------------------------------------------------------
# Bundles / packs
# ---------------------------------------------------------------------------


class BundleResponse(BaseModel):
    """Response envelope for ``GET /bundles/{id}.json``."""

    bundle: Bundle


class BundlesResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/bundles/list.json``."""

    bundles: list[Bundle]
    paginator: Optional[Paginator] = None


class BundledItemResponse(BaseModel):
    """Response envelope for ``POST /bundles/{id}/items.json``."""

    bundled_item: BundledItem


class PackResponse(BaseModel):
    """Response envelope for ``GET /packs/{id}.json``."""

    pack: Pack


# ---------------------------------------------------------------------------
# Forums / topics
# ---------------------------------------------------------------------------


class ForumSetsResponse(BaseModel):
    """Response envelope for ``GET /forums/sets.json``."""

    forum_sets: list[ForumSet]


class TopicsResponse(BaseModel):
    """Response envelope for ``GET /forums/{forum_id}/topics.json``."""

    topics: list[Topic]
    paginator: Optional[Paginator] = None


class TopicResponse(BaseModel):
    """Response envelope for ``GET /topics/{id}.json``."""

    topic: Topic


class ForumPostsResponse(BaseModel):
    """Response envelope for ``GET /topics/{id}/posts.json``."""

    forum_posts: list[ForumPost]
    paginator: Optional[Paginator] = None


class ForumPostResponse(BaseModel):
    """Response envelope for ``GET /forum_posts/{id}.json``."""

    forum_post: ForumPost


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------


class MessageResponse(BaseModel):
    """Response envelope for ``GET /messages/{id}.json``."""

    message: Message


class MessagesResponse(BaseModel):
    """Response envelope for ``GET /messages/list.json``."""

    messages: list[Message]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Shops / stores / groups
# ---------------------------------------------------------------------------


class ShopResponse(BaseModel):
    """Response envelope for ``GET /shops/{id}.json``."""

    shop: Shop


class ShopsResponse(BaseModel):
    """Response envelope for ``GET /shops/search.json``."""

    shops: list[Shop]
    paginator: Optional[Paginator] = None


class StoresResponse(BaseModel):
    """Response envelope for ``GET /stores/search.json``."""

    stores: list[Store]


class StoreProductsResponse(BaseModel):
    """Response envelope for ``GET /stores/{id}/products.json``."""

    products: list[Product]
    paginator: Optional[Paginator] = None


class GroupsResponse(BaseModel):
    """Response envelope for ``GET /groups/search.json``."""

    groups: list[Group]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Products / deliveries
# ---------------------------------------------------------------------------


class ProductResponse(BaseModel):
    """Response envelope for ``GET /products/{id}.json``."""

    product: Product


class ProductAttachmentsResponse(BaseModel):
    """Response envelope for ``GET /products/{id}/attachments.json``."""

    product_attachments: list[ProductAttachment]


class ProductAttachmentResponse(BaseModel):
    """Response envelope for ``GET /product_attachments/{id}.json``."""

    product_attachment: ProductAttachment


class DeliveriesResponse(BaseModel):
    """Response envelope for ``GET /people/{username}/deliveries/list.json``."""

    deliveries: list[Delivery]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Drafts / volumes / pages
# ---------------------------------------------------------------------------


class DraftPatternResponse(BaseModel):
    """Response envelope for ``GET /drafts/{id}.json``."""

    draft_pattern: DraftPattern


class DraftPatternsResponse(BaseModel):
    """Response envelope for ``GET /drafts/list.json``."""

    draft_patterns: list[DraftPattern]


class VolumeResponse(BaseModel):
    """Response envelope for ``GET /volumes/{id}.json``."""

    volume: Volume


class PageResponse(BaseModel):
    """Response envelope for ``GET /pages/{id}.json``."""

    page: Page
