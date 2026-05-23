# Claude instructions for ravelpy

## Merging to main

Before every merge to main (or direct push), verify:

- **docs/resources.md** and **docs/quickstart.md** reflect any new or changed behaviour
- **Docstrings** on affected resource classes and methods are up to date
- **README.md** is updated if any user-facing API surface changed (new sub-client, removed method, new model field, etc.)

## Releases

When tagging a release and publishing to PyPI:

1. Bump `version` in `pyproject.toml` and `release` in `docs/conf.py` to the new version.
2. Create a **GitHub Release** for the tag. The release body must include:
   - A plain-English summary of what changed (new features, bug fixes, removals)
   - A link to every issue or PR that is part of the release (e.g. `Closes #12`)
3. Tag format: `vMAJOR.MINOR.PATCH` — pushing the tag triggers the PyPI publish workflow via GitHub Actions.
