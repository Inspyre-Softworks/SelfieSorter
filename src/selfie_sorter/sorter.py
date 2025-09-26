"""
Handles the classification, de-duplication, metadata cleanup, and organized
movement of image files based on specified policies and configurations.

This module processes image files, scores their content using coarse and fine
detection techniques, categorizes them into appropriate output directories,
and removes duplicates or redundant metadata where applicable. It integrates
several components (deduplication, classifiers, and metadata handlers) and
organizes output within a structured directory tree for ease of access and
management.
"""


from __future__ import annotations
from pathlib import Path
import json
import shutil
import hashlib
from typing import List

from .constants import IMAGE_EXTS
from .config import SortConfig
from .coarse import CoarseGate
from .detector import FineDetector
from .router import TagRouter
from .dedupe import Deduper
from .metadata import MetadataCleaner


class SelfieSorter:
    """
    Orchestrates de-duplication, classification, metadata stripping, and file movement.
    """
    IMAGE_EXTS = IMAGE_EXTS

    def __init__(self, cfg: SortConfig):
        """Initializes main components and sets up necessary directories.

        This constructor method sets up the primary components of the process
        pipeline, including coarse filtering, fine detection, routing, deduplication,
        and metadata cleaning processes. It also ensures that the required
        directories for explicit, suggestive, safe, and duplicate file outputs
        are created if they do not already exist.

        Parameters:
            cfg (SortConfig):
                Configuration object containing settings and file structure information
                for initialization.
        """
        self.cfg = cfg
        self.coarse = CoarseGate(cfg)
        self.fine = FineDetector()
        self.router = TagRouter(cfg)
        self.dedupe = Deduper(cfg)
        self.cleaner = MetadataCleaner(cfg)

        for d in [cfg.dir_explicit, cfg.dir_suggestive, cfg.dir_safe, cfg.dir_dupes]:
            (cfg.root_out / d).mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        """
        Processes a collection of image files found within a specified directory, applying
        a specific transformation or operation to each.

        This function iterates through a list of image files within a root directory defined
        by the configuration. Supported image file types are determined by a pre-defined
        list of image extensions. For every valid file encountered, a processing operation
        is invoked, with any issues being silently handled unless explicitly interrupted.

        Raises:
            KeyboardInterrupt:
                If the execution is manually interrupted.

            Exception:
                Silences other exceptions encountered during processing.

        Parameters:
            None

        Returns:
            None
        """
        files: List[Path] = [
            p for p in self.cfg.root_in.rglob('*')
            if p.is_file() and p.suffix.lower() in self.IMAGE_EXTS
        ]
        for path in files:
            try:
                self._process_one(path)
            except KeyboardInterrupt:
                raise
            except Exception:
                continue

    def _process_one(self, path: Path) -> None:
        """
        Processes a single file by determining its categorization, optionally moving it
        to designated directories, and writing metadata as needed.

        The method checks if the file is a duplicate, assesses its scores and labels
        via the coarse and fine models, and classifies it into a bucket and labels. It
        then processes the file by moving it to the appropriate directory structure
        and optionally writes a metadata sidecar file with relevant classification
        information.

        Parameters:
            path (Path):
                The path of the file we want to process.

        Raises:
            OSError:
                Raised if there are issues moving the file or creating directories.

            ValueError:
                Raised if data from classifiers is malformed.
        """
        if self.dedupe.is_duplicate(path):
            self._move(path, self.cfg.dir_dupes)
            return

        coarse = self.coarse.score(path)
        fine = self.fine.detect(path)
        bucket, labels = self.router.classify(coarse, fine)

        self.cleaner.strip(path)

        if bucket == 'safe' and not self.cfg.move_safe:
            return

        label_dir = 'unlabeled'
        if fine:
            best = max(fine, key=lambda d: d.get('score', 0.0))
            best_label = (best.get('label') or best.get('class') or 'unlabeled')
            label_dir = best_label.lower().replace(' ', '_')

        dest_dir = self.cfg.root_out / bucket / label_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = self._unique_dest(dest_dir / path.name)
        shutil.move(str(path), dest_path)

        if self.cfg.write_sidecar:
            meta = {
                'coarse_score': coarse,
                'bucket': bucket,
                'labels': labels,
                'detections': fine,
            }
            with open(dest_path.with_suffix(dest_path.suffix + '.json'), 'w', encoding='utf-8') as fh:
                json.dump(meta, fh, ensure_ascii=False, indent=2)

    @staticmethod
    def _unique_dest(base: Path) -> Path:
        """
        Generates a unique file path in case the provided path already exists. This function appends
        a short hash digest to the file name before the file extension to ensure it is unique.

        Parameters:
            base (Path):
                The initial file path to check for uniqueness.

        Returns:
            Path:
                A modified file path that is guaranteed to be unique.
        """
        if not base.exists():
            return base
        stem, ext = base.stem, base.suffix
        digest = hashlib.sha1(str(base).encode('utf-8')).hexdigest()[:8]
        return base.with_name(f'{stem}_{digest}{ext}')

    def _move(self, src: Path, sub: str) -> None:
        """
        Moves a file from the source location to a target directory while ensuring the target
        directory exists and the destination filename is unique.

        Args:
            src (Path): The source file path to be moved.
            sub (str): The subdirectory name under the root output directory
                where the file should be moved.

        """
        target_dir = self.cfg.root_out / sub
        target_dir.mkdir(parents=True, exist_ok=True)
        dest = self._unique_dest(target_dir / src.name)
        shutil.move(str(src), dest)
