"""Top-level async client that wires a shared httpx.AsyncClient to every resource sub-client."""

import httpx

from .resources import (
    App,
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
    """Async client for the Ravelry API using :class:`httpx.AsyncClient`.

    All resource sub-clients share a single session so that connection pooling
    and authentication headers are applied uniformly.  Use as an async context
    manager so the underlying session is closed cleanly::

        async with RavelryClient(username="read-xxxx", api_key="your-key") as client:
            data, etag, raw = await client.patterns.search(query="socks")

    **Credential types**

    Ravelry issues three kinds of developer credentials, each with a different
    scope.  Pass the appropriate ``username`` / ``api_key`` pair when
    constructing this client.

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

        async with RavelryClient(username="read-xxxx", api_key="your-key") as client:
            parsed, etag, raw = await client.yarns.show(yarn_id=95245, include="colorways")
    """

    def __init__(self, username: str, api_key: str) -> None:
        """Create a client authenticated with Ravelry developer credentials.

        Args:
            username: Ravelry username for HTTP Basic Auth.  For a read-only
                key this is the ``read-xxxx`` string from the developer portal.
            api_key:  Corresponding API key used as the Basic Auth password.
        """
        session = httpx.AsyncClient(auth=(username, api_key), headers={"Accept": "application/json"})
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
            me, _, _ = await client.people.me()
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

    async def __aenter__(self) -> "RavelryClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    def _setup_resources(self, session: httpx.AsyncClient) -> None:
        self._session = session
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
