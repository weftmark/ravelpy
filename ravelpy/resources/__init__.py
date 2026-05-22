"""Re-exports all resource sub-client classes and the shared ``ApiResult`` type alias."""

from .app import App, AsyncApp
from .base import ApiResult, AsyncResource, Resource
from .bundled_items import AsyncBundledItems, BundledItems
from .bundles import AsyncBundles, Bundles
from .deliveries import AsyncDeliveries, Deliveries
from .designers import AsyncDesigners, Designers
from .drafts import AsyncDrafts, Drafts
from .extras import AsyncExtras, Extras
from .favorites import AsyncFavorites, Favorites
from .fiber import AsyncFiber, Fiber
from .fiber_attribute_groups import AsyncFiberAttributeGroups, FiberAttributeGroups
from .forums import AsyncForums, Forums
from .friends import AsyncFriends, Friends
from .groups import AsyncGroups, Groups
from .languages import AsyncLanguages, Languages
from .library import AsyncLibrary, Library
from .messages import AsyncMessages, Messages
from .needles import AsyncNeedles, Needles
from .packs import AsyncPacks, Packs
from .pages import AsyncPages, Pages
from .pattern_attributes import AsyncPatternAttributes, PatternAttributes
from .pattern_categories import AsyncPatternCategories, PatternCategories
from .pattern_source_types import AsyncPatternSourceTypes, PatternSourceTypes
from .pattern_sources import AsyncPatternSources, PatternSources
from .patterns import AsyncPatterns, Patterns
from .people import AsyncPeople, People
from .photos import AsyncPhotos, Photos
from .product_attachments import AsyncProductAttachments, ProductAttachments
from .products import AsyncProducts, Products
from .projects import AsyncProjects, Projects
from .queue import AsyncQueue, Queue
from .saved_searches import AsyncSavedSearches, SavedSearches
from .shops import AsyncShops, Shops
from .stash import AsyncStash, Stash
from .stores import AsyncStores, Stores
from .topics import AsyncTopics, Topics
from .volumes import AsyncVolumes, Volumes
from .yarn_attributes import AsyncYarnAttributes, YarnAttributes
from .yarn_companies import AsyncYarnCompanies, YarnCompanies
from .yarns import AsyncYarns, Yarns

__all__ = [
    "ApiResult",
    "Resource",
    "AsyncResource",
    # Sync sub-clients
    "App",
    "BundledItems",
    "Bundles",
    "Deliveries",
    "Designers",
    "Drafts",
    "Extras",
    "Favorites",
    "Fiber",
    "FiberAttributeGroups",
    "Forums",
    "Friends",
    "Groups",
    "Languages",
    "Library",
    "Messages",
    "Needles",
    "Packs",
    "Pages",
    "PatternAttributes",
    "PatternCategories",
    "PatternSourceTypes",
    "PatternSources",
    "Patterns",
    "People",
    "Photos",
    "ProductAttachments",
    "Products",
    "Projects",
    "Queue",
    "SavedSearches",
    "Shops",
    "Stash",
    "Stores",
    "Topics",
    "Volumes",
    "YarnAttributes",
    "YarnCompanies",
    "Yarns",
    # Async sub-clients
    "AsyncApp",
    "AsyncBundledItems",
    "AsyncBundles",
    "AsyncDeliveries",
    "AsyncDesigners",
    "AsyncDrafts",
    "AsyncExtras",
    "AsyncFavorites",
    "AsyncFiber",
    "AsyncFiberAttributeGroups",
    "AsyncForums",
    "AsyncFriends",
    "AsyncGroups",
    "AsyncLanguages",
    "AsyncLibrary",
    "AsyncMessages",
    "AsyncNeedles",
    "AsyncPacks",
    "AsyncPages",
    "AsyncPatternAttributes",
    "AsyncPatternCategories",
    "AsyncPatternSourceTypes",
    "AsyncPatternSources",
    "AsyncPatterns",
    "AsyncPeople",
    "AsyncPhotos",
    "AsyncProductAttachments",
    "AsyncProducts",
    "AsyncProjects",
    "AsyncQueue",
    "AsyncSavedSearches",
    "AsyncShops",
    "AsyncStash",
    "AsyncStores",
    "AsyncTopics",
    "AsyncVolumes",
    "AsyncYarnAttributes",
    "AsyncYarnCompanies",
    "AsyncYarns",
]
