# Quickstart

All endpoints are accessed through sub-client attributes on `RavelryClient`.
Every method returns a `(model, etag, raw_dict)` tuple.

## Search patterns

```python
from ravelpy import RavelryClient

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

data, etag, raw = client.patterns.search(
    query="socks",
    weight="fingering",
    availability="free",
    page_size=20,
)

for pattern in raw["patterns"]:
    print(pattern["name"], "—", pattern["permalink"])
```

## Get a single pattern

```python
data, etag, raw = client.patterns.show(pattern_id=7529294)
print(raw["pattern"]["name"])
```

## Search yarns

```python
data, etag, raw = client.yarns.search(query="merino", weight="fingering")
for yarn in raw["yarns"]:
    print(yarn["name"], "by", yarn["yarn_company_name"])
```

## Fetch yarn colorways

Pass `include="colorways"` to `yarns.show()` to receive colorway data alongside
the yarn detail. Active colorways have `current_status=None`; discontinued ones
have `current_status="discontinued"`.

```python
data, etag, raw = client.yarns.show(yarn_id=95245, include="colorways")

# Filter to active colorways via the parsed model
active = [c for c in data.colorways if c.current_status is None]
for cw in active:
    print(f"{cw.code or '':8}  {cw.name}")
```

## Look up your profile

Requires a personal key or OAuth token.

```python
personal = RavelryClient(username="your_username", api_key="your_personal_key")

data, etag, raw = personal.people.me()
print(raw["user"]["username"])
```

## Browse your stash

Stash and pack data require a personal key or OAuth token.

```python
personal = RavelryClient(username="your_username", api_key="your_personal_key")

data, etag, raw = personal.stash.list(username="your_username")
for entry in raw["stash"]:
    print(entry["name"], entry.get("yarn_weight_name", ""))
```

The `Stash` model exposes a `total_skeins` convenience property that sums
skein counts across primary packs. The API's own `total_skeins` field is
`null` for thread and cone-weight yarns — use this property instead:

```python
from ravelpy.models import Stash

data, etag, raw = personal.stash.show(username="your_username", stash_id=123)
stash = Stash(**raw["stash"])
print(stash.total_skeins)  # sum of skeins from primary packs
```

## ETag caching

Pass an `etag` back to avoid re-downloading unchanged data. The server
returns `304 Not Modified` and `raw` will be `None`.

```python
data, etag, raw = client.patterns.search(query="socks")

# On the next call, if nothing changed, raw is None
data, etag, raw = client.patterns.search(query="socks", etag=etag)
if raw is None:
    print("no changes — use your cached copy")
```

## Pagination

```python
page = 1
while True:
    data, etag, raw = client.patterns.search(query="colorwork", page=page, page_size=100)
    patterns = raw.get("patterns", [])
    if not patterns:
        break
    for p in patterns:
        print(p["name"])
    paginator = raw.get("paginator", {})
    if page >= (paginator.get("last_page") or 1):
        break
    page += 1
```

## Error handling

```python
from ravelpy import RavelryClient, RavelryAPIError

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

try:
    data, etag, raw = client.patterns.show(pattern_id=0)
except RavelryAPIError as e:
    print(e.status_code, e.message)
```

## Async client

`AsyncRavelryClient` mirrors `RavelryClient` exactly but every method is a
coroutine — `await` it or use it as an async context manager:

```python
import asyncio
from ravelpy import AsyncRavelryClient

async def main():
    async with AsyncRavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key") as client:
        data, etag, raw = await client.patterns.search(query="colorwork", page_size=20)
        for pattern in raw["patterns"]:
            print(pattern["name"])

asyncio.run(main())
```

OAuth Bearer tokens work the same way:

```python
from pathlib import Path
from ravelpy import AsyncRavelryClient
from ravelpy.oauth import load_tokens

async def main():
    tokens = load_tokens(Path(".oauth_tokens.json"))
    async with AsyncRavelryClient.from_oauth_token(tokens.access_token) as client:
        data, etag, raw = await client.people.me()
        print(raw["user"]["username"])
```

Refreshing tokens asynchronously uses `AsyncOAuthClient`:

```python
from ravelpy.oauth import AsyncOAuthClient, load_tokens, save_tokens
from pathlib import Path

async def refresh():
    tokens = load_tokens(Path(".oauth_tokens.json"))
    oauth = AsyncOAuthClient(client_id="...", client_secret="...")
    new_tokens = await oauth.refresh(tokens.refresh_token)
    save_tokens(new_tokens, Path(".oauth_tokens.json"))
```
