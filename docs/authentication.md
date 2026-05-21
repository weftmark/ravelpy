# Ravelry API Authentication

## Overview

The Ravelry API uses HTTP Basic Auth for all requests. The credential pair you supply
determines which endpoints are accessible. Three distinct credential tiers exist, each
granting a different scope.

---

## Credential Tiers

### 1. Read-Only Basic Auth Key

**Source:** Ravelry developer portal — `basic_auth_username` / `basic_auth_password`.

**Scope:** Public catalog data only. Endpoints not marked *authenticated* in the Ravelry
docs are generally accessible with this credential, though live testing reveals several
exceptions where undocumented enforcement applies (see notes in
[endpoint-auth-map.md](endpoint-auth-map.md)).

**Use case:** Querying patterns, yarns, shops, groups, search — anything that is
inherently public on Ravelry.com.

```python
client = RavelryClient(username="read-xxxx", api_key="basic_auth_password")
```

### 2. Personal Account Access (Personal Key)

**Source:** Ravelry developer portal — `access_key` / `personal_key`.

**Scope:** Full access to the associated Ravelry account. All OAuth permission scopes
are granted automatically — no explicit scopes are needed. This is the simplest
credential for personal tooling.

**Use case:** Reading or writing your own stash, projects, queue, messages, favorites,
needles, library, etc.

```python
client = RavelryClient(username="access_key_value", api_key="personal_key_value")
```

### 3. OAuth 2.0

**Source:** Client-ID / client-secret flow at `https://www.ravelry.com/oauth2/auth`.

**Scope:** Depends on scopes requested. Tokens expire after 24 hours; request `offline`
to receive a refresh token.

**Use case:** Apps that act on behalf of other Ravelry users.

**Note:** OAuth is not natively wired into `RavelryClient`. Supply an OAuth access token
as `api_key` and the authorizing user's Ravelry username as `username` to use it manually.

```python
client = RavelryClient(username="ravelry_username", api_key="oauth_access_token")
```

#### Available OAuth Scopes

| Scope              | Grants access to                                        |
|--------------------|---------------------------------------------------------|
| `offline`          | Refresh tokens (long-lived sessions)                    |
| `forum-write`      | Posting to forums                                       |
| `message-write`    | Sending messages                                        |
| `patternstore-read`| Reading pattern store data                              |
| `patternstore-pdf` | Downloading PDFs from the pattern store                 |
| `deliveries-read`  | Reading delivery records                                |
| `library-pdf`      | Downloading library PDFs                                |
| `profile-only`     | Read-only profile access                                |
| `carts-only`       | Cart/checkout access                                    |

---

## How Authentication Works

All requests use HTTP Basic Auth:

```
Authorization: Basic base64(username:api_key)
```

The Ravelry API signals auth failures with:

- **403 Forbidden** — most common response when the credential is insufficient
- **302 → login page** — seen on some endpoints when no credentials are present or
  credentials are insufficient (e.g., `fiber_attribute_groups/list`)
- **401 Unauthorized** — less common; may appear on some endpoints

A **200 OK** or **404 Not Found** response confirms the credential was accepted (the
resource may simply not exist for 404s).

---

## Key Findings from Live Testing

The official Ravelry API documentation marks certain endpoints as *authenticated* using
a small tag in the HTML source. Live testing with a read-only Basic Auth key revealed
several discrepancies:

### Endpoints marked authenticated in docs but publicly accessible in practice

These endpoints return 200/404 with a read-only key — auth is not enforced:

- `GET /designers/{id}.json`
- `GET /packs/{id}.json`
- `GET /needles/sizes.json` and `/needles/types.json`
- `GET /pattern_sources/{id}/patterns.json`
- `GET /people/{username}/fiber/{id}.json`
- `GET /bundled_items/{id}.json`
- `GET /people/{username}/bundles/list.json` and `…/bundles/{id}.json`
- `GET /people/{username}/queue/list.json` and `…/queue/{id}.json`
- `GET /projects/{username}/list.json`, `/projects/crafts.json`, `/projects/project_statuses.json`

### Endpoints not marked authenticated in docs but requiring auth in practice

These endpoints return 403 with a read-only key — auth is enforced despite the docs:

- `GET /stores/list.json`, `/stores/{id}/products.json`, `/stores/{id}/purchases.json`
- `GET /stash/search.json`, `/people/{username}/stash/{id}/comments.json`
- `GET /patterns/{id}/comments.json`, `/patterns/{id}/projects.json`
- `GET /yarns/{id}/comments.json`
- `GET /projects/{username}/{id}/comments.json`
- `GET /forum_posts/unread.json`
- `GET /saved_searches/list.json`
- `GET /drafts/patterns/list.json`, `/drafts/patterns/{id}.json`

### Deliveries

`GET /deliveries/list.json` is not marked *authenticated* in the docs but returns 403
with the read-only key. It requires the `deliveries-read` OAuth scope, which the personal
key grants automatically.

### fiber_attribute_groups/list

`GET /fiber_attribute_groups/list.json` returns a 302 redirect to the Ravelry login
page with the read-only key. The other two fiber attribute endpoints (`/fiber_attributes.json`
and `/fiber_categories.json`) are publicly accessible.

### patterns/highlights

`GET /patterns/highlights.json` returns a 500 Internal Server Error regardless of
credential. This appears to be an intermittent Ravelry API bug, not an auth enforcement.

---

## Using the Test Script

A live API smoke test script is provided at [`scripts/test_auth.py`](../scripts/test_auth.py).
It loads credentials from `.env` and calls every endpoint, reporting the actual HTTP
status code against the expected auth tier.

```
python scripts/test_auth.py
```

Requires `.env` with:

```
RAVELRY_USERNAME=read-xxxx
RAVELRY_API_KEY=your-key
```
