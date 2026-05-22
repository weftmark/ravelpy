#!/usr/bin/env python3
"""Test a single endpoint against every OAuth scope combination.

Authorizes once per scope via the manual browser flow and records the HTTP
status code for the given path.  Useful for investigating a specific endpoint
without re-running the full scope matrix.

Usage:
    python scripts/probe_endpoint.py /patterns/7529294/comments.json
    python scripts/probe_endpoint.py /patterns/7529294/comments.json --env-file .env.oauth.personal
"""

import argparse
import os
import sys
import urllib.parse
import webbrowser
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from ravelpy.oauth import OAuthClient

SCOPE_MATRIX: list[tuple[str, list[str]]] = [
    ("baseline",           ["offline"]),
    ("forum-write",        ["offline", "forum-write"]),
    ("message-write",      ["offline", "message-write"]),
    ("patternstore-read",  ["offline", "patternstore-read"]),
    ("deliveries-read",    ["offline", "deliveries-read"]),
    ("library-pdf",        ["offline", "library-pdf"]),
]

BASE_URL = "https://api.ravelry.com"


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Probe one endpoint across all OAuth scopes")
    p.add_argument("path", help="API path to test (e.g. /patterns/7529294/comments.json)")
    p.add_argument("--env-file", default=str(ROOT / ".env.oauth.personal"))
    p.add_argument("--oauth-clientid", metavar="ID")
    p.add_argument("--oauth-secret",   metavar="SECRET")
    p.add_argument(
        "--scopes", nargs="+",
        choices=[n for n, _ in SCOPE_MATRIX],
        help="Subset of scopes to test (default: all)",
    )
    return p.parse_args()


def _authorize(client: OAuthClient, scopes: list[str], scope_name: str) -> str:
    url, _ = client.auth_url(scopes)
    print(f"\n{'=' * 60}")
    print(f"  Scope: {scope_name!r}  ({' '.join(scopes)})")
    print(f"{'=' * 60}")
    print(f"\nOpen this URL in your browser:\n\n  {url}\n")
    webbrowser.open(url)
    print("Paste the full redirect URL (or just the code= value):")
    pasted = input("> ").strip()

    if pasted.startswith("http"):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(pasted).query)
        if "error" in params:
            sys.exit(f"Authorization error: {params['error'][0]}")
        code = params.get("code", [None])[0]
        if not code:
            sys.exit("No 'code' parameter found in the pasted URL.")
    else:
        code = pasted

    return client.exchange_code(code).access_token


def main() -> None:
    args = _parse_args()
    load_dotenv(Path(args.env_file))
    client_id     = args.oauth_clientid or os.environ.get("RAVELRY_OAUTH_CLIENT_ID", "")
    client_secret = args.oauth_secret   or os.environ.get("RAVELRY_OAUTH_CLIENT_SECRET", "")
    redirect_uri  = os.environ.get("RAVELRY_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")

    if not client_id or not client_secret:
        sys.exit("OAuth credentials required — set in env file or pass --oauth-clientid/--oauth-secret")

    oauth = OAuthClient(client_id, client_secret, redirect_uri)
    matrix = SCOPE_MATRIX
    if args.scopes:
        matrix = [(n, s) for n, s in SCOPE_MATRIX if n in args.scopes]

    url = f"{BASE_URL}{args.path}"
    results: list[tuple[str, int]] = []

    for scope_name, scopes in matrix:
        token = _authorize(oauth, scopes, scope_name)
        r = httpx.get(url, headers={"Accept": "application/json",
                                    "Authorization": f"Bearer {token}"}, timeout=15)
        results.append((scope_name, r.status_code))
        print(f"  → {r.status_code}")

    print(f"\n\nResults for {args.path}")
    print("-" * 40)
    for scope_name, code in results:
        marker = "✓" if code == 200 else "✗"
        print(f"  {marker} {scope_name:<20} {code}")


if __name__ == "__main__":
    main()
