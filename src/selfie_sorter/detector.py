"""
NudeNet body-part detector module.

This module provides tools for detecting sensitive or explicit content in
images using NudeNet. It exports a wrapper class for using the NudeDetector
and a flag indicating the availability of the NudeNet library. The NudeNet
library is optional, and its presence determines the functionality.

Exports:
  - FineDetector (class):
      A class that enables detecting nudity or explicit content
      in images using the NudeNet detector.

  - HAS_NUDENET (bool):
        A boolean flag indicating if the NudeNet library is available.
"""
from __future__ import annotations
from typing import Dict, List, Optional


try:
    from nudenet import NudeDetector
    HAS_NUDENET = True
except Exception:
    HAS_NUDENET = False


class FineDetector:
    """
    Detects inappropriate or sensitive content in images.

    The `FineDetector` class is designed to utilize a pre-configured model to
    analyze images for potentially inappropriate content. The model used depends
    on the availability of the `NudeDetector`. If the model is not available,
    detection functionality will be disabled.

    Attributes:
        model (Optional[NudeDetector]):
          The detection model instance used for
          processing images. Set to `None` if `NudeDetector` is not available.
    """
    def __init__(self):
        self.model = NudeDetector() if HAS_NUDENET else None

    def detect(self, path) -> List[Dict]:
        """
        Detect objects in the given file path using the preloaded model.

        This method utilizes a preloaded model to perform object detection on the
        file specified by the input path. If the model is not initialized, or an
        error occurs during detection, an empty list is returned.

        Parameters:
            path (str):
                The file path to the input data for object detection.

        Returns:
            List[Dict]:
              A list of dictionaries representing detected objects. Each
              dictionary contains details of the detected objects. If no objects are
              detected or model is unavailable, an empty list is returned.
        """
        if not self.model:
            return []
        try:
            out = self.model.detect(str(path))
            return out or []
        except Exception:
            return []


__all__ = [
    'FineDetector',
    'HAS_NUDENET',
]
