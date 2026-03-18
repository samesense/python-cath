# mypy: disable-error-code="attr-defined"
"""Cat files w/ headers"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
