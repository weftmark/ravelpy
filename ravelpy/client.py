"""Top-level client that wires a shared httpx session to every resource sub-client."""

import httpx

from .resources import (
    App,
    BundledItems,
    Bundles,
    Deliveries,
    Designers,
    Drafts,
    Extras,
    Favorites,
    Fiber,
    FiberAttributeGroups,
    Forums,
    Friends,
    Groups,
    Languages,
    Library,
    Messages,
    Needles,
    Packs,
    Pages,
    PatternAttributes,
    PatternCategories,
    PatternSourceTypes,
    PatternSources,
    Patterns,
    People,
    Photos,
    ProductAttachments,
    Products,
    Projects,
    Queue,
    SavedSearches,
    Shops,
    Stash,
    Stores,
    Topics,
    Volumes,
    YarnAttributes,
    YarnCompanies,
    Yarns,
)


class RavelryClient:
    """Read-only client for the Ravelry API using developer credentials (HTTP Basic Auth).

    All resource sub-clients share a single :class:`httpx.Client` session so
    that connection pooling and authentication headers are applied uniformly.

    Example::

        client = RavelryClient(username="you", api_key="your-key")
        parsed, etag, raw = client.yarns.show(yarn_id=95245, include="colorways")
    """

    def __init__(self, username: str, api_key: str) -> None:
        """Create a client authenticated with Ravelry developer credentials.

        Args:
            username: Your Ravelry username (used as the Basic Auth user).
            api_key:  Your Ravelry API key (used as the Basic Auth password).
        """
        session = httpx.Client(auth=(username, api_key), headers={"Accept": "application/json"})
        self.app = App(session)
        self.bundled_items = BundledItems(session)
        self.bundles = Bundles(session)
        self.deliveries = Deliveries(session)
        self.designers = Designers(session)
        self.drafts = Drafts(session)
        self.extras = Extras(session)
        self.favorites = Favorites(session)
        self.fiber = Fiber(session)
        self.fiber_attribute_groups = FiberAttributeGroups(session)
        self.forums = Forums(session)
        self.friends = Friends(session)
        self.groups = Groups(session)
        self.languages = Languages(session)
        self.library = Library(session)
        self.messages = Messages(session)
        self.needles = Needles(session)
        self.packs = Packs(session)
        self.pages = Pages(session)
        self.pattern_attributes = PatternAttributes(session)
        self.pattern_categories = PatternCategories(session)
        self.pattern_source_types = PatternSourceTypes(session)
        self.pattern_sources = PatternSources(session)
        self.patterns = Patterns(session)
        self.people = People(session)
        self.photos = Photos(session)
        self.product_attachments = ProductAttachments(session)
        self.products = Products(session)
        self.projects = Projects(session)
        self.queue = Queue(session)
        self.saved_searches = SavedSearches(session)
        self.shops = Shops(session)
        self.stash = Stash(session)
        self.stores = Stores(session)
        self.topics = Topics(session)
        self.volumes = Volumes(session)
        self.yarn_attributes = YarnAttributes(session)
        self.yarn_companies = YarnCompanies(session)
        self.yarns = Yarns(session)
