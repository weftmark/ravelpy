# Quickstart

All endpoints are accessed through sub-client attributes on `RavelryClient`.
Every method is a coroutine — `await` it and unpack the `(model, etag, raw_dict)` tuple.

## Search patterns

```python
import asyncio
from ravelpy import RavelryClient

async def main():
    async with RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key") as client:
        data, etag, raw = await client.patterns.search(
            query="socks",
            weight="fingering",
            availability="free",
            page_size=20,
        )
        for pattern in raw["patterns"]:
            print(pattern["name"], "—", pattern["permalink"])

asyncio.run(main())
```

## Get a single pattern

```python
data, etag, raw = await client.patterns.show(pattern_id=7529294)
print(raw["pattern"]["name"])
```

## Search yarns

```python
data, etag, raw = await client.yarns.search(query="merino", weight="fingering")
for yarn in raw["yarns"]:
    print(yarn["name"], "by", yarn["yarn_company_name"])
```

## Fetch yarn colorways

Pass `include="colorways"` to `yarns.show()` to receive colorway data alongside
the yarn detail. Active colorways have `current_status=None`; discontinued ones
have `current_status="discontinued"`.

```python
data, etag, raw = await client.yarns.show(yarn_id=95245, include="colorways")

# Filter to active colorways via the parsed model
active = [c for c in data.colorways if c.current_status is None]
for cw in active:
    print(f"{cw.code or '':8}  {cw.name}")
```

## Look up your profile

Requires a personal key or OAuth token.

```python
personal = RavelryClient(username="your_username", api_key="your_personal_key")

data, etag, raw = await personal.people.me()
print(raw["user"]["username"])
```

## Browse your stash

Stash and pack data require a personal key or OAuth token.

```python
data, etag, raw = await personal.stash.list(username="your_username")
for entry in raw["stash"]:
    print(entry["name"], entry.get("yarn_weight_name", ""))
```

The `Stash` model exposes a `total_skeins` convenience property that sums
skein counts across primary packs. The API's own `total_skeins` field is
`null` for thread and cone-weight yarns — use this property instead:

```python
from ravelpy.models import Stash

data, etag, raw = await personal.stash.show(username="your_username", stash_id=123)
stash = Stash(**raw["stash"])
print(stash.total_skeins)  # sum of skeins from primary packs
```

## ETag caching

Pass an `etag` back to avoid re-downloading unchanged data. The server
returns `304 Not Modified` and `raw` will be `None`.

```python
data, etag, raw = await client.patterns.search(query="socks")

# On the next call, if nothing changed, raw is None
data, etag, raw = await client.patterns.search(query="socks", etag=etag)
if raw is None:
    print("no changes — use your cached copy")
```

## Pagination

```python
page = 1
while True:
    data, etag, raw = await client.patterns.search(query="colorwork", page=page, page_size=100)
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

Resource methods raise two kinds of error, both subclasses of `RavelryError`:

- `RavelryAPIError` — Ravelry responded with a non-2xx status (or a body that
  isn't JSON). Has `status_code` and `message`.
- `RavelryConnectionError` — no response arrived: timeout, DNS failure,
  refused or reset connection. `is_timeout` tells timeouts apart; the original
  httpx exception is available as `__cause__`.

```python
from ravelpy import RavelryClient, RavelryAPIError, RavelryConnectionError

async with RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key") as client:
    try:
        data, etag, raw = await client.patterns.show(pattern_id=0)
    except RavelryAPIError as e:
        print(e.status_code, e.message)
    except RavelryConnectionError as e:
        print("timed out" if e.is_timeout else f"network error: {e}")
```

## Timeouts

Requests time out after 5 seconds by default. Pass `timeout=` to either
constructor — a number of seconds, an `httpx.Timeout` for separate limits, or
`None` to disable timeouts:

```python
import httpx

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key", timeout=30)
client = RavelryClient.from_oauth_token(access_token, timeout=httpx.Timeout(10, connect=2))
```

## Add a yarn to your stash

`Stash.create()` requires a personal key or OAuth token. Pass a dict of
fields; `yarn_id` is the only required one.

```python
async with RavelryClient.from_oauth_token(access_token) as client:
    _, _, raw = await client.stash.create("your_username", {
        "yarn_id": 95245,
        "colorway_name": "Natural",
        "skeins": 3,
    })
    print("New stash ID:", raw["stash"]["id"])
```

## OAuth Bearer tokens

```python
from pathlib import Path
from ravelpy import RavelryClient
from ravelpy.oauth import load_tokens

async def main():
    tokens = load_tokens(Path(".oauth_tokens.json"))
    async with RavelryClient.from_oauth_token(tokens.access_token) as client:
        data, etag, raw = await client.people.me()
        print(raw["user"]["username"])
```

## Refreshing tokens

```python
from ravelpy.oauth import OAuthClient, load_tokens, save_tokens
from pathlib import Path

async def refresh():
    tokens = load_tokens(Path(".oauth_tokens.json"))
    oauth = OAuthClient(client_id="...", client_secret="...")
    new_tokens = await oauth.refresh(tokens.refresh_token)
    save_tokens(new_tokens, Path(".oauth_tokens.json"))
```
