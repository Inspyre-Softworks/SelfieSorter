"""
Top-level package for selfie_sorter.

Note:
    We intentionally do not re-export submodule classes (e.g.,
    :class:`~selfie_sorter.config.SortConfig`) from the package root to avoid
    duplicate documentation targets in Sphinx.
"""

from __future__ import annotations
from importlib.metadata import version as _pkg_version, PackageNotFoundError

try:
    __version__ = _pkg_version('selfie_sorter')
except PackageNotFoundError:
    __version__ = '0.0.0'

__all__ = ['__version__']

