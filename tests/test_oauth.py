"""Tests for :mod:`ravelpy.oauth` — OAuthClient and token persistence helpers."""

import json
import urllib.parse
from pathlib import Path

import pytest
import respx
import httpx

from ravelpy.oauth import (
    AUTH_URL,
    TOKEN_URL,
    DEFAULT_REDIRECT_URI,
    OAuthClient,
    TokenResponse,
    save_tokens,
    load_tokens,
)
from ravelpy import RavelryClient


CLIENT_ID = "test_client_id"
CLIENT_SECRET = "test_client_secret"
REDIRECT_URI = "http://localhost:8080/callback"

SAMPLE_TOKEN_RESPONSE = {
    "access_token": "sample_access_token",
    "token_type": "bearer",
    "expires_in": 86400,
    "refresh_token": "sample_refresh_token",
    "scope": "offline",
}


@pytest.fixture
def oauth() -> OAuthClient:
    return OAuthClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)


# ── TokenResponse ────────────────────────────────────────────────────────────

class TestTokenResponse:
    def test_parses_all_fields(self):
        tr = TokenResponse(SAMPLE_TOKEN_RESPONSE)
        assert tr.access_token == "sample_access_token"
        assert tr.token_type == "bearer"
        assert tr.expires_in == 86400
        assert tr.refresh_token == "sample_refresh_token"
        assert tr.scope == "offline"

    def test_optional_refresh_token(self):
        data = {**SAMPLE_TOKEN_RESPONSE}
        del data["refresh_token"]
        tr = TokenResponse(data)
        assert tr.refresh_token is None

    def test_to_dict_roundtrip(self):
        tr = TokenResponse(SAMPLE_TOKEN_RESPONSE)
        assert tr.to_dict() == SAMPLE_TOKEN_RESPONSE

    def test_from_dict_roundtrip(self):
        tr = TokenResponse.from_dict(SAMPLE_TOKEN_RESPONSE)
        assert tr.access_token == SAMPLE_TOKEN_RESPONSE["access_token"]


# ── OAuthClient.auth_url ─────────────────────────────────────────────────────

class TestAuthUrl:
    def test_contains_auth_base(self, oauth):
        url, _ = oauth.auth_url(["offline"])
        assert url.startswith(AUTH_URL)

    def test_scopes_joined_with_space(self, oauth):
        url, _ = oauth.auth_url(["offline", "forum-write"])
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        assert params["scope"] == ["offline forum-write"]

    def test_client_id_in_url(self, oauth):
        url, _ = oauth.auth_url(["offline"])
        assert f"client_id={CLIENT_ID}" in url

    def test_redirect_uri_in_url(self, oauth):
        url, _ = oauth.auth_url(["offline"])
        assert urllib.parse.quote(REDIRECT_URI, safe="") in url

    def test_response_type_is_code(self, oauth):
        url, _ = oauth.auth_url(["offline"])
        assert "response_type=code" in url

    def test_state_included_in_url(self, oauth):
        url, state = oauth.auth_url(["offline"])
        assert state in url

    def test_custom_state_used(self, oauth):
        url, state = oauth.auth_url(["offline"], state="my_state_123")
        assert state == "my_state_123"
        assert "my_state_123" in url

    def test_state_differs_across_calls(self, oauth):
        _, state1 = oauth.auth_url(["offline"])
        _, state2 = oauth.auth_url(["offline"])
        assert state1 != state2


# ── OAuthClient.exchange_code ────────────────────────────────────────────────

class TestExchangeCode:
    def test_posts_to_token_url(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            oauth.exchange_code("auth_code_xyz")
            assert mock.calls.last.request.url == TOKEN_URL

    def test_sends_grant_type(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            oauth.exchange_code("auth_code_xyz")
            body = dict(urllib.parse.parse_qsl(mock.calls.last.request.content.decode()))
            assert body["grant_type"] == "authorization_code"
            assert body["code"] == "auth_code_xyz"
            assert body["redirect_uri"] == REDIRECT_URI

    def test_uses_basic_auth(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            oauth.exchange_code("auth_code_xyz")
            auth_header = mock.calls.last.request.headers.get("authorization", "")
            assert auth_header.startswith("Basic ")

    def test_returns_token_response(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            result = oauth.exchange_code("auth_code_xyz")
            assert isinstance(result, TokenResponse)
            assert result.access_token == "sample_access_token"

    def test_raises_on_error_status(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(401, json={"error": "invalid_client"})
            with pytest.raises(httpx.HTTPStatusError):
                oauth.exchange_code("bad_code")


# ── OAuthClient.refresh ──────────────────────────────────────────────────────

class TestRefresh:
    def test_posts_to_token_url(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            oauth.refresh("my_refresh_token")
            assert mock.calls.last.request.url == TOKEN_URL

    def test_sends_grant_type(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            oauth.refresh("my_refresh_token")
            body = dict(urllib.parse.parse_qsl(mock.calls.last.request.content.decode()))
            assert body["grant_type"] == "refresh_token"
            assert body["refresh_token"] == "my_refresh_token"

    def test_uses_basic_auth(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            oauth.refresh("my_refresh_token")
            auth_header = mock.calls.last.request.headers.get("authorization", "")
            assert auth_header.startswith("Basic ")

    def test_returns_token_response(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(200, json=SAMPLE_TOKEN_RESPONSE)
            result = oauth.refresh("my_refresh_token")
            assert isinstance(result, TokenResponse)

    def test_raises_on_error_status(self, oauth):
        with respx.mock() as mock:
            mock.post(TOKEN_URL).respond(400, json={"error": "invalid_grant"})
            with pytest.raises(httpx.HTTPStatusError):
                oauth.refresh("expired_token")


# ── Token persistence ─────────────────────────────────────────────────────────

class TestTokenPersistence:
    def test_save_and_load_roundtrip(self, tmp_path):
        path = tmp_path / ".oauth_tokens.json"
        original = TokenResponse(SAMPLE_TOKEN_RESPONSE)
        save_tokens(original, path)
        loaded = load_tokens(path)
        assert loaded.access_token == original.access_token
        assert loaded.refresh_token == original.refresh_token
        assert loaded.expires_in == original.expires_in

    def test_saved_file_is_valid_json(self, tmp_path):
        path = tmp_path / ".oauth_tokens.json"
        save_tokens(TokenResponse(SAMPLE_TOKEN_RESPONSE), path)
        data = json.loads(path.read_text())
        assert data["access_token"] == "sample_access_token"

    def test_load_raises_if_file_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_tokens(tmp_path / "nonexistent.json")


# ── RavelryClient.from_oauth_token ───────────────────────────────────────────

class TestRavelryClientFromOAuthToken:
    def test_sends_bearer_auth(self):
        client = RavelryClient.from_oauth_token("my_access_token")
        with respx.mock(base_url="https://api.ravelry.com", assert_all_called=False) as mock:
            mock.get("/color_families.json").respond(200, json={"color_families": []})
            client.extras.color_families()
            auth_header = mock.calls.last.request.headers.get("authorization", "")
            assert auth_header == "Bearer my_access_token"

    def test_does_not_send_basic_auth(self):
        client = RavelryClient.from_oauth_token("my_access_token")
        with respx.mock(base_url="https://api.ravelry.com", assert_all_called=False) as mock:
            mock.get("/color_families.json").respond(200, json={"color_families": []})
            client.extras.color_families()
            auth_header = mock.calls.last.request.headers.get("authorization", "")
            assert not auth_header.startswith("Basic ")

    def test_all_resource_sub_clients_present(self):
        client = RavelryClient.from_oauth_token("tok")
        for attr in ["patterns", "yarns", "people", "stash", "projects", "forums", "needles"]:
            assert hasattr(client, attr)

    def test_normal_init_still_uses_basic_auth(self):
        client = RavelryClient(username="u", api_key="k")
        with respx.mock(base_url="https://api.ravelry.com", assert_all_called=False) as mock:
            mock.get("/color_families.json").respond(200, json={"color_families": []})
            client.extras.color_families()
            auth_header = mock.calls.last.request.headers.get("authorization", "")
            assert auth_header.startswith("Basic ")
