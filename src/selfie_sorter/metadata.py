"""
Module for stripping metadata from files using an external tool like exiftool.

This module provides the `MetadataCleaner` class, which can be used to strip
embedded metadata from files in a controlled manner. The class relies on a
configuration object that dictates whether metadata stripping is enabled and
specifies the path to the metadata stripping tool.

Classes:
    MetadataCleaner:
      Handles the metadata stripping functionality using an
      external tool.

"""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from .config import SortConfig


class MetadataCleaner:
    """
    Strip metadata from files using an external tool (default: exiftool).

    .. warning::
       This class **modifies files in place** when enabled. Ensure you keep backups.

    Attributes:
        cfg (SortConfig):
            Configuration controlling behavior. Must expose:

              - ``strip_metadata`` (bool):
                Whether stripping is enabled.

              - ``exiftool_cmd`` (str):
                Executable or path to exiftool.

    Methods:
        strip(path: Path) -> bool:
            Remove all embedded metadata from ``path``. Returns ``True`` on success.
    """

    def __init__(self, cfg: SortConfig):
        """
        Parameters:
            cfg:
                Configuration object providing ``strip_metadata`` and ``exiftool_cmd``.
        """
        self.cfg = cfg

    def _exiftool_path(self) -> Optional[str]:
        """Resolve the exiftool executable path or return ``None`` if unavailable."""
        # Allow absolute/relative paths in config; otherwise search PATH.
        if self.cfg.exiftool_cmd and Path(self.cfg.exiftool_cmd).exists():
            return str(self.cfg.exiftool_cmd)
        return shutil.which(self.cfg.exiftool_cmd or 'exiftool')

    def strip(self, path: Path) -> bool:
        """
        Remove all metadata in place using exiftool.

        .. warning::
           This operation cannot be undone. It writes to the original file.

        Parameters:
            path:
                Path to a file whose metadata should be stripped.

        Returns:
            bool:
                ``True`` if stripping succeeded or was skipped due to config; ``False`` otherwise.

        Raises:
            ValueError:
                If ``path`` does not exist or is not a file.
        """
        if not self.cfg.strip_metadata:
            return True  # explicitly “succeeds” when disabled

        if not path or not path.is_file():
            raise ValueError(f'Not a file: {path!s}')

        exe = self._exiftool_path()
        if not exe:
            # No executable available; caller can decide how to react
            return False

        try:
            # -all:all= wipes metadata; -overwrite_original avoids *_original files.
            subprocess.run(
                [exe, '-all:all=', '-overwrite_original', str(path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError:
            return False


__all__ = ['MetadataCleaner']
