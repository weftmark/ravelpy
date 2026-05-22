# ravelpy

Python client for the [Ravelry REST API](https://www.ravelry.com/api).

```{note}
**Built with Claude AI** — The requirements, architecture, and implementation of ravelpy were developed
collaboratively with [Claude](https://claude.ai) by Anthropic. Claude wrote the majority of the code in
this repository through an iterative conversation-driven process. This is disclosed prominently because
we believe AI development transparency matters.
```

Supports all three Ravelry credential tiers — read-only public access,
personal account keys, and OAuth 2.0 — with Pydantic models for every
response and built-in ETag caching.

```{toctree}
:maxdepth: 2
:caption: Getting started

installation
authentication
quickstart
```

```{toctree}
:maxdepth: 2
:caption: Reference

resources
autoapi/index
```

## Quick example

```python
from ravelpy import RavelryClient

client = RavelryClient(username="read-xxxxxxxxxxxx", api_key="your_api_key")

data, etag, raw = client.patterns.search(query="socks", weight="fingering")
for p in raw["patterns"]:
    print(p["name"])
```
