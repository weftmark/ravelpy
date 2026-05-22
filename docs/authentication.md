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
from ravelpy import RavelryClient

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

data, etag, raw = client.patterns.search(query="socks")
data, etag, raw = client.yarns.show(yarn_id=90897)
```

---

## Personal key

Authenticates as your own Ravelry account. Grants full access to all
endpoints without configuring OAuth scopes.

```python
from ravelpy import RavelryClient

client = RavelryClient(username="your_username", api_key="your_personal_key")

data, etag, raw = client.people.me()
data, etag, raw = client.messages.list()
data, etag, raw = client.stash.list(username="your_username")
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

```python
from ravelpy import RavelryClient
from ravelpy.oauth import OAuthClient, OAuthScope

oauth = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Step 1 — send the user to Ravelry
url, state = oauth.auth_url(scopes=[OAuthScope.OFFLINE])
print(f"Visit: {url}")

# Step 2 — exchange the authorization code for a token
token = oauth.exchange_code(code="code_from_callback")

# Step 3 — build a client
client = RavelryClient.from_oauth_token(token.access_token)
data, etag, raw = client.people.me()
```

### Persisting tokens

```python
from ravelpy.oauth import save_tokens, load_tokens

# Save after exchanging or refreshing
save_tokens(token)

# Load on next run
token = load_tokens()
client = RavelryClient.from_oauth_token(token.access_token)
```

### Refreshing tokens

```python
refreshed = oauth.refresh(token.refresh_token)
save_tokens(refreshed)
client = RavelryClient.from_oauth_token(refreshed.access_token)
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
