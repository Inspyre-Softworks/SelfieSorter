# Selfie Sorter

Local-only pipeline that sorts images into `explicit/`, `suggestive/`, or `safe/`
and sub-folders by detected label (e.g., `female_breast_exposed`) using:
- OpenNSFW2 (coarse "NSFW?" score) — optional
- NudeNet (fine object detection with labels)
- imagehash (de-dup)
- exiftool (optional EXIF/GPS removal)

## Quickstart

```bash
# with Poetry
poetry install
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted"

# OR without Poetry (you provide exiftool on your PATH):
pip install pillow imagehash nudenet opennsfw2
python -m selfie_sorter.cli --in "/path/to/unsorted" --out "/path/to/sorted"
```

## Notes
- Some NudeNet builds emit `class`, others `label`. We handle both.
- Rules are normalized to UPPERCASE_WITH_UNDERSCORES for robust matching.
- Set `--no-coarse` to skip OpenNSFW2 gate.
- Use `--dup-hamming` to tune near-duplicate sensitivity (default 5).
