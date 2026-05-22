"""OAuth 2.0 authorization code flow helper for the Ravelry API.

Ravelry-specific notes (from official docs):
- Auth URL:  https://www.ravelry.com/oauth2/auth
- Token URL: https://www.ravelry.com/oauth2/token
- Client credentials MUST be sent via Basic Auth header — body/form auth is not supported.
- Access tokens expire in 24 hours.
- Request the ``offline`` scope to receive a refresh token.

Typical local-testing workflow::

    from ravelpy.oauth import OAuthClient, save_tokens, load_tokens

    # 1. Get tokens — opens browser, captures callback on localhost
    oauth = OAuthClient(client_id="...", client_secret="...")
    tokens = oauth.local_flow(["offline"])
    save_tokens(tokens, Path(".oauth_tokens.json"))

    # 2. Build an authenticated RavelryClient from the token
    from ravelpy import RavelryClient
    tokens = load_tokens(Path(".oauth_tokens.json"))
    client = RavelryClient.from_oauth_token(tokens.access_token)
    me, _, _ = client.people.me()

    # 3. Refresh when the 24-hour token expires
    new_tokens = oauth.refresh(tokens.refresh_token)
    save_tokens(new_tokens, Path(".oauth_tokens.json"))
"""

import http.server
import json
import secrets
import urllib.parse
import webbrowser
from enum import Enum
from pathlib import Path
from typing import Optional

import httpx


AUTH_URL = "https://www.ravelry.com/oauth2/auth"
TOKEN_URL = "https://www.ravelry.com/oauth2/token"
DEFAULT_PORT = 8080
DEFAULT_REDIRECT_URI = f"http://localhost:{DEFAULT_PORT}/callback"


class OAuthScope(str, Enum):
    """Valid OAuth 2.0 scope values accepted by the Ravelry token endpoint.

    Pass one or more values to :meth:`OAuthClient.auth_url` or
    :meth:`OAuthClient.local_flow`.  Separate multiple scopes with a space,
    or pass a list and join with ``" ".join(...)``.

    Personal keys (Basic Auth) do **not** need explicit scopes — all privileges
    are granted automatically.  Scopes are only relevant for OAuth 2.0 flows.

    Standard scopes
    ---------------
    OFFLINE
        Standard OAuth 2.0 scope for requesting a refresh token.  Without this,
        tokens expire after 24 hours and require full re-authorization.

    FORUM_WRITE
        Create, edit, and delete forum posts.

    MESSAGE_WRITE
        Create (send) and delete private messages to other users.

    PATTERNSTORE_READ
        Enumerate the pattern stores the user administers and their products.

    PATTERNSTORE_PDF
        Generate download links for PDFs within the user's pattern stores.
        Currently limited access — available by request only.

    DELIVERIES_READ
        List products purchased by or gifted to the current user.

    LIBRARY_PDF
        Directly download PDFs from a user's library via ``generate_download_link``.
        Tokens with this scope expire more quickly than usual and may also expire
        if a rate limit is exceeded.  Consider holding a separate token for this
        scope alongside a normal token.

    Minimal-privilege scopes
    ------------------------
    PROFILE_ONLY
        Access ``/current_user.json`` and nothing else.

    CARTS_ONLY
        Access ``/carts/*.json`` and nothing else.
    """

    OFFLINE          = "offline"
    FORUM_WRITE      = "forum-write"
    MESSAGE_WRITE    = "message-write"
    PATTERNSTORE_READ = "patternstore-read"
    PATTERNSTORE_PDF = "patternstore-pdf"
    DELIVERIES_READ  = "deliveries-read"
    LIBRARY_PDF      = "library-pdf"
    PROFILE_ONLY     = "profile-only"
    CARTS_ONLY       = "carts-only"


class TokenResponse:
    """Parsed response from the Ravelry OAuth 2.0 token endpoint."""

    def __init__(self, data: dict) -> None:
        self.access_token: str = data["access_token"]
        self.token_type: str = data.get("token_type", "bearer")
        self.expires_in: int = data.get("expires_in", 86400)
        self.refresh_token: Optional[str] = data.get("refresh_token")
        self.scope: str = data.get("scope", "")
        self._raw: dict = data

    def to_dict(self) -> dict:
        """Return the raw token response dict (suitable for JSON serialisation)."""
        return self._raw

    @classmethod
    def from_dict(cls, data: dict) -> "TokenResponse":
        """Reconstruct a :class:`TokenResponse` from a previously serialised dict."""
        return cls(data)


class OAuthClient:
    """Manages the Ravelry OAuth 2.0 authorization code flow.

    For local testing, :meth:`local_flow` starts a one-shot HTTP server on
    ``localhost`` to capture the authorization callback automatically — no
    manual copy-pasting of codes required.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = DEFAULT_REDIRECT_URI,
    ) -> None:
        """
        Args:
            client_id:     OAuth client ID from the Ravelry developer portal.
            client_secret: OAuth client secret from the Ravelry developer portal.
            redirect_uri:  Must match a URI registered in the developer portal.
                           Defaults to ``http://localhost:8080/callback``.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    # ── URL construction ────────────────────────────────────────────────────

    def auth_url(
        self,
        scopes: list[str],
        state: Optional[str] = None,
    ) -> tuple[str, str]:
        """Build the Ravelry authorization URL and a CSRF state token.

        Args:
            scopes: OAuth scopes to request (e.g. ``["offline", "forum-write"]``).
            state:  CSRF state value.  Generated randomly if not provided.

        Returns:
            ``(url, state)`` — send the user to ``url``; verify ``state`` in the
            callback to guard against CSRF.
        """
        if state is None:
            state = secrets.token_urlsafe(16)
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "state": state,
        }
        return f"{AUTH_URL}?{urllib.parse.urlencode(params)}", state

    # ── Token operations ────────────────────────────────────────────────────

    def exchange_code(self, code: str) -> TokenResponse:
        """Exchange an authorization code for access and refresh tokens.

        Args:
            code: The ``code`` query parameter received at the redirect URI.

        Raises:
            httpx.HTTPStatusError: If the token endpoint returns a non-2xx status.
        """
        response = httpx.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            },
            auth=(self.client_id, self.client_secret),
        )
        response.raise_for_status()
        return TokenResponse(response.json())

    def refresh(self, refresh_token: str) -> TokenResponse:
        """Obtain a new access token using a refresh token.

        Args:
            refresh_token: The refresh token from a previous :meth:`exchange_code`
                           or :meth:`local_flow` call.  Requires the ``offline``
                           scope to have been requested originally.

        Raises:
            httpx.HTTPStatusError: If the token endpoint returns a non-2xx status.
        """
        response = httpx.post(
            TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(self.client_id, self.client_secret),
        )
        response.raise_for_status()
        return TokenResponse(response.json())

    # ── Local browser flow ──────────────────────────────────────────────────

    def local_flow(self, scopes: list[str]) -> TokenResponse:
        """Run the full authorization code flow using a local callback server.

        Opens the user's browser to the Ravelry authorization page, then starts a
        temporary HTTP server on ``localhost`` to receive the redirect callback.
        Once the code arrives it is exchanged for tokens and the server stops.

        The redirect URI registered in the Ravelry developer portal must match
        ``self.redirect_uri`` exactly (default: ``http://localhost:8080/callback``).

        Args:
            scopes: OAuth scopes to request (include ``"offline"`` for a refresh token).

        Returns:
            :class:`TokenResponse` with the access token (and refresh token if
            ``"offline"`` was in ``scopes``).

        Raises:
            RuntimeError: If the user denies access or the state token mismatches.
        """
        url, expected_state = self.auth_url(scopes)
        parsed = urllib.parse.urlparse(self.redirect_uri)
        port = int(parsed.port or DEFAULT_PORT)
        path = parsed.path or "/callback"

        captured: dict = {}
        oauth_client = self  # closure reference

        class _CallbackHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                req = urllib.parse.urlparse(self.path)
                if req.path != path:
                    self._reply(404, b"Not found.")
                    return

                params = urllib.parse.parse_qs(req.query, keep_blank_values=True)

                if "error" in params:
                    captured["error"] = params["error"][0]
                    self._reply(400, f"Authorization error: {params['error'][0]}. You can close this window.".encode())
                elif params.get("state", [None])[0] != expected_state:
                    captured["error"] = "state_mismatch"
                    self._reply(400, b"State mismatch \xe2\x80\x94 possible CSRF. Close this window.")
                else:
                    captured["code"] = params["code"][0]
                    self._reply(200, b"Authorization successful. You can close this window.")

                self.server._done = True

            def _reply(self, status: int, body: bytes) -> None:
                self.send_response(status)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, fmt: str, *args: object) -> None:
                pass  # silence per-request logs

        server = http.server.HTTPServer(("localhost", port), _CallbackHandler)
        server._done = False  # type: ignore[attr-defined]

        print(f"Opening browser for Ravelry authorization…")
        print(f"If the browser does not open, visit:\n  {url}")
        webbrowser.open(url)

        while not server._done:  # type: ignore[attr-defined]
            server.handle_request()
        server.server_close()

        if "error" in captured:
            raise RuntimeError(f"OAuth authorization failed: {captured['error']}")

        return self.exchange_code(captured["code"])


# ── Token persistence helpers ───────────────────────────────────────────────

def save_tokens(tokens: TokenResponse, path: Path) -> None:
    """Write a :class:`TokenResponse` to a JSON file.

    Args:
        tokens: Token response to persist.
        path:   Destination file path (e.g. ``Path(".oauth_tokens.json")``).
    """
    path.write_text(json.dumps(tokens.to_dict(), indent=2))


def load_tokens(path: Path) -> TokenResponse:
    """Load a :class:`TokenResponse` from a JSON file written by :func:`save_tokens`.

    Args:
        path: File path previously written by :func:`save_tokens`.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
    """
    return TokenResponse(json.loads(path.read_text()))
