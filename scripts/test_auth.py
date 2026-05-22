#!/usr/bin/env python3
"""Live API smoke test — validates auth tier requirements against real endpoints.

Loads credentials from an env file and calls every endpoint in the library.
Reports the actual HTTP status code and whether it matches the expected auth tier:

  public        → expect 200 or 404  (credential accepted; resource may not exist)
  authenticated → expect 401 or 403  (credential rejected) with read-only key
                  OR expect 200/404 with --personal-key or --oauth-token-file

Usage:
    python scripts/test_auth.py
    python scripts/test_auth.py --env-file .env.user.read
    python scripts/test_auth.py --api-user read-xxxx --api-key yourkey
    python scripts/test_auth.py --personal-key --env-file .env.user.readwrite
    python scripts/test_auth.py --oauth-token-file .oauth_tokens.json
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from _test_cases import BASE_URL, CASES, Case, TEST_USER  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ravelry API auth smoke test")
    p.add_argument(
        "--env-file",
        metavar="FILE",
        default=str(ROOT / ".env.developer.readonly"),
        help="Env file to load credentials from (default: .env.developer.readonly)",
    )
    p.add_argument("--api-user", metavar="USERNAME", help="Ravelry username (overrides env file)")
    p.add_argument("--api-key",  metavar="KEY",      help="Ravelry API key (overrides env file)")
    p.add_argument(
        "--personal-key",
        action="store_true",
        help=(
            "Key is a personal account key (access_key/personal_key) rather than a "
            "developer read-only key. Flips 'authenticated' expectation: personal keys "
            "are accepted (200/404) instead of rejected (401/403)."
        ),
    )
    p.add_argument(
        "--oauth-token-file",
        metavar="FILE",
        help=(
            "Path to a JSON token file produced by oauth_login.py (default: .oauth_tokens.json). "
            "Uses Bearer auth instead of Basic Auth. Implies --personal-key."
        ),
    )
    return p.parse_args()


args = _parse_args()

# ── Resolve auth: OAuth Bearer token takes priority over Basic Auth ──────────
import json as _json

OAUTH_TOKEN: Optional[str] = None

if args.oauth_token_file:
    token_path = Path(args.oauth_token_file)
    if not token_path.exists():
        sys.exit(f"Token file not found: {token_path}. Run scripts/oauth_login.py first.")
    OAUTH_TOKEN = _json.loads(token_path.read_text()).get("access_token", "")
    if not OAUTH_TOKEN:
        sys.exit(f"No access_token found in {token_path}.")
    USERNAME = API_KEY = ""  # not used with Bearer auth
else:
    load_dotenv(Path(args.env_file))
    USERNAME = args.api_user or os.environ.get("RAVELRY_USERNAME", "")
    API_KEY  = args.api_key  or os.environ.get("RAVELRY_API_KEY",  "")
    if not USERNAME or not API_KEY:
        sys.exit(f"Credentials required: set RAVELRY_USERNAME/RAVELRY_API_KEY in {args.env_file} or pass --api-user/--api-key")



def run() -> None:
    personal = args.personal_key or bool(OAUTH_TOKEN)

    if OAUTH_TOKEN:
        session = httpx.Client(
            headers={"Accept": "application/json", "Authorization": f"Bearer {OAUTH_TOKEN}"},
            timeout=15.0,
        )
    else:
        session = httpx.Client(auth=(USERNAME, API_KEY), headers={"Accept": "application/json"}, timeout=15.0)

    results: list[tuple[Case, int]] = []
    for case in CASES:
        clean = {k: v for k, v in case.params.items() if v is not None}
        r = session.get(f"{BASE_URL}{case.path}", params=clean)
        results.append((case, r.status_code))

    session.close()

    # ── Print table ──────────────────────────────────────────────────────────
    col_resource = 22
    col_method   = 16
    col_path     = 52
    col_exp      = 7
    col_got      = 5

    if OAUTH_TOKEN:
        key_mode = "OAuth Bearer token (authenticated -> expect 200/404)"
    elif personal:
        key_mode = "personal key (authenticated -> expect 200/404)"
    else:
        key_mode = "read-only key (authenticated -> expect 401/403)"
    header = (
        f"{'Resource':<{col_resource}} {'Method':<{col_method}} {'Path':<{col_path}} "
        f"{'Exp':<{col_exp}} {'Got':<{col_got}} Match  Note"
    )
    sep = "-" * len(header)
    print(f"Key mode: {key_mode}")
    print(header)
    print(sep)

    pass_count = fail_count = special_count = 0

    REJECTED = (401, 403, 302)

    for case, status in results:
        if case.expected == "public":
            # 200/304/404/500 indicate credential accepted; 302→login or 401/403 = rejected
            match = status not in REJECTED
        elif case.expected == "authenticated":
            if personal:
                # Personal key should be accepted on authenticated endpoints
                match = status not in REJECTED
            else:
                # Read-only key should be rejected on authenticated endpoints
                match = status in REJECTED
        else:
            match = None  # special / unknown

        if match is None:
            symbol = "----"
            special_count += 1
        elif match:
            symbol = "OK"
            pass_count += 1
        else:
            symbol = "FAIL"
            fail_count += 1

        path_display = case.path
        if len(path_display) > col_path:
            path_display = path_display[:col_path - 1] + "…"

        print(
            f"{case.resource:<{col_resource}} {case.method:<{col_method}} "
            f"{path_display:<{col_path}} {case.expected:<{col_exp}} {status:<{col_got}} "
            f"{symbol:<6} {case.note}"
        )

    print(sep)
    print(f"Passed: {pass_count}  Failed: {fail_count}  Special (manual review): {special_count}")
    print()
    if fail_count:
        print("FAILURES — check docstring auth annotations for the entries marked FAIL above.")
    else:
        print("All tested endpoints matched expected auth tier.")


if __name__ == "__main__":
    run()
