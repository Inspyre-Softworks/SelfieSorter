"""
Module for configuration and management of image sorting with a focus on
classification and handling of explicit, suggestive, and safe content.

This module provides the :class:`~selfie_sorter.config.SortConfig` class, which defines the necessary
configuration settings for the SelfieSorter tool, specifically for :class:`~selfie_sorter.sorter.SelfieSorter` The configuration includes
options for specifying input and output directories, classification parameters,
metadata handling, and more.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from .constants import EXPLICIT_RULES, SUGGESTIVE_RULES


@dataclass
class SortConfig:
    """
    Configuration for SelfieSorter.

    Attributes:
        root_in (Path):
            Input directory scanned recursively for images.

        root_out (Path):
            Destination root. Created if missing.

        use_coarse_gate (bool):
            Use OpenNSFW2 coarse score gate if available.

        nsfw_threshold (float):
            Coarse score threshold for suggestive fallback.

        explicit_rules (Tuple[str, ...]):
            Labels counted as explicit.

        suggestive_rules (Tuple[str, ...]):
            Labels counted as suggestive.

        dup_hamming (int):
            Perceptual hash Hamming distance for near-dupe detection.

        strip_metadata (bool):
            If True, EXIF/GPS is removed in-place.

        write_sidecar (bool):
            If True, write JSON sidecar with decisions.

        move_safe (bool):
            If True, also relocate safe images to root_out/safe/.

        dir_explicit (str):
            Destination directory for explicit images.

        dir_suggestive (str):
            Destination directory for suggestive images.
    """
    root_in:          Path
    root_out:         Path
    use_coarse_gate:  bool            = True
    nsfw_threshold:   float           = 0.80
    explicit_rules:   Tuple[str, ...] = EXPLICIT_RULES
    suggestive_rules: Tuple[str, ...] = SUGGESTIVE_RULES
    dup_hamming:      int             = 5
    strip_metadata:   bool            = True
    write_sidecar:    bool            = True
    move_safe:        bool            = False
    write_censored:   bool            = False
    censor_style:     str             = 'pixelated'
    censor_strength:  int             = 12
    censor_label:     str             = 'CENSORED'
    censored_suffix:  str             = '_censored'
    censored_root:    Path            = Path('censored')
    show_progress:    bool            = True

    dir_explicit: str = 'explicit'
    dir_suggestive: str = 'suggestive'
    dir_safe: str = 'safe'
    dir_dupes: str = 'dupes'
    exiftool_cmd: str = 'exiftool'
    input_files: Optional[Tuple[Path, ...]] = None


__all__ = [
    'SortConfig',
]
