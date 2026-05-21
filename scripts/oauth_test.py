#!/usr/bin/env python3
"""Smoke test an OAuth 2.0 token against a representative set of Ravelry endpoints.

Loads .oauth_tokens.json, builds a RavelryClient with Bearer auth, and calls a
selection of endpoints across different auth tiers to verify the token works.

Usage:
    python scripts/oauth_test.py

Run scripts/oauth_login.py first to obtain a token.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
TOKEN_PATH = ROOT / ".oauth_tokens.json"

if not TOKEN_PATH.exists():
    sys.exit(f"No token file at {TOKEN_PATH}. Run scripts/oauth_login.py first.")

from ravelpy import RavelryClient, RavelryAPIError
from ravelpy.oauth import load_tokens

tokens = load_tokens(TOKEN_PATH)
client = RavelryClient.from_oauth_token(tokens.access_token)

# (label, expected_to_pass, callable)
CASES: list[tuple[str, bool, object]] = [
    # Public endpoints — should always succeed
    ("patterns.search",        True,  lambda: client.patterns.search(query="hat")),
    ("yarns.show",             True,  lambda: client.yarns.show(yarn_id=95245)),
    ("extras.color_families",  True,  lambda: client.extras.color_families()),
    # Authenticated endpoints — should succeed with a valid OAuth token
    ("people.me",              True,  lambda: client.people.me()),
    ("saved_searches.list",    True,  lambda: client.saved_searches.list()),
    ("forums.sets",            True,  lambda: client.forums.sets()),
    ("needles.sizes",          True,  lambda: client.needles.sizes()),
    ("messages.list",          True,  lambda: client.messages.list()),
]

col_label = 28
col_result = 10

header = f"{'Endpoint':<{col_label}} {'Result':<{col_result}} Detail"
sep = "-" * 70
print(header)
print(sep)

pass_count = fail_count = 0

for label, should_pass, call in CASES:
    try:
        parsed, etag, raw = call()
        status = "OK"
        detail = f"etag={etag}"
        if should_pass:
            pass_count += 1
        else:
            fail_count += 1
            status = "UNEXPECTED OK"
    except RavelryAPIError as e:
        status = f"HTTP {e.status_code}"
        detail = e.message[:60] if e.message else ""
        if should_pass:
            fail_count += 1
        else:
            pass_count += 1
    except Exception as e:
        status = "ERROR"
        detail = str(e)[:60]
        fail_count += 1

    print(f"{label:<{col_label}} {status:<{col_result}} {detail}")

print(sep)
print(f"Passed: {pass_count}  Failed: {fail_count}")
if fail_count:
    print("\nIf authenticated endpoints return 401, the token may have expired.")
    print("Run scripts/oauth_refresh.py (or oauth_login.py to re-authorize).")
