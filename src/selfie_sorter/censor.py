"""Utility helpers for generating censored image copies."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter, ImageFont


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

    def create_copy(self, source: Path, destination: Optional[Path] = None) -> Path:
        """Write a censored copy of ``source`` to ``destination``.

        Parameters
        ----------
        source:
            Original image that has already been sorted.
        destination:
            Optional output path.  When omitted a sibling file suffixed with
            ``_censored`` is produced.
        """
        if not source.is_file():
            raise ValueError(f'Not a file: {source!s}')

        if destination is None:
            destination = source.with_name(f'{source.stem}_censored{source.suffix}')

        destination.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(source) as image:
            image.load()
            censored = self._apply(image)
            censored.save(destination)

        return destination

    def _apply(self, image: Image.Image) -> Image.Image:
        if self.style == 'pixelated':
            return self._pixelate(image)
        if self.style == 'blurred':
            return image.filter(ImageFilter.GaussianBlur(radius=self.strength))
        return self._black_box(image)

    def _pixelate(self, image: Image.Image) -> Image.Image:
        shrink_w = max(1, image.width // self.strength)
        shrink_h = max(1, image.height // self.strength)
        censored = image.resize((shrink_w, shrink_h), Image.BILINEAR)
        return censored.resize(image.size, Image.NEAREST)

    def _black_box(self, image: Image.Image) -> Image.Image:
        censored = image.copy()
        draw = ImageDraw.Draw(censored, 'RGBA')
        margin = max(0, min(image.size) // 20)
        box_height = max(self.strength, image.height // 3)
        top = max(margin, (image.height - box_height) // 2)
        bottom = min(image.height - margin, top + box_height)
        draw.rectangle(
            [(margin, top), (image.width - margin, bottom)],
            fill=(0, 0, 0, 255),
        )
        if self.label:
            font = ImageFont.load_default()
            try:
                text_bbox = draw.textbbox((0, 0), self.label, font=font)
                text_w = text_bbox[2] - text_bbox[0]
                text_h = text_bbox[3] - text_bbox[1]
            except AttributeError:  # pragma: no cover - Pillow < 8 compatibility
                text_w, text_h = draw.textsize(self.label, font=font)
            text_x = (image.width - text_w) / 2
            text_y = top + (box_height - text_h) / 2
            draw.text((text_x, text_y), self.label, fill='white', font=font)
        return censored


__all__ = ['ImageCensor']
