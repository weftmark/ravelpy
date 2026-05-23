"""Top-level client that wires a shared httpx session to every resource sub-client."""

import httpx

from .resources import (
    App,
    AsyncApp,
    AsyncBundledItems,
    AsyncColorways,
    AsyncBundles,
    AsyncDeliveries,
    AsyncDesigners,
    AsyncDrafts,
    AsyncExtras,
    AsyncFavorites,
    AsyncFiber,
    AsyncFiberAttributeGroups,
    AsyncForums,
    AsyncFriends,
    AsyncGroups,
    AsyncLanguages,
    AsyncLibrary,
    AsyncMessages,
    AsyncNeedles,
    AsyncPacks,
    AsyncPages,
    AsyncPatternAttributes,
    AsyncPatternCategories,
    AsyncPatternSourceTypes,
    AsyncPatternSources,
    AsyncPatterns,
    AsyncPeople,
    AsyncPhotos,
    AsyncProductAttachments,
    AsyncProducts,
    AsyncProjects,
    AsyncQueue,
    AsyncSavedSearches,
    AsyncShops,
    AsyncStash,
    AsyncStores,
    AsyncTopics,
    AsyncVolumes,
    AsyncYarnAttributes,
    AsyncYarnCompanies,
    AsyncYarns,
    BundledItems,
    Bundles,
    Colorways,
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
                portal.
            api_key:  Corresponding API key used as the Basic Auth password.
        """
        session = httpx.Client(auth=(username, api_key), headers={"Accept": "application/json"})
        self._setup_resources(session)

    @classmethod
    def from_oauth_token(cls, access_token: str) -> "RavelryClient":
        """Create a client that authenticates with a Ravelry OAuth 2.0 access token.

        Sends ``Authorization: Bearer <token>`` on every request instead of Basic Auth.
        Obtain the token by running ``scripts/oauth_login.py`` or calling
        :meth:`ravelpy.oauth.OAuthClient.local_flow`.

        Args:
            access_token: A valid Ravelry OAuth 2.0 access token.

        Returns:
            A fully initialised :class:`RavelryClient` using Bearer token auth.

        Example::

            from ravelpy import RavelryClient
            from ravelpy.oauth import load_tokens
            tokens = load_tokens(Path(".oauth_tokens.json"))
            client = RavelryClient.from_oauth_token(tokens.access_token)
            me, _, _ = client.people.me()
        """
        class _BearerAuth(httpx.Auth):
            def auth_flow(self, request):
                request.headers["Authorization"] = f"Bearer {access_token}"
                yield request

        instance = cls.__new__(cls)
        session = httpx.Client(auth=_BearerAuth(), headers={"Accept": "application/json"})
        instance._setup_resources(session)
        return instance

    def _setup_resources(self, session: httpx.Client) -> None:
        self.app = App(session)
        self.bundled_items = BundledItems(session)
        self.colorways = Colorways(session)
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


class AsyncRavelryClient:
    """Async client for the Ravelry API using :class:`httpx.AsyncClient`.

    Mirrors :class:`RavelryClient` but every sub-client method is a coroutine.
    Use as an async context manager so the underlying session is closed cleanly::

        async with AsyncRavelryClient(username="read-xxxx", api_key="your-key") as client:
            data, etag, raw = await client.patterns.search(query="socks")

    **Credential types** are the same as :class:`RavelryClient` — read-only key,
    personal key, or OAuth 2.0 Bearer token via :meth:`from_oauth_token`.
    """

    def __init__(self, username: str, api_key: str) -> None:
        """Create an async client authenticated with Ravelry developer credentials.

        Args:
            username: Ravelry username for HTTP Basic Auth.
            api_key:  Corresponding API key used as the Basic Auth password.
        """
        session = httpx.AsyncClient(auth=(username, api_key), headers={"Accept": "application/json"})
        self._setup_resources(session)

    @classmethod
    def from_oauth_token(cls, access_token: str) -> "AsyncRavelryClient":
        """Create an async client that authenticates with a Ravelry OAuth 2.0 access token.

        Args:
            access_token: A valid Ravelry OAuth 2.0 access token.

        Returns:
            A fully initialised :class:`AsyncRavelryClient` using Bearer token auth.
        """
        class _BearerAuth(httpx.Auth):
            def auth_flow(self, request):
                request.headers["Authorization"] = f"Bearer {access_token}"
                yield request

        instance = cls.__new__(cls)
        session = httpx.AsyncClient(auth=_BearerAuth(), headers={"Accept": "application/json"})
        instance._setup_resources(session)
        return instance

    async def aclose(self) -> None:
        """Close the underlying :class:`httpx.AsyncClient` session."""
        await self._session.aclose()

    async def __aenter__(self) -> "AsyncRavelryClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    def _setup_resources(self, session: httpx.AsyncClient) -> None:
        self._session = session
        self.app = AsyncApp(session)
        self.bundled_items = AsyncBundledItems(session)
        self.colorways = AsyncColorways(session)
        self.bundles = AsyncBundles(session)
        self.deliveries = AsyncDeliveries(session)
        self.designers = AsyncDesigners(session)
        self.drafts = AsyncDrafts(session)
        self.extras = AsyncExtras(session)
        self.favorites = AsyncFavorites(session)
        self.fiber = AsyncFiber(session)
        self.fiber_attribute_groups = AsyncFiberAttributeGroups(session)
        self.forums = AsyncForums(session)
        self.friends = AsyncFriends(session)
        self.groups = AsyncGroups(session)
        self.languages = AsyncLanguages(session)
        self.library = AsyncLibrary(session)
        self.messages = AsyncMessages(session)
        self.needles = AsyncNeedles(session)
        self.packs = AsyncPacks(session)
        self.pages = AsyncPages(session)
        self.pattern_attributes = AsyncPatternAttributes(session)
        self.pattern_categories = AsyncPatternCategories(session)
        self.pattern_source_types = AsyncPatternSourceTypes(session)
        self.pattern_sources = AsyncPatternSources(session)
        self.patterns = AsyncPatterns(session)
        self.people = AsyncPeople(session)
        self.photos = AsyncPhotos(session)
        self.product_attachments = AsyncProductAttachments(session)
        self.products = AsyncProducts(session)
        self.projects = AsyncProjects(session)
        self.queue = AsyncQueue(session)
        self.saved_searches = AsyncSavedSearches(session)
        self.shops = AsyncShops(session)
        self.stash = AsyncStash(session)
        self.stores = AsyncStores(session)
        self.topics = AsyncTopics(session)
        self.volumes = AsyncVolumes(session)
        self.yarn_attributes = AsyncYarnAttributes(session)
        self.yarn_companies = AsyncYarnCompanies(session)
        self.yarns = AsyncYarns(session)
