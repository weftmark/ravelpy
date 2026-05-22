# Installation

## Requirements

- Python 3.11 or later

## Install from PyPI

```bash
pip install ravelpy
```

## Optional extras

The `server` extra installs FastAPI and Uvicorn for running the included
Swagger UI proxy:

```bash
pip install "ravelpy[server]"
```

## Install from source

```bash
git clone https://github.com/weftmark/ravelpy.git
cd ravelpy
pip install -e ".[dev]"
```

## Verify

```python
import ravelpy
print(ravelpy.__version__)
```
