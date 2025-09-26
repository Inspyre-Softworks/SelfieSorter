"""
Provides functionality for sorting and organizing selfie images based on configured criteria.

This module imports and exposes the `SortConfig` class for configuration of sorting parameters
and the `SelfieSorter` class for processing and organizing selfies. It is designed to streamline
the management of large collections of selfies by automating the categorization process.

Exported Classes:
    - SortConfig:
        Defines configuration settings for the sorting process.

    - SelfieSorter:
        Implements the selfie sorting logic.

Constants:
    __all__ (list):
        Specifies the public API of the module.

    __version__ (str):
        Represents the version of the module.
"""
from .config import SortConfig
from .sorter import SelfieSorter

__all__ = ['SortConfig', 'SelfieSorter']
__version__ = '1.0.0-dev.1'
