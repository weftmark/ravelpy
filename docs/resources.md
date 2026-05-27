# Resources

Every resource is a sub-client attribute on `RavelryClient`. The table below
lists each sub-client, its available methods, and the minimum credential tier
required.

**Auth tiers:** `public` = read-only key works; `personal` = personal key or
OAuth required; `scope` = specific OAuth scope needed.

| Sub-client | Methods | Auth |
| --- | --- | --- |
| `client.patterns` | `search`, `show`, `list`, `comments`, `highlights`, `projects` | `search`/`show`/`list`/`highlights` → public; others → personal |
| `client.pattern_sources` | `show`, `search`, `patterns` | public |
| `client.yarns` | `show`, `list`, `search`, `comments` | `show`/`list`/`search` → public; `comments` → personal |
| `client.yarn_companies` | `search` | public |
| `client.reference` | `color_families`, `fiber_attributes`, `fiber_categories`, `yarn_weights`, `yarn_attribute_groups`, `pattern_attributes`, `pattern_categories`, `pattern_source_types`, `languages`, `photo_sizes` | public |
| `client.people` | `me`, `show`, `comments` | personal |
| `client.projects` | `search`, `list`, `show`, `comments`, `crafts`, `statuses` | `search`/`list`/`crafts`/`statuses` → public; others → personal |
| `client.stash` | `list`, `search`, `unified_list`, `show`, `comments`, `create` | personal / OAuth |
| `client.queue` | `list`, `show` | public (returns empty for other users) |
| `client.favorites` | `list`, `show` | personal |
| `client.fiber` | `show`, `comments` | public |
| `client.bundles` | `list`, `show`, `bundled_items`, `packs` | public |
| `client.shops` | `search`, `show` | public |
| `client.groups` | `search` | public |
| `client.stores` | `list`, `products`, `purchases` | `list` → `patternstore-read` scope; `purchases` → `patternstore-purchases` scope |
| `client.forums` | `sets`, `topics`, `filtered_topics`, `post`, `unread_posts` | personal |
| `client.topics` | `show`, `posts` | personal |
| `client.messages` | `list`, `show` | personal key only (no OAuth scope grants read access) |
| `client.needles` | `list`, `sizes`, `types` | `sizes`/`types` → public; `list` → personal |
| `client.designers` | `show` | public |
| `client.products` | `show`, `attachments` | personal |
| `client.deliveries` | `list` | `deliveries-read` scope |
| `client.drafts` | `list`, `show` | `patternstore-read` scope; scoped to current user's pattern store |
| `client.volumes` | `show` | personal |
| `client.pages` | `show` | personal |
| `client.packs` | `show` | public |
| `client.friends` | `list`, `activity` | personal |
| `client.library` | `search` | personal |
| `client.saved_searches` | `list` | personal |
| `client.app` | `config`, `data` | personal |
| `client.extras` | `color_families`, `search` | public |
| `client.photos` | `dimensions`, `sizes`, `status` | personal |
| `client.colorways` | *(see note below)* | public |

---

## Colorway model

`Colorway` objects appear in `YarnResponse.colorways` when `yarns.show()` is
called with `include="colorways"`. Each colorway represents one named colour
variant of a yarn.

Key fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `int` | Ravelry colorway ID |
| `name` | `str \| None` | Colour name (e.g. `"Kaki"`) |
| `code` | `str \| None` | Yarn-company colour code |
| `current_status` | `str \| None` | `None` = active; `"discontinued"` = no longer produced |
| `photos` | `list[ColorwayPhoto]` | Always empty from the yarn embed — see note below |
| `projects_count` | `int \| None` | Projects using this colorway |
| `stashes_count` | `int \| None` | Stash entries using this colorway |

### Fetching colorways

Pass `include="colorways"` to `yarns.show()`. The colorways come back as a
top-level `colorways` key in the raw response **and** populate
`YarnResponse.colorways` in the parsed result:

```python
data, etag, raw = await client.yarns.show(yarn_id=95245, include="colorways")

# via parsed model
active = [c for c in data.colorways if c.current_status is None]
for cw in active:
    print(cw.name, cw.code)

# via raw dict
for cw in raw["colorways"]:
    print(cw["name"], cw.get("current_status"))
```

You can combine `colorways` with `availability` in a single call:

```python
data, etag, raw = await client.yarns.show(yarn_id=95245, include="colorways availability")
```

### Colorway photos — API limitation

`Colorway.photos` is **always empty** from the yarn embed — the Ravelry API
does not include photo data in that response.

There is no public Ravelry endpoint that returns colorway-specific photos:

- `GET /colorways/{id}.json` redirects to the login page for all developer
  credential types (Basic Auth and OAuth 2.0).
- `GET /projects/search.json` accepts a `colorway_id` query parameter, but
  the parameter is **silently ignored** by the API — every call returns the
  same top project for the yarn regardless of the colorway requested.  This
  was confirmed with both a read-only Basic Auth key and a user OAuth 2.0
  Bearer token.

`client.colorways` is retained as a namespace for future helpers if a valid
endpoint is discovered, but it exposes no methods at this time.

---

## Pack model

`Pack` objects appear in `Stash.packs`, `Project.packs`, and the individual
`GET /packs/{id}.json` endpoint. Each pack represents one yarn in a stash
entry or project, and includes skein counts, total yardage/weight, and
per-skein measurements.

Key fields:

| Field | Type | Notes |
| --- | --- | --- |
| `skeins` | `float` | Skein count for this pack — the reliable source of quantity |
| `primary_pack_id` | `int \| None` | `None` on the primary pack; set on secondary packs |
| `total_yards` / `total_meters` | `float` | Total yardage/meterage across all skeins |
| `total_grams` / `total_ounces` | `float` | Total weight |
| `yards_per_skein` / `grams_per_skein` | `float` | Per-skein measurements |
| `quantity_description` | `str` | Human-readable e.g. `"2 skeins = 400 yards"` |
| `shop_name` / `shop_id` | `str / int` | Where the yarn was purchased |

### Stash.total_skeins

`Stash` exposes a `total_skeins` property that sums `skeins` across primary
packs (those where `primary_pack_id is None`). The API's own `total_skeins`
field is `null` for thread and cone-weight yarns — use the property instead:

```python
from ravelpy.models import Stash

_, _, raw = await client.stash.show(username="you", stash_id=123)
stash = Stash(**raw["stash"])
print(stash.total_skeins)
```

---

## Pagination

Methods that return lists accept `page` and `page_size` parameters. The raw
response includes a `paginator` dict with `page`, `page_size`, `results`,
and `last_page` fields.

```python
data, etag, raw = await client.patterns.search(query="colorwork", page=1, page_size=100)
paginator = raw.get("paginator", {})
print(f"Page {paginator['page']} of {paginator['last_page']}")
```

## ETag caching

Every method accepts an optional `etag` keyword argument. See
[Quickstart](quickstart.md) for a full example.

---

## Writing stash entries

`Stash.create()` is the first write method in ravelpy. It requires a personal
key or an OAuth 2.0 Bearer token (the `offline` scope is sufficient).

```python
from ravelpy import RavelryClient

async with RavelryClient.from_oauth_token(access_token) as client:
    _, _, raw = await client.stash.create("your_username", {
        "yarn_id": 95245,
        "colorway_name": "Natural",
        "dye_lot": "A42",
        "notes": "Bought at local yarn store",
        "skeins": 3,
        "grams_per_skein": 100,
        "yards_per_skein": 220,
    })
    stash_id = raw["stash"]["id"]
    print(f"Created stash entry #{stash_id}")
```

Common `payload` fields:

| Field | Type | Notes |
| --- | --- | --- |
| `yarn_id` | `int` | **Required.** Ravelry yarn ID. |
| `colorway_name` | `str` | Colour name as shown on the label. |
| `dye_lot` | `str` | Dye lot identifier. |
| `notes` | `str` | Free-text notes. |
| `stash_status_id` | `int` | `1` = in stock, `2` = used up, `3` = gifted/sold. |
| `skeins` | `float` | Number of skeins. |
| `grams_per_skein` | `float` | Weight per skein in grams. |
| `yards_per_skein` | `float` | Length per skein in yards. |

The response envelope is `{"stash": {...}}` — `raw["stash"]["id"]` is the new entry's ID.
