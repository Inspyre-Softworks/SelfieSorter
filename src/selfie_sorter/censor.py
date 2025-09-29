"""Utility helpers for generating censored image copies."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .constants import IMAGE_EXTS


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CensorBox:
    """Normalized description of a censor region."""

    left: int
    top: int
    right: int
    bottom: int
    label: Optional[str] = None

    def as_tuple(self) -> Tuple[int, int, int, int]:
        return (self.left, self.top, self.right, self.bottom)


class ImageCensor:
    """Create censored copies of images for safer sharing."""

    _VALID_STYLES = {'pixelated', 'blurred', 'black_box'}

    def __init__(self, *, style: str = 'pixelated', strength: int = 12, label: str = 'CENSORED') -> None:
        normalized = style.lower().replace('-', '_')
        if normalized not in self._VALID_STYLES:
            raise ValueError(f'Unsupported censor style: {style!r}')
        if strength < 1:
            raise ValueError('strength must be >= 1')
        self.style = normalized
        self.strength = strength
        self.label = label

    def create_copy(
        self,
        source: Path,
        destination: Optional[Path] = None,
        *,
        boxes: Optional[Sequence[Tuple[int, int, int, int]]] = None,
        detections: Optional[Sequence[object]] = None,
    ) -> Path:
        """Write a censored copy of ``source`` to ``destination``.

        Parameters
        ----------
        source:
            Original image that has already been sorted.
        destination:
            Optional output path.  When omitted a sibling file suffixed with
            ``_censored`` is produced.
        boxes:
            Optional sequence of explicit pixel coordinates ``(left, top, right, bottom)``
            that should be censored.
        detections:
            Optional NudeNet-style detection dictionaries used to derive censor boxes.
        """
        if not source.is_file():
            raise ValueError(f'Not a file: {source!s}')

        if destination is None:
            destination = source.with_name(f'{source.stem}_censored{source.suffix}')

        destination.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(source) as image:
            image.load()
            resolved = self._resolve_boxes(image.size, boxes=boxes, detections=detections)
            censored = self._apply(image, resolved)
            censored.save(destination)

        return destination

    def _resolve_boxes(
        self,
        size: Tuple[int, int],
        *,
        boxes: Optional[Sequence[Tuple[int, int, int, int]]] = None,
        detections: Optional[Sequence[object]] = None,
    ) -> List[CensorBox]:
        width, height = size
        resolved: List[CensorBox] = []

        if boxes:
            for box in boxes:
                normalized = self._normalize_box(tuple(box), width, height)
                if normalized:
                    resolved.append(CensorBox(*normalized))

        if not resolved and detections:
            for det in detections:
                if not isinstance(det, dict):
                    continue
                raw_box = det.get('box') or det.get('bbox') or det.get('rect')
                if not raw_box:
                    continue
                normalized = self._normalize_box(tuple(raw_box), width, height)
                if not normalized:
                    continue
                label = det.get('label') or det.get('class')
                resolved.append(CensorBox(*normalized, label=label))

        return resolved

    @staticmethod
    def _normalize_box(box: Tuple[float, float, float, float], width: int, height: int) -> Optional[Tuple[int, int, int, int]]:
        if len(box) != 4:
            return None

        x1, y1, x2, y2 = box

        def clamp(val: float, upper: int) -> int:
            return max(0, min(int(round(val)), upper))

        # Determine whether the box is normalized (0-1) or absolute coordinates.
        normalized = all(0.0 <= coord <= 1.0 for coord in box)
        if normalized:
            if x2 <= 1.0 and x2 <= x1:
                x2 = x1 + max(0.0, x2)
            if y2 <= 1.0 and y2 <= y1:
                y2 = y1 + max(0.0, y2)
            x1 *= width
            x2 *= width
            y1 *= height
            y2 *= height
        else:
            if x2 <= x1:
                x2 = x1 + max(0.0, x2)
            if y2 <= y1:
                y2 = y1 + max(0.0, y2)

        left = clamp(x1, width)
        top = clamp(y1, height)
        right = clamp(x2, width)
        bottom = clamp(y2, height)

        if right - left <= 1 or bottom - top <= 1:
            return None

        return (left, top, right, bottom)

    def _apply(self, image: Image.Image, boxes: Sequence[CensorBox]) -> Image.Image:
        if not boxes:
            if self.style == 'pixelated':
                return self._pixelate_region(image, (0, 0, image.width, image.height))
            if self.style == 'blurred':
                return image.filter(ImageFilter.GaussianBlur(radius=self.strength))
            return self._black_box_regions(image, [CensorBox(0, 0, image.width, image.height, self.label)])

        if self.style == 'pixelated':
            return self._apply_pixelate(image, boxes)
        if self.style == 'blurred':
            return self._apply_blur(image, boxes)
        return self._black_box_regions(image, boxes)

    def _apply_pixelate(self, image: Image.Image, boxes: Sequence[CensorBox]) -> Image.Image:
        censored = image.copy()
        for box in boxes:
            region = self._pixelate_region(image, box.as_tuple())
            censored.paste(region, (box.left, box.top))
        return censored

    def _pixelate_region(self, image: Image.Image, box: Tuple[int, int, int, int]) -> Image.Image:
        left, top, right, bottom = box
        region = image.crop((left, top, right, bottom))
        shrink_w = max(1, region.width // self.strength)
        shrink_h = max(1, region.height // self.strength)
        small = region.resize((shrink_w, shrink_h), Image.BILINEAR)
        return small.resize(region.size, Image.NEAREST)

    def _apply_blur(self, image: Image.Image, boxes: Sequence[CensorBox]) -> Image.Image:
        censored = image.copy()
        for box in boxes:
            left, top, right, bottom = box.as_tuple()
            region = image.crop((left, top, right, bottom))
            blurred = region.filter(ImageFilter.GaussianBlur(radius=self.strength))
            censored.paste(blurred, (left, top))
        return censored

    def _black_box_regions(self, image: Image.Image, boxes: Sequence[CensorBox]) -> Image.Image:
        censored = image.copy()
        draw = ImageDraw.Draw(censored, 'RGBA')
        font = ImageFont.load_default() if self.label else None
        for box in boxes:
            left, top, right, bottom = box.as_tuple()
            draw.rectangle([(left, top), (right, bottom)], fill=(0, 0, 0, 255))
            text = self.label
            if text and '{label}' in text:
                text = text.format(label=box.label or '')
            if text and font:
                try:
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_w = text_bbox[2] - text_bbox[0]
                    text_h = text_bbox[3] - text_bbox[1]
                except AttributeError:  # pragma: no cover - Pillow < 8 compatibility
                    text_w, text_h = draw.textsize(text, font=font)
                text_x = left + (right - left - text_w) / 2
                text_y = top + (bottom - top - text_h) / 2
                draw.text((text_x, text_y), text, fill='white', font=font)
        return censored


def censor_sorted_tree(
    root: Path,
    *,
    censor: ImageCensor,
    suffix: str = '_censored',
    image_exts: Iterable[str] = IMAGE_EXTS,
) -> List[Path]:
    """Generate censored copies for images that already have NudeNet metadata.

    Parameters
    ----------
    root:
        Directory containing sorted images and JSON sidecars.
    censor:
        Configured :class:`ImageCensor` instance.
    suffix:
        Suffix appended to the generated filenames.
    image_exts:
        Iterable of supported image extensions.
    """

    root = Path(root)
    if not root.is_dir():
        raise ValueError(f'Not a directory: {root!s}')

    created: List[Path] = []
    normalized_exts = {ext.lower() for ext in image_exts}

    for image_path in sorted(root.rglob('*')):
        if image_path.suffix.lower() not in normalized_exts:
            continue

        sidecar = image_path.with_suffix(image_path.suffix + '.json')
        if not sidecar.exists():
            logger.warning('Skipping %s: missing sidecar %s', image_path, sidecar.name)
            continue

        try:
            with open(sidecar, 'r', encoding='utf-8') as fh:
                metadata = json.load(fh)
        except Exception:
            logger.warning('Skipping %s: failed to parse %s', image_path, sidecar.name, exc_info=True)
            continue

        detections = metadata.get('detections') or []
        if not detections:
            logger.info('Skipping %s: no detections recorded', image_path)
            continue

        destination = _unique_destination(
            image_path.with_name(f'{image_path.stem}{suffix}{image_path.suffix}')
        )
        try:
            censor.create_copy(image_path, destination, detections=detections)
        except Exception:
            logger.warning('Failed to create censored copy for %s', image_path, exc_info=True)
            continue

        created.append(destination)

    return created


def _unique_destination(base: Path) -> Path:
    if not base.exists():
        return base
    stem, ext = base.stem, base.suffix
    counter = 1
    candidate = base
    while candidate.exists():
        candidate = base.with_name(f'{stem}_{counter}{ext}')
        counter += 1
    return candidate


__all__ = ['CensorBox', 'ImageCensor', 'censor_sorted_tree']
