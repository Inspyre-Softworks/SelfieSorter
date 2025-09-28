"""Top-level package for :mod:`selfie_sorter`.

Historically, this module avoided re-exporting classes from submodules (such as
``SortConfig``) to keep the Sphinx documentation tree concise.  Downstream
consumers, however, relied on ``selfie_sorter.SortConfig`` being available from
the package root.  The import error observed in the tests stems from the fact
that :mod:`selfie_sorter.__init__` no longer exposed that symbol.

To retain compatibility while keeping documentation tidy, we re-export
``SortConfig`` explicitly in ``__all__``.  Sphinx respects ``__all__`` when
discovering public attributes, so this fix satisfies both requirements.
"""

from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version as _pkg_version

from .config import SortConfig

try:
    __version__ = _pkg_version('selfie_sorter')
except PackageNotFoundError:
    __version__ = '0.0.0'

__all__ = ['__version__', 'SortConfig']

