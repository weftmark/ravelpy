#!/usr/bin/env python3
"""Display the authenticated user's stash contents.

Fetches the username from /current_user.json, then paginates through all stash
entries and prints a formatted table grouped by stash status.

Usage:
    python scripts/my_stash.py
    python scripts/my_stash.py --env-file .env.user.readwrite
    python scripts/my_stash.py --api-user your_key --api-key your_secret
    python scripts/my_stash.py --sort weight
    python scripts/my_stash.py --status "in use"
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Display your Ravelry stash")
    p.add_argument(
        "--env-file",
        metavar="FILE",
        default=str(ROOT / ".env.user.readwrite"),
        help="Env file to load credentials from (default: .env.user.readwrite)",
    )
    p.add_argument("--api-user", metavar="USERNAME", help="Ravelry username (overrides env file)")
    p.add_argument("--api-key",  metavar="KEY",      help="Ravelry API key (overrides env file)")
    p.add_argument(
        "--sort",
        choices=["name", "weight", "status", "yarn", "updated"],
        default="status",
        help="Sort order (default: status)",
    )
    p.add_argument(
        "--status",
        metavar="STATUS",
        help="Filter by stash status (e.g. 'stashed', 'in use', 'used up')",
    )
    p.add_argument(
        "--page-size",
        type=int,
        default=100,
        metavar="N",
        help="Entries per API page (default: 100)",
    )
    return p.parse_args()


args = _parse_args()
load_dotenv(Path(args.env_file))

api_user = args.api_user or os.environ.get("RAVELRY_USERNAME", "")
api_key  = args.api_key  or os.environ.get("RAVELRY_API_KEY",  "")

if not api_user or not api_key:
    sys.exit(
        f"Credentials required: set RAVELRY_USERNAME/RAVELRY_API_KEY in {args.env_file} "
        "or pass --api-user/--api-key"
    )

from ravelpy import RavelryClient

client = RavelryClient(api_user, api_key)


# ---------------------------------------------------------------------------
# Resolve the authenticated user's Ravelry username
# ---------------------------------------------------------------------------

user_result, _, _ = client.people.me()
if user_result is None:
    sys.exit("Could not fetch current user — check your credentials.")

username = user_result.user.username
if not username:
    sys.exit("Current user response did not include a username.")

print(f"Fetching stash for: {username}")


# ---------------------------------------------------------------------------
# Paginate through all stash entries
# ---------------------------------------------------------------------------

from ravelpy.models import Stash
from ravelpy.responses import StashListResponse

all_entries: list[Stash] = []
page = 1

while True:
    result, _, raw = client.stash.list(username=username, page=page, page_size=args.page_size)

    if isinstance(result, StashListResponse):
        entries = result.stash or []
    else:
        # Pydantic validation failed; fall back to raw dict
        raw_entries = (raw or {}).get("stash", [])
        entries = [Stash.model_validate(e) for e in raw_entries]

    all_entries.extend(entries)

    paginator = (raw or {}).get("paginator", {})
    page_count = paginator.get("page_count", 1)
    if page >= page_count:
        break
    page += 1

print(f"Total stash entries: {len(all_entries)}")


# ---------------------------------------------------------------------------
# Optional status filter
# ---------------------------------------------------------------------------

if args.status:
    filter_lower = args.status.lower()
    all_entries = [e for e in all_entries if (e.stash_status and e.stash_status.name or "").lower() == filter_lower]
    print(f"Filtered to '{args.status}': {len(all_entries)} entries")


# ---------------------------------------------------------------------------
# Sort
# ---------------------------------------------------------------------------

def _sort_key(e: Stash):
    if args.sort == "name":
        return (e.name or "").lower()
    if args.sort == "weight":
        return (e.yarn_weight_name or "").lower()
    if args.sort == "status":
        return (e.stash_status.name if e.stash_status else "").lower()
    if args.sort == "yarn":
        yarn_name = (e.yarn.name if e.yarn else "") or ""
        return yarn_name.lower()
    if args.sort == "updated":
        return e.updated_at or ""
    return ""

all_entries.sort(key=_sort_key)


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

if not all_entries:
    print("No stash entries found.")
    sys.exit(0)

print()

COL_YARN     = 40
COL_COLORWAY = 24
COL_COMPANY  = 26
COL_WEIGHT   = 14
COL_STATUS   = 10
COL_LOC      = 18

header = (
    f"{'Yarn':<{COL_YARN}} {'Colorway':<{COL_COLORWAY}} {'Company':<{COL_COMPANY}} "
    f"{'Weight':<{COL_WEIGHT}} {'Status':<{COL_STATUS}} {'Location':<{COL_LOC}} Tags"
)
sep = "-" * len(header)
print(header)
print(sep)

current_group = None

for e in all_entries:
    # Group header when sorting by status or weight
    if args.sort in ("status", "weight"):
        if args.sort == "status":
            group = (e.stash_status.name if e.stash_status else "Unknown status")
        else:
            group = (e.yarn_weight_name or "Unknown weight")

        if group != current_group:
            if current_group is not None:
                print()
            print(f"  [{group}]")
            current_group = group

    # Prefer yarn name; fall back to stash entry name
    yarn_name = (e.yarn.name if e.yarn else "") or (e.name or "(unnamed)")
    company   = (e.yarn.yarn_company_name if e.yarn else "") or ""
    colorway  = e.colorway_name or ""
    weight    = e.yarn_weight_name or ""
    status    = (e.stash_status.name if e.stash_status else "")
    loc       = e.location or ""
    tags      = ", ".join(e.tag_names) if e.tag_names else ""

    print(
        f"{yarn_name[:COL_YARN]:<{COL_YARN}} {colorway[:COL_COLORWAY]:<{COL_COLORWAY}} "
        f"{company[:COL_COMPANY]:<{COL_COMPANY}} {weight[:COL_WEIGHT]:<{COL_WEIGHT}} "
        f"{status[:COL_STATUS]:<{COL_STATUS}} {loc[:COL_LOC]:<{COL_LOC}} {tags}"
    )

print(sep)
print(f"{len(all_entries)} entries displayed.")
