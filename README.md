# ravelpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

Python client for the [Ravelry REST API](https://www.ravelry.com/api), supporting read-only Basic Auth
(public catalog data), personal account keys (full authenticated access), and OAuth 2.0 (scoped delegated
access).

---

> **Built with Claude AI**
>
> The requirements, architecture, and implementation of ravelpy were developed collaboratively with [Claude](https://claude.ai) by Anthropic. Claude wrote the majority of the code in this repository through an iterative conversation-driven process. This is disclosed prominently because we believe AI development transparency matters.

---

## Install

```bash
pip install ravelpy
```

To also run the optional Swagger UI server:

```bash
pip install "ravelpy[server]"
```

---

## Auth

Ravelry supports three credential tiers:

| Tier | Credential | Access |
| --- | --- | --- |
| Read-only | Basic Auth with `read-` prefix username | Public catalog data only |
| Personal key | Basic Auth with your developer credentials | Full authenticated access; all OAuth scopes granted automatically |
| OAuth 2.0 | Bearer token | Scoped delegated access; requires explicit scope grants |

Get your developer credentials from [ravelry.com/pro/developer](https://www.ravelry.com/pro/developer).

### Basic Auth (read-only or personal key)

Set credentials as environment variables (or in a `.env` file):

```env
RAVELRY_USERNAME=read-xxxxxxxxxxxx   # or your personal username
RAVELRY_API_KEY=your_api_key
```

```python
from ravelpy import RavelryClient

# Read-only key — public catalog data only
client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

# Personal key — full authenticated access, all scopes auto-granted
client = RavelryClient(username="your_username", api_key="your_personal_key")
```

### OAuth 2.0

```python
from ravelpy import RavelryClient
from ravelpy.oauth import OAuthClient, OAuthScope

oauth = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Build an auth URL and redirect the user there
url, state = oauth.auth_url(scopes=[OAuthScope.OFFLINE])

# After the user grants access, exchange the code for a token
token = oauth.exchange_code(code="the_code_from_callback")

# Build a RavelryClient from the access token
client = RavelryClient.from_oauth_token(token.access_token)
```

See [docs/authentication.md](docs/authentication.md) for the full OAuth scope list, a tested scope matrix, and notes on which endpoints require specific scopes.

---

## Quickstart

All endpoints are accessed through sub-client attributes on `RavelryClient`:

```python
from ravelpy import RavelryClient

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

# Search for free sock patterns
data, etag, raw = client.patterns.search(query="socks", weight="fingering", availability="free")
for p in raw["patterns"]:
    print(p["name"])

# Get a specific yarn
data, etag, raw = client.yarns.show(yarn_id=90897)
print(raw["yarn"]["name"])

# Look up your own profile (requires personal key or OAuth)
personal_client = RavelryClient(username="your_username", api_key="your_personal_key")
data, etag, raw = personal_client.people.me()
print(raw["user"]["username"])
```

---

## Async client

`AsyncRavelryClient` is a drop-in async replacement — all the same sub-clients and methods, but every call is a coroutine:

```python
import asyncio
from ravelpy import AsyncRavelryClient

async def main():
    async with AsyncRavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key") as client:
        data, etag, raw = await client.patterns.search(query="colorwork")
        for p in raw["patterns"]:
            print(p["name"])

asyncio.run(main())
```

---

## ETag caching

Every method returns `(model, etag, raw_dict)`. Pass the `etag` back on subsequent calls — the server returns `304 Not Modified` and both `model` and `raw_dict` will be `None`.

```python
data, etag, raw = client.patterns.search(query="socks")

# later...
data, etag, raw = client.patterns.search(query="socks", etag=etag)
if data is None:
    print("not modified — use cached data")
```

---

## API coverage

| Sub-client | Methods |
| --- | --- |
| `client.patterns` | search, show, list (multi-get), comments, highlights, projects |
| `client.pattern_sources` | show, search, patterns |
| `client.yarns` | show, list (multi-get), search, comments |
| `client.yarn_companies` | search |
| `client.reference` | color families, fiber attributes/categories, yarn weights/attributes, pattern attributes/categories, pattern source types, languages, photo sizes |
| `client.people` | me, show, comments |
| `client.projects` | search, list, show, comments, crafts, statuses |
| `client.stash` | list, search, unified_list, show, comments |
| `client.queue` | list, show |
| `client.favorites` | list, show |
| `client.fiber` | show, comments |
| `client.bundles` | list, show, bundled_items, packs |
| `client.shops` | search, show |
| `client.groups` | search |
| `client.stores` | list, products, purchases |
| `client.forums` | sets, topics, filtered_topics, post, unread_posts |
| `client.topics` | show, posts |
| `client.messages` | list, show |
| `client.needles` | list, sizes, types |
| `client.designers` | show |
| `client.products` | show, attachments |
| `client.deliveries` | list |
| `client.drafts` | list, show |
| `client.volumes` | show |
| `client.pages` | show |
| `client.packs` | show |
| `client.friends` | list, activity |
| `client.library` | search |
| `client.saved_searches` | list |
| `client.app` | config, data |
| `client.extras` | color_families, search |
| `client.photos` | dimensions, sizes, status |

---

## Swagger UI server

The `examples/server.py` FastAPI proxy exposes all endpoints with interactive docs:

```bash
uvicorn examples.server:app --reload
```

Open `http://localhost:8000/docs`.

---

## Links

- [Ravelry API documentation](https://www.ravelry.com/api)
- [Ravelry Developer Agreement](https://www.ravelry.com/api#terms)
- [Report an issue](https://github.com/weftmark/ravelpy/issues)

## License

MIT — see [LICENSE](LICENSE).
