#!/usr/bin/env python3
"""Test each OAuth scope in isolation and map which endpoints each scope unlocks.

Iterates through SCOPE_MATRIX (baseline + one scope per run), authorizes via
the manual browser flow for each combination, hits every authenticated endpoint,
and records HTTP status codes.  After all runs prints a comparison matrix and a
delta summary showing exactly which endpoints each scope changes vs baseline.

Results are saved to .oauth_scope_results.json after each authorization so you
can resume an interrupted run or reprint the report without re-authorizing.

Usage:
    # Full run — authorizes once per scope (8 browser flows total)
    python scripts/oauth_scope_test.py --env-file .env.oauth.personal

    # Print report from a previous run without re-authorizing
    python scripts/oauth_scope_test.py --report-only

    # Test a subset of scopes (skip ones already in the JSON or not needed)
    python scripts/oauth_scope_test.py --scopes baseline forum-write message-write
"""

import argparse
import json
import os
import sys
import urllib.parse
import webbrowser
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT       = Path(__file__).parent.parent
RESULTS_PATH = ROOT / ".oauth_scope_results.json"

sys.path.insert(0, str(Path(__file__).parent))
from _test_cases import AUTH_CASES, BASE_URL, Case  # noqa: E402

# Scopes to test — each is run as  offline + the named scope.
# "baseline" = offline only (no extra scope).
SCOPE_MATRIX: list[tuple[str, list[str]]] = [
    ("baseline",           ["offline"]),
    ("forum-write",        ["offline", "forum-write"]),
    ("message-write",      ["offline", "message-write"]),
    ("patternstore-read",  ["offline", "patternstore-read"]),
    ("deliveries-read",    ["offline", "deliveries-read"]),
    ("library-pdf",        ["offline", "library-pdf"]),
    # NOTE: profile-only and carts-only are mutually exclusive with all other scopes.
    # Combining them with "offline" (or any other scope) causes Ravelry to reject
    # the authorization with "Unexpected scope error". They are standalone-only tokens
    # and cannot be tested in this composite flow.
]

ALL_SCOPE_NAMES = [name for name, _ in SCOPE_MATRIX]


# ── Argument parsing ─────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OAuth scope permission matrix test")
    p.add_argument(
        "--env-file",
        metavar="FILE",
        default=str(ROOT / ".env.oauth.personal"),
        help="Env file with OAuth client credentials (default: .env.oauth.personal)",
    )
    p.add_argument("--oauth-clientid", metavar="ID",     help="OAuth client ID (overrides env file)")
    p.add_argument("--oauth-secret",   metavar="SECRET", help="OAuth client secret (overrides env file)")
    p.add_argument(
        "--report-only",
        action="store_true",
        help="Skip authorization; print the report from an existing .oauth_scope_results.json",
    )
    p.add_argument(
        "--scopes",
        nargs="+",
        metavar="SCOPE",
        choices=ALL_SCOPE_NAMES,
        help=f"Only test these scope names (choices: {', '.join(ALL_SCOPE_NAMES)})",
    )
    p.add_argument(
        "--results-file",
        metavar="FILE",
        default=str(RESULTS_PATH),
        help=f"Where to save/load results JSON (default: {RESULTS_PATH})",
    )
    return p.parse_args()


args = _parse_args()
results_path = Path(args.results_file)

if not args.report_only:
    load_dotenv(Path(args.env_file))
    CLIENT_ID     = args.oauth_clientid or os.environ.get("RAVELRY_OAUTH_CLIENT_ID", "")
    CLIENT_SECRET = args.oauth_secret   or os.environ.get("RAVELRY_OAUTH_CLIENT_SECRET", "")
    REDIRECT_URI  = os.environ.get("RAVELRY_OAUTH_REDIRECT_URI", "http://localhost:8080/callback")

    if not CLIENT_ID or not CLIENT_SECRET:
        sys.exit(
            f"OAuth credentials required: set RAVELRY_OAUTH_CLIENT_ID/RAVELRY_OAUTH_CLIENT_SECRET "
            f"in {args.env_file} or pass --oauth-clientid/--oauth-secret"
        )

from ravelpy.oauth import OAuthClient  # noqa: E402


# ── Helpers ──────────────────────────────────────────────────────────────────

def _authorize(client: OAuthClient, scopes: list[str], scope_name: str) -> str:
    """Run the manual browser flow and return an access token."""
    url, _ = client.auth_url(scopes)
    print(f"\n{'=' * 70}")
    print(f"  Authorizing scope set: {scope_name!r}  ({' '.join(scopes)})")
    print(f"{'=' * 70}")
    print(f"\nOpen this URL in your browser:\n\n  {url}\n")
    webbrowser.open(url)
    print("After clicking Allow, copy the full redirect URL from the address bar")
    print("and paste it here (or just the code= value):")
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

    tokens = client.exchange_code(code)
    return tokens.access_token


def _run_cases(token: str, cases: list[Case]) -> dict[str, int]:
    """Hit every case with a Bearer token and return {label: status_code}."""
    session = httpx.Client(
        headers={"Accept": "application/json", "Authorization": f"Bearer {token}"},
        timeout=15.0,
    )
    results: dict[str, int] = {}
    for case in cases:
        clean = {k: v for k, v in case.params.items() if v is not None}
        r = session.get(f"{BASE_URL}{case.path}", params=clean)
        results[case.label] = r.status_code
        print(f"  {case.label:<40} {r.status_code}")
    session.close()
    return results


# ── Load existing results ─────────────────────────────────────────────────────

all_results: dict[str, dict[str, int]] = {}
if results_path.exists():
    all_results = json.loads(results_path.read_text())
    print(f"Loaded existing results from {results_path}  "
          f"({', '.join(all_results)} already done)")


# ── Run authorizations ────────────────────────────────────────────────────────

if not args.report_only:
    scope_matrix = SCOPE_MATRIX
    if args.scopes:
        scope_matrix = [(n, s) for n, s in SCOPE_MATRIX if n in args.scopes]

    pending = [(n, s) for n, s in scope_matrix if n not in all_results]
    if not pending:
        print("All requested scopes already have results. Use --report-only to print.")
    else:
        oauth = OAuthClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
        total = len(pending)
        for i, (scope_name, scopes) in enumerate(pending, 1):
            print(f"\n[{i}/{total}] Scope: {scope_name}")
            token = _authorize(oauth, scopes, scope_name)
            print(f"\nRunning {len(AUTH_CASES)} endpoint tests...")
            all_results[scope_name] = _run_cases(token, AUTH_CASES)
            results_path.write_text(json.dumps(all_results, indent=2))
            print(f"Saved to {results_path}")

    if not all_results:
        sys.exit("No results to report.")


# ── Report ────────────────────────────────────────────────────────────────────

# Only report on scopes that were actually run
ordered_scopes = [n for n, _ in SCOPE_MATRIX if n in all_results]
if not ordered_scopes:
    sys.exit(f"No results found in {results_path}. Run without --report-only first.")

labels = [c.label for c in AUTH_CASES]

COL_LABEL = 36
COL_SCOPE = 9  # wide enough for status codes with padding

print(f"\n\n{'=' * 70}")
print("  SCOPE PERMISSION MATRIX")
print(f"  Rows: authenticated endpoints   Columns: OAuth scope tested")
print(f"  Values: HTTP status code")
print(f"{'=' * 70}\n")

# Header
header = f"{'Endpoint':<{COL_LABEL}}"
for name in ordered_scopes:
    header += f" {name[:COL_SCOPE - 1]:>{COL_SCOPE - 1}}"
sep = "-" * len(header)
print(header)
print(sep)

for label in labels:
    row = f"{label:<{COL_LABEL}}"
    for scope_name in ordered_scopes:
        code = all_results[scope_name].get(label, "???")
        row += f" {str(code):>{COL_SCOPE - 1}}"
    print(row)

print(sep)

# Delta summary — what changed vs baseline
if "baseline" in all_results:
    baseline = all_results["baseline"]
    print("\n\nDELTA vs baseline (offline only):")
    print("-" * 50)
    any_delta = False
    for scope_name in ordered_scopes:
        if scope_name == "baseline":
            continue
        scope_results = all_results[scope_name]
        changes: list[str] = []
        for label in labels:
            b = baseline.get(label)
            s = scope_results.get(label)
            if b != s:
                changes.append(f"    {label}: {b} -> {s}")
        if changes:
            any_delta = True
            print(f"\n  {scope_name}:")
            for c in changes:
                print(c)
        else:
            print(f"\n  {scope_name}: no changes vs baseline")

    if not any_delta:
        print("  (no scope changed any endpoint result vs baseline)")
else:
    print("\n(Run 'baseline' scope to enable delta comparison)")
