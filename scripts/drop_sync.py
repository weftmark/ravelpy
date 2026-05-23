"""One-shot script to drop sync classes from all resource and test files."""

import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── Resource files ─────────────────────────────────────────────────────────

def transform_resource(content: str, filename: str) -> str:
    # Find where the Async class block begins
    match = re.search(r'\n\nclass Async\w+\(AsyncResource\):', content)
    if not match:
        print(f"  [skip] no Async class found in {filename}")
        return content

    # Keep module docstring + imports + sync class body only
    sync_part = content[:match.start()]

    # Fix imports
    for old, new in [
        ("from .base import ApiResult, AsyncResource, Resource", "from .base import ApiResult, Resource"),
        ("from .base import AsyncResource, Resource", "from .base import Resource"),
    ]:
        sync_part = sync_part.replace(old, new)

    # Make every top-level method (4-space indent) async
    sync_part = re.sub(r'^    def ', '    async def ', sync_part, flags=re.MULTILINE)

    # Make _get calls awaited
    sync_part = sync_part.replace('return self._get(', 'return await self._get(')

    return sync_part


def process_resources():
    resources_dir = os.path.join(REPO, "ravelpy", "resources")
    skip = {"__init__.py", "base.py"}

    for fname in sorted(os.listdir(resources_dir)):
        if not fname.endswith(".py") or fname in skip:
            continue
        path = os.path.join(resources_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        transformed = transform_resource(original, fname)
        if transformed != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(transformed)
            print(f"  [resource] {fname}")


# ── Test files ─────────────────────────────────────────────────────────────

# Tests that are pure model tests (no client calls) — leave them sync
MODEL_ONLY_TESTS = {"test_pack_model.py", "test_colorway_model.py"}

# This file will be rewritten entirely below
SKIP_TESTS = {"test_async_client_core.py"}


def transform_test(content: str, filename: str) -> str:
    lines = content.splitlines(keepends=True)
    result = []
    needs_asyncio_import = False
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if this is a test function that takes `client`
        m = re.match(r'^(def )(test_\w+\(.*\bclient\b.*\):)', line)
        if m:
            result.append('@pytest.mark.asyncio\n')
            result.append(f'async def {m.group(2)}\n')
            needs_asyncio_import = True
        else:
            result.append(line)
        i += 1

    content = ''.join(result)

    # Add `await` before client.xxx.xxx( patterns (not already awaited)
    def add_await(m):
        start = m.start()
        preceding = content[max(0, start - 6):start]
        return m.group(0) if 'await ' in preceding else f'await {m.group(0)}'

    content = re.sub(r'\bclient\.\w+\.\w+\(', add_await, content)

    # Ensure pytest is imported (already is in every test file)
    return content


def process_tests():
    tests_dir = os.path.join(REPO, "tests")
    for fname in sorted(os.listdir(tests_dir)):
        if not fname.endswith(".py") or fname in SKIP_TESTS | MODEL_ONLY_TESTS | {"conftest.py"}:
            continue
        path = os.path.join(tests_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        transformed = transform_test(original, fname)
        if transformed != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(transformed)
            print(f"  [test]     {fname}")


if __name__ == "__main__":
    print("Transforming resource files...")
    process_resources()
    print("Transforming test files...")
    process_tests()
    print("Done.")
