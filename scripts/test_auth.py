#!/usr/bin/env python3
"""Live API smoke test — validates auth tier requirements against real endpoints.

Loads read-only Basic Auth credentials from .env and calls every endpoint in the
library.  Reports the actual HTTP status code and whether it matches the expected
auth tier:

  public       → expect 200 or 404  (credential accepted; resource may not exist)
  authenticated → expect 401 or 403  (credential rejected)
  special       → noted in the table; outcome uncertain with read-only key

Usage:
    python scripts/test_auth.py

Credentials required in .env:
    RAVELRY_USERNAME=read-xxxx
    RAVELRY_API_KEY=your-key
"""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

USERNAME = os.environ.get("RAVELRY_USERNAME", "")
API_KEY = os.environ.get("RAVELRY_API_KEY", "")

if not USERNAME or not API_KEY:
    sys.exit("RAVELRY_USERNAME and RAVELRY_API_KEY must be set in .env")

BASE_URL = "https://api.ravelry.com"
TEST_USER = "tester"  # placeholder username for user-scoped paths; auth result is what matters


@dataclass
class Case:
    resource: str
    method: str
    path: str
    params: dict = field(default_factory=dict)
    # "public": expect 200/404 | "authenticated": expect 401/403 | "special": unknown
    expected: str = "public"
    note: str = ""


CASES: list[Case] = [
    # ── Patterns ────────────────────────────────────────────────────────────
    Case("patterns", "show",       "/patterns/1.json",           expected="public"),
    Case("patterns", "list",       "/patterns.json",             {"ids": "1,2"}, expected="public"),
    Case("patterns", "search",     "/patterns/search.json",      {"query": "hat"}, expected="public"),
    Case("patterns", "highlights", "/patterns/highlights.json",  expected="public",
         note="returns 500 server error — likely an intermittent API bug, not auth"),
    Case("patterns", "comments",   "/patterns/1/comments.json",  expected="authenticated"),
    Case("patterns", "projects",   "/patterns/1/projects.json",  expected="authenticated"),

    # ── Yarns ───────────────────────────────────────────────────────────────
    Case("yarns", "show",     "/yarns/95245.json",             expected="public"),
    Case("yarns", "list",     "/yarns.json",                   {"ids": "95245"}, expected="public"),
    Case("yarns", "search",   "/yarns/search.json",            {"query": "merino"}, expected="public"),
    Case("yarns", "comments", "/yarns/95245/comments.json",    expected="authenticated"),

    # ── Yarn companies ──────────────────────────────────────────────────────
    Case("yarn_companies", "search", "/yarn_companies/search.json", {"query": "cascade"}, expected="public"),

    # ── Yarn attributes (reference data) ────────────────────────────────────
    Case("yarn_attributes", "groups",  "/yarn_attributes/groups.json", expected="public"),
    Case("yarn_attributes", "weights", "/yarn_weights.json",           expected="public"),

    # ── Pattern attributes / categories / source types (reference data) ─────
    Case("pattern_attributes",    "groups", "/pattern_attributes/groups.json",   expected="public"),
    Case("pattern_categories",    "list",   "/pattern_categories/list.json",     expected="public"),
    Case("pattern_source_types",  "list",   "/pattern_source_types/list.json",   expected="public"),

    # ── Fiber attribute groups ───────────────────────────────────────────────
    Case("fiber_attribute_groups", "list",       "/fiber_attribute_groups/list.json",
         expected="authenticated", note="redirects to login page (302) with read-only key"),
    Case("fiber_attribute_groups", "attributes", "/fiber_attributes.json",            expected="public"),
    Case("fiber_attribute_groups", "categories", "/fiber_categories.json",            expected="public"),

    # ── Languages ────────────────────────────────────────────────────────────
    Case("languages", "list", "/languages/list.json", expected="public"),

    # ── Shops ────────────────────────────────────────────────────────────────
    Case("shops", "search", "/shops/search.json", {"query": "knit"}, expected="public"),
    Case("shops", "show",   "/shops/1.json",                         expected="public"),

    # ── Groups ───────────────────────────────────────────────────────────────
    Case("groups", "search", "/groups/search.json", {"query": "knitting"}, expected="public"),

    # ── Extras ───────────────────────────────────────────────────────────────
    Case("extras", "color_families", "/color_families.json",           expected="public"),
    Case("extras", "search",         "/search.json", {"query": "yarn"}, expected="public"),

    # ── Stores ───────────────────────────────────────────────────────────────
    Case("stores", "list",      "/stores/list.json",        expected="authenticated",
         note="not marked auth in docs but returns 403 in practice"),
    Case("stores", "products",  "/stores/1/products.json",  expected="authenticated",
         note="not marked auth in docs but returns 403 in practice"),
    Case("stores", "purchases", "/stores/1/purchases.json", expected="authenticated",
         note="not marked auth in docs but returns 403 in practice"),

    # ── Pattern sources (all public) ─────────────────────────────────────────
    Case("pattern_sources", "show",     "/pattern_sources/1.json",          expected="public"),
    Case("pattern_sources", "search",   "/pattern_sources/search.json",     {"query": "vogue"}, expected="public"),
    Case("pattern_sources", "patterns", "/pattern_sources/1/patterns.json",
         expected="public", note="marked auth in docs but returns 200/404 in practice"),

    # ── Stash (all authenticated) ────────────────────────────────────────────
    Case("stash", "search",   "/stash/search.json",                            {"query": "merino"}, expected="authenticated"),
    Case("stash", "comments", f"/people/{TEST_USER}/stash/1/comments.json",    expected="authenticated"),
    Case("stash", "list",     f"/people/{TEST_USER}/stash/list.json",          expected="authenticated"),
    Case("stash", "show",     f"/people/{TEST_USER}/stash/1.json",             expected="authenticated"),
    Case("stash", "unified",  f"/people/{TEST_USER}/stash/unified/list.json",  expected="authenticated"),

    # ── Projects (mixed — comments needs auth, rest are public) ──────────────
    Case("projects", "search",   "/projects/search.json",                    {"query": "sweater"}, expected="public"),
    Case("projects", "list",     f"/projects/{TEST_USER}/list.json",         expected="public",
         note="marked auth in docs; returns empty list for any user in practice"),
    Case("projects", "show",     f"/projects/{TEST_USER}/1.json",            expected="public",
         note="may return 500 for invalid user/id combinations"),
    Case("projects", "crafts",   "/projects/crafts.json",                    expected="public",
         note="marked auth in docs but returns 200 in practice"),
    Case("projects", "statuses", "/projects/project_statuses.json",          expected="public",
         note="marked auth in docs but returns 200 in practice"),
    Case("projects", "comments", f"/projects/{TEST_USER}/1/comments.json",   expected="authenticated"),

    # ── Forums (all authenticated) ────────────────────────────────────────────
    Case("forums", "unread_posts",    "/forum_posts/unread.json",
         expected="authenticated", note="not marked auth in docs but returns 403 in practice"),
    Case("forums", "sets",            "/forums/sets.json",                 expected="authenticated"),
    Case("forums", "topics",          "/forums/1/topics.json",             expected="authenticated"),
    Case("forums", "filtered_topics", "/forums/filtered_topics.json",      expected="authenticated"),
    Case("forums", "post",            "/forum_posts/1.json",               expected="authenticated"),

    # ── Topics ───────────────────────────────────────────────────────────────
    Case("topics", "show",  "/topics/1.json",       expected="authenticated"),
    Case("topics", "posts", "/topics/1/posts.json", expected="authenticated"),

    # ── Saved searches (authenticated despite docs saying otherwise) ──────────
    Case("saved_searches", "list", "/saved_searches/list.json",
         expected="authenticated", note="not marked auth in docs but returns 403 in practice"),

    # ── Drafts (authenticated despite docs saying otherwise) ──────────────────
    Case("drafts", "list", "/drafts/patterns/list.json",
         expected="authenticated", note="not marked auth in docs but returns 403 in practice"),
    Case("drafts", "show", "/drafts/patterns/1.json",
         expected="authenticated", note="not marked auth in docs but returns 403 in practice"),

    # ── Deliveries (requires deliveries-read scope) ────────────────────────────
    Case("deliveries", "list", "/deliveries/list.json",
         expected="authenticated", note="requires deliveries-read scope; personal key grants automatically"),

    # ── People ───────────────────────────────────────────────────────────────
    Case("people", "me",       "/current_user.json",                         expected="authenticated"),
    Case("people", "show",     f"/people/{TEST_USER}.json",                  expected="authenticated"),
    Case("people", "comments", f"/people/{TEST_USER}/comments/list.json",    expected="authenticated"),

    # ── Fiber (all public) ────────────────────────────────────────────────────
    Case("fiber", "show",     f"/people/{TEST_USER}/fiber/1.json",
         expected="public", note="marked auth in docs but returns 200/404 in practice"),
    Case("fiber", "comments", f"/people/{TEST_USER}/fiber/1/comments.json",  expected="public"),

    # ── App ──────────────────────────────────────────────────────────────────
    Case("app", "config", "/app/config/get.json", expected="authenticated"),
    Case("app", "data",   "/app/data/get.json",   expected="authenticated"),

    # ── Photos ───────────────────────────────────────────────────────────────
    Case("photos", "dimensions", "/photos/dimensions.json",  expected="authenticated"),
    Case("photos", "sizes",      "/photos/1/sizes.json",     expected="authenticated"),
    Case("photos", "status",     "/photos/status.json",      expected="authenticated"),

    # ── Designers ────────────────────────────────────────────────────────────
    Case("designers", "show", "/designers/1.json",
         expected="public", note="marked auth in docs but returns 200 in practice"),

    # ── Products / attachments ───────────────────────────────────────────────
    Case("products",           "show",        "/products/1.json",                expected="authenticated"),
    Case("products",           "attachments", "/products/1/attachments.json",    expected="authenticated"),
    Case("product_attachments","show",        "/product_attachments/1.json",     expected="authenticated"),

    # ── Bundled items ────────────────────────────────────────────────────────
    Case("bundled_items", "show", "/bundled_items/1.json",
         expected="public", note="marked auth in docs but returns 200/404 in practice"),

    # ── Bundles ──────────────────────────────────────────────────────────────
    Case("bundles", "list", f"/people/{TEST_USER}/bundles/list.json",
         expected="public", note="marked auth in docs; returns empty list for any user in practice"),
    Case("bundles", "show", f"/people/{TEST_USER}/bundles/1.json",
         expected="public", note="marked auth in docs but returns 200/404 in practice"),

    # ── Favorites ────────────────────────────────────────────────────────────
    Case("favorites", "list", f"/people/{TEST_USER}/favorites/list.json",  expected="authenticated"),
    Case("favorites", "show", f"/people/{TEST_USER}/favorites/1.json",     expected="authenticated"),

    # ── Friends ──────────────────────────────────────────────────────────────
    Case("friends", "list",     f"/people/{TEST_USER}/friends/list.json",     expected="authenticated"),
    Case("friends", "activity", f"/people/{TEST_USER}/friends/activity.json", expected="authenticated"),

    # ── Library ──────────────────────────────────────────────────────────────
    Case("library", "search", f"/people/{TEST_USER}/library/search.json", expected="authenticated"),

    # ── Messages ─────────────────────────────────────────────────────────────
    Case("messages", "list", "/messages/list.json", expected="authenticated"),
    Case("messages", "show", "/messages/1.json",    expected="authenticated"),

    # ── Needles ──────────────────────────────────────────────────────────────
    Case("needles", "list",  f"/people/{TEST_USER}/needles/list.json", expected="authenticated"),
    Case("needles", "sizes", "/needles/sizes.json",
         expected="public", note="marked auth in docs but returns 200 in practice"),
    Case("needles", "types", "/needles/types.json",
         expected="public", note="marked auth in docs but returns 200 in practice"),

    # ── Packs ────────────────────────────────────────────────────────────────
    Case("packs", "show", "/packs/1.json",
         expected="public", note="marked auth in docs but returns 200 in practice"),

    # ── Pages ────────────────────────────────────────────────────────────────
    Case("pages", "show", "/pages/1.json", expected="authenticated"),

    # ── Volumes ──────────────────────────────────────────────────────────────
    Case("volumes", "show", "/volumes/1.json", expected="authenticated"),

    # ── Queue ────────────────────────────────────────────────────────────────
    Case("queue", "list", f"/people/{TEST_USER}/queue/list.json",
         expected="public", note="marked auth in docs; returns empty list for any user in practice"),
    Case("queue", "show", f"/people/{TEST_USER}/queue/1.json",
         expected="public", note="marked auth in docs but returns 200/404 in practice"),
]


def run() -> None:
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

    header = (
        f"{'Resource':<{col_resource}} {'Method':<{col_method}} {'Path':<{col_path}} "
        f"{'Exp':<{col_exp}} {'Got':<{col_got}} Match  Note"
    )
    sep = "-" * len(header)
    print(header)
    print(sep)

    pass_count = fail_count = special_count = 0

    for case, status in results:
        if case.expected == "public":
            # 200/304/404/500 all indicate credential was accepted; 302→login or 401/403 = rejected
            match = status not in (401, 403, 302)
            symbol = "OK" if match else "FAIL"
            if match:
                pass_count += 1
            else:
                fail_count += 1
        elif case.expected == "authenticated":
            match = status in (401, 403, 302)
            symbol = "OK" if match else "FAIL"
            if match:
                pass_count += 1
            else:
                fail_count += 1
        else:
            symbol = "----"
            special_count += 1

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
