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
| `client.stash` | `list`, `search`, `unified_list`, `show`, `comments` | personal |
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

---

## Pagination

Methods that return lists accept `page` and `page_size` parameters. The raw
response includes a `paginator` dict with `page`, `page_size`, `results`,
and `last_page` fields.

```python
data, etag, raw = client.patterns.search(query="colorwork", page=1, page_size=100)
paginator = raw.get("paginator", {})
print(f"Page {paginator['page']} of {paginator['last_page']}")
```

## ETag caching

Every method accepts an optional `etag` keyword argument. See
[Quickstart](quickstart.md) for a full example.
