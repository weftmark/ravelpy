# ravelpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

Read-only Python client for the [Ravelry REST API](https://www.ravelry.com/api), authenticated with developer credentials (HTTP Basic Auth).

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

## Auth setup

Get your developer credentials from [ravelry.com/pro/developer](https://www.ravelry.com/pro/developer).

Set them as environment variables (or in a `.env` file):

```env
RAVELRY_USERNAME=read-xxxxxxxxxxxx
RAVELRY_API_KEY=your_api_key
```

---

## Quickstart

```python
from ravelpy import RavelryClient

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

# Search for free sock patterns
data, etag = client.search_patterns(query="socks", weight="fingering", availability="free")
for p in data["patterns"]:
    print(p["name"])

# Get a specific yarn
data, etag = client.get_yarn(yarn_id=90897)
print(data["yarn"]["name"])

# Look up your stash
data, etag = client.get_stash_list(username="your_username")
```

---

## ETag caching

Every method returns `(data, etag)`. Pass the etag back on subsequent calls to avoid re-downloading unchanged data — the server returns `304 Not Modified` and `data` will be `None`.

```python
data, etag = client.get_yarn_weights()

# later...
data, etag = client.get_yarn_weights(etag=etag)
if data is None:
    print("not modified — use cached data")
```

---

## API coverage

| Section | Methods |
| --- | --- |
| Reference Data | color families, fiber, yarn weights/attributes, needles, pattern attributes/categories, project crafts/statuses, photo sizes |
| Search | global search |
| Patterns | search, get, multi-get, comments, highlights, projects, sources |
| Yarns | search, get, multi-get, comments, yarn companies |
| People | current user, profile, comments, friends, library |
| Projects | search, list, get, comments |
| Stash | list, search, unified list, get, comments |
| Queue | list, get item |
| Favorites | list, get |
| Fiber | get, comments |
| Bundles | list, get, bundled items, packs |
| Forums | sets, topics, filtered topics, posts, unread |
| Messages | list, get |
| Shops & Groups | search shops, get shop, stores, store products/purchases, search groups |
| Designers | get |
| Products & Deliveries | get product, attachments, deliveries |
| Drafts & Volumes | draft patterns, volumes, pages |
| App Config | config, data |

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
- [Report an issue](https://github.com/gx1400/ravelry-api/issues)

## License

MIT — see [LICENSE](LICENSE).
