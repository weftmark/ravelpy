"""Add missing `import pytest` to test files that use @pytest.mark.asyncio."""

import os
import re

tests_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")

for fname in sorted(os.listdir(tests_dir)):
    if not fname.endswith(".py") or fname == "conftest.py":
        continue
    path = os.path.join(tests_dir, fname)
    content = open(path, encoding="utf-8").read()
    if "@pytest.mark.asyncio" in content and "import pytest" not in content:
        # Insert import pytest after the module docstring
        new = re.sub(
            r'(^""".*?"""\n\n)',
            r'\1import pytest\n\n',
            content, count=1, flags=re.DOTALL
        )
        if new == content:
            new = "import pytest\n\n" + content
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        print(f"  fixed: {fname}")
