# Ravelry API Authentication

## Overview

The Ravelry API supports two authentication mechanisms: HTTP Basic Auth (for
developer and personal keys) and OAuth 2.0 Bearer tokens. Three distinct
credential tiers exist, each granting a different level of access.

---

## Credential Tiers

### 1. Read-Only Basic Auth Key

**Source:** Ravelry developer portal — `basic_auth_username` / `basic_auth_password`.

**Format:** Username begins with `read-`.

**Scope:** Public catalog data only. Cannot access authenticated endpoints.

**Use case:** Querying patterns, yarns, shops, groups, search — anything inherently
public on Ravelry.com.

```python
client = RavelryClient(username="read-xxxx", api_key="basic_auth_password")
```

---

### 2. Personal Account Access (Personal Key)

**Source:** Ravelry developer portal — `access_key` / `personal_key`.

**Format:** Username does **not** begin with `read-`.

**Scope:** Full read and write access to the associated Ravelry account. All OAuth
permission scopes are granted automatically — no explicit scope list is needed.
This is the simplest credential for personal tooling.

**Use case:** Reading or writing your own stash, projects, queue, messages,
favorites, needles, library, forums, etc.

```python
client = RavelryClient(username="access_key_value", api_key="personal_key_value")
```

---

### 3. OAuth 2.0

**Source:** Client-ID / client-secret flow; see [`scripts/oauth_login.py`](../scripts/oauth_login.py).

**Transport:** Bearer token in `Authorization` header (not Basic Auth).

**Scope:** Determined by the scopes requested during authorization. Tokens expire
after 24 hours; request the `offline` scope to receive a refresh token for
silent renewal.

**Use case:** Apps that act on behalf of other Ravelry users, or when scoped
permissions are required.

```python
from ravelpy import RavelryClient
from ravelpy.oauth import load_tokens
from pathlib import Path

tokens = load_tokens(Path(".oauth_tokens.json"))
client = RavelryClient.from_oauth_token(tokens.access_token)
```

#### Available OAuth Scopes (`OAuthScope` enum)

All valid scope values are codified in `ravelpy.OAuthScope`.

| Scope                | Constant                       | Grants access to                                                                   |
|----------------------|--------------------------------|------------------------------------------------------------------------------------|
| `offline`            | `OAuthScope.OFFLINE`           | Refresh tokens (long-lived sessions)                                               |
| `forum-write`        | `OAuthScope.FORUM_WRITE`       | Create, edit, and delete forum posts                                               |
| `message-write`      | `OAuthScope.MESSAGE_WRITE`     | Send and delete private messages                                                   |
| `patternstore-read`  | `OAuthScope.PATTERNSTORE_READ` | Enumerate user's pattern stores and products                                       |
| `patternstore-pdf`   | `OAuthScope.PATTERNSTORE_PDF`  | Generate PDF download links from pattern stores (limited access, by request)       |
| `deliveries-read`    | `OAuthScope.DELIVERIES_READ`   | List purchased or gifted products                                                  |
| `library-pdf`        | `OAuthScope.LIBRARY_PDF`       | Download PDFs from library (tokens expire faster; may also expire on rate limit)   |
| `profile-only`       | `OAuthScope.PROFILE_ONLY`      | `/current_user.json` only                                                          |
| `carts-only`         | `OAuthScope.CARTS_ONLY`        | `/carts/*.json` only                                                               |

**Note:** There is no `message-read` scope. Message list/read access is only available
via personal keys, not OAuth tokens.

---

## Personal Key vs. OAuth: Behavioural Differences

Live testing shows three endpoints accessible with a personal key that return 403
with an OAuth Bearer token, even with a fully-scoped token. No documented scope
grants access to these endpoints via OAuth:

| Endpoint                         | Personal key | OAuth token |
|----------------------------------|:------------:|:-----------:|
| `GET /stores/list.json`          | 200          | 403         |
| `GET /drafts/patterns/list.json` | 200          | 403         |
| `GET /messages/list.json`        | 200          | 403         |

For applications that need these endpoints, a personal key is required. OAuth tokens
are equivalent to personal keys for all other endpoints (that aren't ownership-gated).

---

## HTTP Authentication

### Basic Auth (developer and personal keys)

```
Authorization: Basic base64(username:api_key)
```

### Bearer Token (OAuth 2.0)

```
Authorization: Bearer <access_token>
```

### Auth failure signals

| Status           | Meaning                                                                    |
|------------------|----------------------------------------------------------------------------|
| 403 Forbidden    | Most common rejection; credential is insufficient for this endpoint        |
| 302 → login      | Credential missing or insufficient; seen on `fiber_attribute_groups/list`  |
| 401 Unauthorized | OAuth token has expired or been revoked                                    |

A **200 OK** or **404 Not Found** confirms the credential was accepted (404 means
the resource doesn't exist, not a credential problem).

---

## HTTP Status Code Reference

| Code | Meaning                                                                   |
|------|---------------------------------------------------------------------------|
| 400  | Bad Request — invalid parameters                                          |
| 401  | Unauthorized — OAuth token expired or revoked                             |
| 403  | Forbidden — credential not permitted for this endpoint                    |
| 404  | Not Found — resource does not exist                                       |
| 405  | Method Not Allowed — wrong HTTP verb                                      |
| 413  | Request Entity Too Large — POST body exceeds per-method limit             |
| 429  | Too Many Requests — rate limit exceeded                                   |
| 500  | Server Error — bug on Ravelry's side; they receive notification           |
| 503  | Service Unavailable — API is down                                         |
| 504  | Gateway Timeout — response took more than 10 seconds; reduce page size    |

---

## Key Findings from Live Testing

The official docs mark endpoints as *authenticated* via an HTML tag. Live testing with
all three credential tiers revealed many discrepancies.

### Endpoints marked authenticated in docs but publicly accessible

These return 200/404 with a read-only developer key — auth is not enforced:

- `GET /designers/{id}.json`
- `GET /packs/{id}.json`
- `GET /needles/sizes.json` and `/needles/types.json`
- `GET /pattern_sources/{id}/patterns.json`
- `GET /people/{username}/fiber/{id}.json` and `/fiber/{id}/comments.json`
- `GET /bundled_items/{id}.json`
- `GET /people/{username}/bundles/list.json` and `…/bundles/{id}.json`
- `GET /people/{username}/queue/list.json` and `…/queue/{id}.json`
- `GET /projects/{username}/list.json`, `/projects/crafts.json`, `/projects/project_statuses.json`

### Endpoints not marked authenticated in docs but requiring auth

These return 403 with a read-only key — auth is enforced despite the docs:

- `GET /stores/list.json`, `/stores/{id}/products.json`, `/stores/{id}/purchases.json`
- `GET /stash/search.json`, `/people/{username}/stash/{id}/comments.json`
- `GET /patterns/{id}/comments.json`, `/patterns/{id}/projects.json`
- `GET /yarns/{id}/comments.json`
- `GET /projects/{username}/{id}/comments.json`
- `GET /forum_posts/unread.json`
- `GET /saved_searches/list.json`
- `GET /drafts/patterns/list.json`, `/drafts/patterns/{id}.json`

### Special cases

- **`GET /deliveries/list.json`** — requires `deliveries-read` OAuth scope; personal key grants automatically.
- **`GET /fiber_attribute_groups/list.json`** — returns 302 redirect to login page with any credential type tested, including personal key and OAuth.
- **`GET /patterns/highlights.json`** — returns 500 regardless of credential; intermittent Ravelry server bug.
- **`GET /forums/filtered_topics.json`** — returns 400 (missing required parameters) with personal key and OAuth; 403 with read-only key.

---

## Using the Test Script

```bash
# Read-only developer key (default)
python scripts/test_auth.py

# Personal account key
python scripts/test_auth.py --personal-key --env-file .env.user.readwrite

# OAuth Bearer token
python scripts/test_auth.py --oauth-token-file .oauth_tokens.json
```
