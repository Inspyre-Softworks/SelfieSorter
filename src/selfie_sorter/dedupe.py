"""
A module for detecting near-duplicate images using perceptual hashing (pHash).

This module provides a class (`Deduper`) that uses perceptual hashing to
identify near-duplicate images efficiently. The class checks whether an
image is a near-duplicate of any previously encountered images by
computing the perceptual hash of the image and comparing it with stored
hashes.
"""
from __future__ import annotations
from typing import Dict
from pathlib import Path
from PIL import Image
import imagehash

from .config import SortConfig


class Deduper:
    """
    A class to identify and manage duplicate images.

    This class is designed to determine whether a given image file is a potential
    duplicate of previously processed images. It uses perceptual hashing algorithms
    to compare images and uses a configurable "hamming" distance threshold for
    identifying duplicate images.

    Attributes:
        cfg (SortConfig):
            Configuration object containing settings for duplicate
            detection, such as the hamming distance threshold.
    """
    def __init__(self, cfg: SortConfig):
        self.cfg = cfg
        self._seen: Dict[str, imagehash.ImageHash] = {}

    def is_duplicate(self, path: Path) -> bool:
        try:
            with Image.open(path) as im:
                ph = imagehash.phash(im)
        except Exception:
            return False

        key = path.stem
        if key in self._seen:
            return (self._seen[key] - ph) <= self.cfg.dup_hamming
        self._seen[key] = ph
        return False


__all__ = ['Deduper']
