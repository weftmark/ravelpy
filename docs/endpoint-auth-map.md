# Endpoint Auth Map

Complete list of all endpoints in the ravelpy library, showing the HTTP method, path,
which credential tier is required, and the HTTP status code observed in live testing
with a read-only Basic Auth key.

**Legend**

| Tier            | Meaning                                                                      |
|-----------------|------------------------------------------------------------------------------|
| public          | Accessible with any valid developer credential, including the read-only key  |
| authenticated   | Requires a personal key or OAuth 2.0; read-only key returns 403 or 302      |

**Test conditions:**
- Credential: read-only Basic Auth key (`RAVELRY_USERNAME` / `RAVELRY_API_KEY` from `.env`)
- Placeholder username `tester` used for user-scoped paths
- Placeholder IDs of `1` or `95245` used for resource-scoped paths
- `public` pass: status code is 200, 304, 404, or 500 (any non-auth-rejection)
- `authenticated` pass: status code is 401, 403, or 302

---

## Patterns

| Method | Path                                  | Tier          | Live status | Notes |
|--------|---------------------------------------|---------------|-------------|-------|
| GET    | `/patterns/{id}.json`                 | public        | 404         |       |
| GET    | `/patterns.json?ids=…`                | public        | 404         |       |
| GET    | `/patterns/search.json`               | public        | 200         |       |
| GET    | `/patterns/highlights.json`           | public        | 500         | Intermittent server error on Ravelry's side |
| GET    | `/patterns/{id}/comments.json`        | authenticated | 403         | Docs do not mark as authenticated; auth enforced in practice |
| GET    | `/patterns/{id}/projects.json`        | authenticated | 403         | Docs do not mark as authenticated; auth enforced in practice |

## Yarns

| Method | Path                                  | Tier          | Live status | Notes |
|--------|---------------------------------------|---------------|-------------|-------|
| GET    | `/yarns/{id}.json`                    | public        | 200         |       |
| GET    | `/yarns.json?ids=…`                   | public        | 200         |       |
| GET    | `/yarns/search.json`                  | public        | 200         |       |
| GET    | `/yarns/{id}/comments.json`           | authenticated | 403         | Docs do not mark as authenticated; auth enforced in practice |

## Yarn Companies

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/yarn_companies/search.json`         | public | 200         |       |

## Yarn Attributes (reference data)

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/yarn_attributes/groups.json`        | public | 200         |       |
| GET    | `/yarn_weights.json`                  | public | 200         |       |

## Pattern Attributes (reference data)

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/pattern_attributes/groups.json`     | public | 200         |       |

## Pattern Categories (reference data)

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/pattern_categories/list.json`       | public | 200         |       |

## Pattern Source Types (reference data)

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/pattern_source_types/list.json`     | public | 200         |       |

## Fiber Attribute Groups (reference data)

| Method | Path                                  | Tier          | Live status | Notes |
|--------|---------------------------------------|---------------|-------------|-------|
| GET    | `/fiber_attribute_groups/list.json`   | authenticated | 302         | Redirects to login page; marked public in docs |
| GET    | `/fiber_attributes.json`              | public        | 200         |       |
| GET    | `/fiber_categories.json`              | public        | 200         |       |

## Languages (reference data)

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/languages/list.json`                | public | 200         |       |

## Shops

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/shops/search.json`                  | public | 200         |       |
| GET    | `/shops/{id}.json`                    | public | 404         |       |

## Groups

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/groups/search.json`                 | public | 200         |       |

## Extras (color families, global search)

| Method | Path                                  | Tier   | Live status | Notes |
|--------|---------------------------------------|--------|-------------|-------|
| GET    | `/color_families.json`                | public | 200         |       |
| GET    | `/search.json`                        | public | 200         |       |

## Stores

| Method | Path                                  | Tier          | Live status | Notes |
|--------|---------------------------------------|---------------|-------------|-------|
| GET    | `/stores/list.json`                   | authenticated | 403         | Marked public in docs; auth enforced in practice |
| GET    | `/stores/{id}/products.json`          | authenticated | 403         | Marked public in docs; auth enforced in practice |
| GET    | `/stores/{id}/purchases.json`         | authenticated | 403         | Marked public in docs; auth enforced in practice |

## Pattern Sources

| Method | Path                                          | Tier   | Live status | Notes |
|--------|-----------------------------------------------|--------|-------------|-------|
| GET    | `/pattern_sources/{id}.json`                  | public | 404         |       |
| GET    | `/pattern_sources/search.json`                | public | 200         |       |
| GET    | `/pattern_sources/{id}/patterns.json`         | public | 404         | Marked authenticated in docs; auth not enforced in practice |

## Stash

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/stash/search.json`                                  | authenticated | 403         | Marked public in docs; auth enforced in practice |
| GET    | `/people/{username}/stash/{id}/comments.json`         | authenticated | 403         | Marked public in docs; auth enforced in practice |
| GET    | `/people/{username}/stash/list.json`                  | authenticated | 403         |       |
| GET    | `/people/{username}/stash/{id}.json`                  | authenticated | 403         |       |
| GET    | `/people/{username}/stash/unified/list.json`          | authenticated | 403         |       |

## Projects

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/projects/search.json`                               | public        | 200         |       |
| GET    | `/projects/{username}/list.json`                      | public        | 200         | Marked authenticated in docs; returns empty list for any user |
| GET    | `/projects/{username}/{id}.json`                      | public        | 500         | Marked authenticated in docs; 500 on invalid user/id combo |
| GET    | `/projects/crafts.json`                               | public        | 200         | Marked authenticated in docs; auth not enforced in practice |
| GET    | `/projects/project_statuses.json`                     | public        | 200         | Marked authenticated in docs; auth not enforced in practice |
| GET    | `/projects/{username}/{id}/comments.json`             | authenticated | 403         | Marked public in docs; auth enforced in practice |

## Forums

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/forum_posts/unread.json`                    | authenticated | 403         | Marked public in docs; auth enforced in practice |
| GET    | `/forums/sets.json`                           | authenticated | 403         |       |
| GET    | `/forums/{forum_id}/topics.json`              | authenticated | 403         |       |
| GET    | `/forums/filtered_topics.json`                | authenticated | 403         |       |
| GET    | `/forum_posts/{id}.json`                      | authenticated | 403         |       |

## Topics

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/topics/{id}.json`                           | authenticated | 403         |       |
| GET    | `/topics/{id}/posts.json`                     | authenticated | 403         |       |

## Saved Searches

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/saved_searches/list.json`                   | authenticated | 403         | Marked public in docs; auth enforced in practice |

## Drafts

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/drafts/patterns/list.json`                  | authenticated | 403         | Marked public in docs; auth enforced in practice |
| GET    | `/drafts/patterns/{id}.json`                  | authenticated | 403         | Marked public in docs; auth enforced in practice |

## Deliveries

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/deliveries/list.json`                       | authenticated | 403         | Requires `deliveries-read` OAuth scope; personal key grants automatically |

## People

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/current_user.json`                                  | authenticated | 403         |       |
| GET    | `/people/{username}.json`                             | authenticated | 403         |       |
| GET    | `/people/{username}/comments/list.json`               | authenticated | 403         |       |

## Fiber

| Method | Path                                                  | Tier   | Live status | Notes |
|--------|-------------------------------------------------------|--------|-------------|-------|
| GET    | `/people/{username}/fiber/{id}.json`                  | public | 404         | Marked authenticated in docs; auth not enforced in practice |
| GET    | `/people/{username}/fiber/{id}/comments.json`         | public | 404         |       |

## App

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/app/config/get.json`                        | authenticated | 403         |       |
| GET    | `/app/data/get.json`                          | authenticated | 403         |       |

## Photos

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/photos/dimensions.json`                     | authenticated | 403         |       |
| GET    | `/photos/{id}/sizes.json`                     | authenticated | 403         |       |
| GET    | `/photos/status.json`                         | authenticated | 403         |       |

## Designers

| Method | Path                                          | Tier   | Live status | Notes |
|--------|-----------------------------------------------|--------|-------------|-------|
| GET    | `/designers/{id}.json`                        | public | 200         | Marked authenticated in docs; auth not enforced in practice |

## Products

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/products/{id}.json`                         | authenticated | 403         |       |
| GET    | `/products/{id}/attachments.json`             | authenticated | 403         |       |

## Product Attachments

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/product_attachments/{id}.json`              | authenticated | 403         |       |

## Bundled Items

| Method | Path                                          | Tier   | Live status | Notes |
|--------|-----------------------------------------------|--------|-------------|-------|
| GET    | `/bundled_items/{id}.json`                    | public | 404         | Marked authenticated in docs; auth not enforced in practice |

## Bundles

| Method | Path                                                  | Tier   | Live status | Notes |
|--------|-------------------------------------------------------|--------|-------------|-------|
| GET    | `/people/{username}/bundles/list.json`                | public | 200         | Marked authenticated in docs; returns empty list for any user |
| GET    | `/people/{username}/bundles/{id}.json`                | public | 404         | Marked authenticated in docs; auth not enforced in practice |

## Favorites

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/people/{username}/favorites/list.json`              | authenticated | 403         |       |
| GET    | `/people/{username}/favorites/{id}.json`              | authenticated | 403         |       |

## Friends

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/people/{username}/friends/list.json`                | authenticated | 403         |       |
| GET    | `/people/{username}/friends/activity.json`            | authenticated | 403         |       |

## Library

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/people/{username}/library/search.json`              | authenticated | 403         |       |

## Messages

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/messages/list.json`                         | authenticated | 403         | Sending requires `message-write` OAuth scope (not yet in library) |
| GET    | `/messages/{id}.json`                         | authenticated | 403         |       |

## Needles

| Method | Path                                                  | Tier          | Live status | Notes |
|--------|-------------------------------------------------------|---------------|-------------|-------|
| GET    | `/people/{username}/needles/list.json`                | authenticated | 403         |       |
| GET    | `/needles/sizes.json`                                 | public        | 200         | Marked authenticated in docs; auth not enforced in practice |
| GET    | `/needles/types.json`                                 | public        | 200         | Marked authenticated in docs; auth not enforced in practice |

## Packs

| Method | Path                                          | Tier   | Live status | Notes |
|--------|-----------------------------------------------|--------|-------------|-------|
| GET    | `/packs/{id}.json`                            | public | 200         | Marked authenticated in docs; auth not enforced in practice |

## Pages

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/pages/{id}.json`                            | authenticated | 403         |       |

## Volumes

| Method | Path                                          | Tier          | Live status | Notes |
|--------|-----------------------------------------------|---------------|-------------|-------|
| GET    | `/volumes/{id}.json`                          | authenticated | 403         |       |

## Queue

| Method | Path                                                  | Tier   | Live status | Notes |
|--------|-------------------------------------------------------|--------|-------------|-------|
| GET    | `/people/{username}/queue/list.json`                  | public | 200         | Marked authenticated in docs; returns empty list for any user |
| GET    | `/people/{username}/queue/{id}.json`                  | public | 404         | Marked authenticated in docs; auth not enforced in practice |
