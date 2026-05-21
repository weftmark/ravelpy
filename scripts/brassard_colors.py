"""
Brassard yarn exploration script.

  python scripts/brassard_colors.py
  python scripts/brassard_colors.py --env-file .env.user.read
  python scripts/brassard_colors.py --api-user read-xxxx --api-key yourkey

Loads credentials from .env.developer.readonly in the repo root (or the file /
credentials passed via flags), then:
  1. Searches yarn companies for "brassard"
  2. Searches yarns for "brassard 8/2 unmercerized cotton"
  3. Fetches full yarn detail + colorways for the first match
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from ravelpy import RavelryClient

ROOT = Path(__file__).parent.parent


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Brassard yarn exploration")
    p.add_argument(
        "--env-file",
        metavar="FILE",
        default=str(ROOT / ".env.developer.readonly"),
        help="Env file to load credentials from (default: .env.developer.readonly)",
    )
    p.add_argument("--api-user", metavar="USERNAME", help="Ravelry username (overrides env file)")
    p.add_argument("--api-key",  metavar="KEY",      help="Ravelry API key (overrides env file)")
    return p.parse_args()


args = _parse_args()
load_dotenv(Path(args.env_file))

username = args.api_user or os.environ.get("RAVELRY_USERNAME", "")
api_key  = args.api_key  or os.environ.get("RAVELRY_API_KEY",  "")

if not username or not api_key:
    sys.exit(f"Credentials required: set RAVELRY_USERNAME/RAVELRY_API_KEY in {args.env_file} or pass --api-user/--api-key")

client = RavelryClient(username, api_key)


# ---------------------------------------------------------------------------
# Request / response logging via httpx event hooks
# ---------------------------------------------------------------------------

def _on_request(request):
    print(f"\n{'-' * 64}")
    print(f"  REQUEST   {request.method} {request.url}")

def _on_response(response):
    response.read()
    elapsed = response.elapsed.total_seconds() if response.elapsed else 0
    print(f"  RESPONSE  {response.status_code}  {elapsed:.3f}s  {len(response.content):,} bytes")

session = client.yarn_companies._session
session.event_hooks["request"].append(_on_request)
session.event_hooks["response"].append(_on_response)


def _print_raw(data: dict) -> None:
    for key, val in data.items():
        if isinstance(val, list):
            print(f"  raw [{key}]: list of {len(val)}")
        elif isinstance(val, dict):
            print(f"  raw [{key}]: dict  keys={list(val.keys())[:6]}")
        else:
            print(f"  raw [{key}]: {val!r}")


# ---------------------------------------------------------------------------
# 1. Yarn company search
# ---------------------------------------------------------------------------

COMPANY_QUERY = "brassard"
print(f"\n{'=' * 64}")
print(f"  STEP 1 -- yarn company search: {COMPANY_QUERY!r}")

_parsed, _, raw = client.yarn_companies.search(query=COMPANY_QUERY)
_print_raw(raw)

companies = raw.get("yarn_companies", [])
print(f"\n  {len(companies)} company result(s):")
for co in companies:
    print(
        f"    [{co['id']:>6}]  {co['name']:<35}"
        f"  yarns={co.get('yarns_count', '-'):>5}"
        f"  permalink={co.get('permalink')}"
    )


# ---------------------------------------------------------------------------
# 2. Yarn search
# ---------------------------------------------------------------------------

YARN_QUERY = "brassard 8/2 unmercerized cotton"
print(f"\n{'=' * 64}")
print(f"  STEP 2 -- yarn search: {YARN_QUERY!r}")

_parsed, _, raw = client.yarns.search(query=YARN_QUERY)
_print_raw(raw)

yarns = raw.get("yarns", [])
pager = raw.get("paginator", {})
print(
    f"\n  {pager.get('results', len(yarns))} total result(s)"
    f"  (page {pager.get('page')}/{pager.get('page_count')},"
    f" showing {len(yarns)})"
)
for y in yarns:
    weight = (y.get("yarn_weight") or {}).get("name", "-")
    print(
        f"    [{y['id']:>7}]  {y['name']:<45}"
        f"  {y.get('yarn_company_name', ''):<25}"
        f"  weight={weight}"
    )


# ---------------------------------------------------------------------------
# 3. Full detail + colorways for the first match
# ---------------------------------------------------------------------------

if not yarns:
    print("\n  No yarns found.")
else:
    first   = yarns[0]
    yarn_id = first["id"]

    print(f"\n{'=' * 64}")
    print(f"  STEP 3 -- yarn detail + colorways: [{yarn_id}] {first['name']}")

    _parsed, _, raw = client.yarns.show(yarn_id=yarn_id, include="colorways")
    _print_raw(raw)

    yarn      = raw.get("yarn", {})
    colorways = raw.get("colorways", [])

    # Fiber content
    fibers = yarn.get("yarn_fibers", [])
    if fibers:
        print(f"\n  Fiber content:")
        for f in fibers:
            ft  = f.get("fiber_type", {})
            print(f"    {f.get('percentage', '?')}%  {ft.get('name', '?')}")

    # Colors
    print(f"\n  {len(colorways)} color(s) available:\n")
    print(f"    {'Code':<8}  {'Name':<40}  {'Stashes':>8}  {'Projects':>9}")
    print(f"    {'-'*8}  {'-'*40}  {'-'*8}  {'-'*9}")
    for cw in sorted(colorways, key=lambda c: (c.get("name") or "").lower()):
        print(
            f"    {(cw.get('code') or ''):<8}"
            f"  {(cw.get('name') or '(unnamed)'):<40}"
            f"  {cw.get('stashes_count', 0):>8}"
            f"  {cw.get('projects_count', 0):>9}"
        )
