"""
Defines a class for an optional OpenNSFW2-based coarse probability gate.

This module provides functionality to determine a coarse probability score for
images by integrating with the OpenNSFW2 library. The scoring relies on the
presence of the OpenNSFW2 dependency and the configuration to enable the gate.
The score is used to assess the suitability or classification of images.

Classes:
    CoarseGate:
        Represents the coarse probability gate leveraging OpenNSFW2.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional

from .config import SortConfig


try:
    from opennsfw2 import predict_image
    HAS_OPENNSFW2 = True
except Exception:
    HAS_OPENNSFW2 = False


class CoarseGate:
    """
    Represents a coarse gate mechanism to process and filter elements based on a score.

    The class is designed to leverage the `OPENNSFW2` library to evaluate an image
    against a model and return a score (if enabled). It ensures that evaluations
    are not performed when it is not properly configured or the relevant library is
    unavailable.

    This is determined by:
        - The presence of the `opennsfw2` library;
        - The configuration to enable the gate (`SortConfig.use_coarse_gate`, `--no-coarse`).

    Attributes:
        enabled (bool):
            Indicates whether the coarse gate feature is enabled.
    """
    def __init__(self, cfg: SortConfig):
        """
        Initializes the instance of the class.

        Args:
            cfg (:class:`~selfie_sorter.config.SortConfig`):
                The configuration object for the sorter.
        """
        self.enabled = HAS_OPENNSFW2 and cfg.use_coarse_gate

    def score(self, path: Path) -> Optional[float]:
        if not self.enabled:
            return None
        try:
            return float(predict_image(str(path)))
        except Exception:
            return None
