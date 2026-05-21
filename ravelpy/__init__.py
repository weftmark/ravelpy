from importlib.metadata import PackageNotFoundError, version

from .client import RavelryClient
from .exceptions import RavelryAPIError

try:
    __version__ = version("ravelpy")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["RavelryClient", "RavelryAPIError", "__version__"]
