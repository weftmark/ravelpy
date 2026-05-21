from typing import Optional
from pydantic import BaseModel

from .models import (
    Activity,
    AttributeGroup,
    Bookmark,
    Bundle,
    BundledItem,
    ColorFamily,
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
    page: Optional[int] = None
    page_count: Optional[int] = None
    page_size: Optional[int] = None
    results: Optional[int] = None
    last_page: Optional[bool] = None


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------


class ColorFamiliesResponse(BaseModel):
    color_families: list[ColorFamily]


class FiberAttributeGroupsResponse(BaseModel):
    fiber_attribute_groups: list[FiberAttributeGroup]


class FiberAttributesResponse(BaseModel):
    fiber_attributes: list[FiberAttribute]


class FiberCategoriesResponse(BaseModel):
    fiber_categories: list[FiberCategory]


class YarnAttributeGroupsResponse(BaseModel):
    yarn_attribute_groups: list[YarnAttributeGroup]


class YarnWeightsResponse(BaseModel):
    yarn_weights: list[YarnWeight]


class LanguagesResponse(BaseModel):
    languages: list[Language]


class NeedlesResponse(BaseModel):
    needles: list[NeedleRecord]


class NeedleSizesResponse(BaseModel):
    needle_sizes: list[NeedleSize]


class NeedleTypesResponse(BaseModel):
    needle_types: list[NeedleType]


class PatternAttributeGroupsResponse(BaseModel):
    attribute_groups: list[AttributeGroup]


class PatternCategoriesResponse(BaseModel):
    pattern_categories: list[PatternCategory]


class PatternSourceTypesResponse(BaseModel):
    pattern_source_types: list[PatternSourceType]


class ProjectCraftsResponse(BaseModel):
    crafts: list[Craft]


class ProjectStatusesResponse(BaseModel):
    project_statuses: list[ProjectStatus]


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------


class PatternResponse(BaseModel):
    pattern: Pattern


class PatternsMultiResponse(BaseModel):
    patterns: dict[str, Pattern]


class PatternSearchResponse(BaseModel):
    patterns: list[Pattern]
    paginator: Optional[Paginator] = None


class PatternHighlightsResponse(BaseModel):
    patterns: list[Pattern]


class PatternSourceResponse(BaseModel):
    pattern_source: PatternSource


class PatternSourcesSearchResponse(BaseModel):
    pattern_sources: list[PatternSource]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Yarns
# ---------------------------------------------------------------------------


class YarnResponse(BaseModel):
    yarn: Yarn


class YarnsMultiResponse(BaseModel):
    yarns: dict[str, Yarn]


class YarnSearchResponse(BaseModel):
    yarns: list[Yarn]
    paginator: Optional[Paginator] = None


class YarnCompaniesResponse(BaseModel):
    yarn_companies: list[YarnCompany]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------


class CommentsResponse(BaseModel):
    comments: list[Comment]


# ---------------------------------------------------------------------------
# People / social
# ---------------------------------------------------------------------------


class UserResponse(BaseModel):
    user: User


class FriendsResponse(BaseModel):
    users: list[User]


class FriendActivityResponse(BaseModel):
    activities: list[Activity]


class SavedSearchesResponse(BaseModel):
    saved_searches: list[SavedSearch]


class LibraryResponse(BaseModel):
    volumes: list[Volume]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


class ProjectResponse(BaseModel):
    project: Project


class ProjectsResponse(BaseModel):
    projects: list[Project]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Stash
# ---------------------------------------------------------------------------


class StashResponse(BaseModel):
    stash: Stash


class StashListResponse(BaseModel):
    stash: list[Stash]
    paginator: Optional[Paginator] = None


class UnifiedStashResponse(BaseModel):
    stash: list[UnifiedStash]


# ---------------------------------------------------------------------------
# Queue
# ---------------------------------------------------------------------------


class QueuedProjectResponse(BaseModel):
    queued_project: QueuedProject


class QueueResponse(BaseModel):
    queued_projects: list[QueuedProject]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Favorites
# ---------------------------------------------------------------------------


class FavoriteResponse(BaseModel):
    favorite: Bookmark


class FavoritesResponse(BaseModel):
    favorites: list[Bookmark]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Fiber stash
# ---------------------------------------------------------------------------


class FiberStashResponse(BaseModel):
    fiber: FiberStash


# ---------------------------------------------------------------------------
# Bundles / packs
# ---------------------------------------------------------------------------


class BundleResponse(BaseModel):
    bundle: Bundle


class BundlesResponse(BaseModel):
    bundles: list[Bundle]
    paginator: Optional[Paginator] = None


class BundledItemResponse(BaseModel):
    bundled_item: BundledItem


class PackResponse(BaseModel):
    pack: Pack


# ---------------------------------------------------------------------------
# Forums / topics
# ---------------------------------------------------------------------------


class ForumSetsResponse(BaseModel):
    forum_sets: list[ForumSet]


class TopicsResponse(BaseModel):
    topics: list[Topic]
    paginator: Optional[Paginator] = None


class TopicResponse(BaseModel):
    topic: Topic


class ForumPostsResponse(BaseModel):
    forum_posts: list[ForumPost]
    paginator: Optional[Paginator] = None


class ForumPostResponse(BaseModel):
    forum_post: ForumPost


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------


class MessageResponse(BaseModel):
    message: Message


class MessagesResponse(BaseModel):
    messages: list[Message]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Shops / stores / groups
# ---------------------------------------------------------------------------


class ShopResponse(BaseModel):
    shop: Shop


class ShopsResponse(BaseModel):
    shops: list[Shop]
    paginator: Optional[Paginator] = None


class StoresResponse(BaseModel):
    stores: list[Store]


class StoreProductsResponse(BaseModel):
    products: list[Product]
    paginator: Optional[Paginator] = None


class GroupsResponse(BaseModel):
    groups: list[Group]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Products / deliveries
# ---------------------------------------------------------------------------


class ProductResponse(BaseModel):
    product: Product


class ProductAttachmentsResponse(BaseModel):
    product_attachments: list[ProductAttachment]


class ProductAttachmentResponse(BaseModel):
    product_attachment: ProductAttachment


class DeliveriesResponse(BaseModel):
    deliveries: list[Delivery]
    paginator: Optional[Paginator] = None


# ---------------------------------------------------------------------------
# Drafts / volumes / pages
# ---------------------------------------------------------------------------


class DraftPatternResponse(BaseModel):
    draft_pattern: DraftPattern


class DraftPatternsResponse(BaseModel):
    draft_patterns: list[DraftPattern]


class VolumeResponse(BaseModel):
    volume: Volume


class PageResponse(BaseModel):
    page: Page
