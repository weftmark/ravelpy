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

    **Credential types**

    Ravelry issues three kinds of developer credentials, each with a different
    scope.  Pass the appropriate ``username`` / ``api_key`` pair when
    constructing this client.

    The Ravelry API recognises three credential tiers.  Pass the appropriate
    ``username`` / ``api_key`` pair when constructing this client.

    *Read-only Basic Auth key*
        The simplest credential.  The developer portal issues a
        ``basic_auth_username`` / ``basic_auth_password`` pair.  Only endpoints
        **not** marked *"authenticated"* in the official docs can be called with
        this credential — roughly the public pattern/yarn catalog, shops, groups,
        global search, and a handful of others.  Most user-centric endpoints
        (stash, projects, queue, friends, messages, …) require a higher-privilege
        credential.

    *Personal account access* (personal key)
        Uses ``access_key`` as the username and ``personal_key`` as the
        password — both found on the developer portal.  The docs state this
        grants **full access** to the associated Ravelry account with all OAuth
        permissions automatically included; no explicit scopes are needed.  Use
        this for personal tooling that reads or writes your own account data.

    *OAuth 2.0*
        Client-ID / client-secret flow (``https://www.ravelry.com/oauth2/auth``)
        for apps acting on behalf of *other* Ravelry users.  Requires explicit
        scopes: ``forum-write``, ``message-write``, ``deliveries-read``,
        ``library-pdf``, etc.  Tokens expire after 24 hours; request ``offline``
        to receive a refresh token.  Not wired into this client natively — supply
        an OAuth access token as ``api_key`` and the authorising user's username
        to use it manually.

    Individual resource sub-client docstrings note which tier each endpoint
    requires.

    Example::

        client = RavelryClient(username="read-xxxx", api_key="your-key")
        parsed, etag, raw = client.yarns.show(yarn_id=95245, include="colorways")
    """

    def __init__(self, username: str, api_key: str) -> None:
        """Create a client authenticated with Ravelry developer credentials.

        Args:
            username: Ravelry username for HTTP Basic Auth.  For a read-only
                personal key this is the ``read-xxxx`` string from the developer
                portal; for OAuth 2.0 pass the authorizing user's username.
            api_key:  Corresponding API key or OAuth access token used as the
                Basic Auth password.
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
