# Authentication

ravelpy supports three credential tiers. All credentials come from the
[Ravelry developer portal](https://www.ravelry.com/pro/developer).

## Credential tiers

| Tier | Credential type | Access |
| --- | --- | --- |
| Read-only | Basic Auth with `read-` prefix username | Public catalog — patterns, yarns, shops, search |
| Personal key | Basic Auth with your developer credentials | Full access; all OAuth scopes granted automatically |
| OAuth 2.0 | Bearer token | Delegated access on behalf of any Ravelry user |

---

## Read-only Basic Auth

Use the `basic_auth_username` (starts with `read-`) and `basic_auth_password`
from your developer portal. Grants access to public catalog endpoints only.

```python
import asyncio
from ravelpy import RavelryClient

async def main():
    async with RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key") as client:
        data, etag, raw = await client.patterns.search(query="socks")
        data, etag, raw = await client.yarns.show(yarn_id=90897)

asyncio.run(main())
```

---

## Personal key

Authenticates as your own Ravelry account. Grants full access to all
endpoints without configuring OAuth scopes.

```python
from ravelpy import RavelryClient

async with RavelryClient(username="your_username", api_key="your_personal_key") as client:
    data, etag, raw = await client.people.me()
    data, etag, raw = await client.messages.list()
    data, etag, raw = await client.stash.list(username="your_username")
```

---

## OAuth 2.0

Use OAuth 2.0 when your application acts on behalf of other Ravelry users.

### Scopes

| Scope constant | Scope string | Access granted |
| --- | --- | --- |
| `OAuthScope.OFFLINE` | `offline` | Basic authenticated access; includes a refresh token |
| `OAuthScope.FORUM_WRITE` | `forum-write` | Create and reply to forum topics |
| `OAuthScope.MESSAGE_WRITE` | `message-write` | Send private messages |
| `OAuthScope.PATTERNSTORE_READ` | `patternstore-read` | Read pattern store, draft patterns, and store products |
| `OAuthScope.DELIVERIES_READ` | `deliveries-read` | Read PDF delivery history |
| `OAuthScope.LIBRARY_PDF` | `library-pdf` | Download purchased PDFs from the library |

### Authorization flow

`auth_url()` and `local_flow()` are synchronous. `exchange_code()` and
`refresh()` are coroutines and must be awaited. `local_flow()` runs its own
event loop, so call it outside `asyncio.run(...)`, not from inside a coroutine.

```python
from ravelpy import RavelryClient
from ravelpy.oauth import OAuthClient, OAuthScope

oauth = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Step 1 — send the user to Ravelry; keep `state` to check in the callback
url, state = oauth.auth_url(scopes=[OAuthScope.OFFLINE])
print(f"Visit: {url}")

async def finish(code: str, returned_state: str):
    # Step 2 — reject callbacks whose state doesn't match (CSRF guard),
    # then exchange the authorization code for a token
    if returned_state != state:
        raise RuntimeError("OAuth state mismatch")
    token = await oauth.exchange_code(code=code)

    # Step 3 — build a client
    async with RavelryClient.from_oauth_token(token.access_token) as client:
        data, etag, raw = await client.people.me()
    return token
```

For local scripts, `local_flow()` does all of this (browser, callback server,
state check, code exchange) in one synchronous call:

```python
token = oauth.local_flow([OAuthScope.OFFLINE])
```

### Local browser flow

For scripts and local development, `local_flow()` opens the browser, runs a
temporary callback server on `localhost` (the port and path from
`redirect_uri`, default `http://localhost:8080/callback`), and exchanges the
code for you:

```python
token = oauth.local_flow([OAuthScope.OFFLINE])               # waits up to 5 minutes
token = oauth.local_flow([OAuthScope.OFFLINE], timeout=None) # wait indefinitely
```

Only a callback carrying the `state` token generated for this flow ends it.
Requests with a missing or wrong `state`, including `error` callbacks, get a
`400` response and are ignored, so another local process or web page cannot
abort the login. A matching callback with `error` raises `RuntimeError`; no
valid callback within `timeout` seconds raises `TimeoutError`.

### Persisting tokens

```python
from pathlib import Path
from ravelpy.oauth import save_tokens, load_tokens

TOKEN_PATH = Path(".oauth_tokens.json")

# Save after exchanging or refreshing
save_tokens(token, TOKEN_PATH)

# Load on next run
token = load_tokens(TOKEN_PATH)
client = RavelryClient.from_oauth_token(token.access_token)
```

The token file contains your bearer access token and refresh token.
`save_tokens` creates it with mode `0600` (readable and writable by the owner
only) and tightens an existing file to `0600` when overwriting it. On Windows
these permission bits are not enforced, so keep the file in a directory only
you can read.

### Refreshing tokens

```python
async def refresh_and_connect():
    refreshed = await oauth.refresh(token.refresh_token)
    save_tokens(refreshed, TOKEN_PATH)
    async with RavelryClient.from_oauth_token(refreshed.access_token) as client:
        data, etag, raw = await client.people.me()
```

---

## Environment variables

A convenient pattern for storing credentials:

```bash
# .env
RAVELRY_USERNAME=read-xxxxxxxxxxxx
RAVELRY_API_KEY=your_api_key
```

```python
import os
from dotenv import load_dotenv
from ravelpy import RavelryClient

load_dotenv()
client = RavelryClient(
    username=os.environ["RAVELRY_USERNAME"],
    api_key=os.environ["RAVELRY_API_KEY"],
)
```
