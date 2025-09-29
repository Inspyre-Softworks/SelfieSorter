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
# or explicitly list files to process instead of scanning the input tree
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted" --files \
  "/path/to/unsorted/a.jpg" \
  "/path/to/unsorted/subdir/b.png"
# add censored copies alongside the sorted files (pixelated by default)
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted" --censor-copies
# pick a different censor style (blurred or a black box with a label)
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted" --censor-copies \
  --censor-style blurred
# retroactively generate censored copies from an already-sorted tree
poetry run selfie-sort --censor-existing "/path/to/sorted" --censor-style black-box \
  --censor-label "CENSORED" --censor-strength 32

# OR without Poetry (you provide exiftool on your PATH):
pip install pillow imagehash nudenet opennsfw2
python -m selfie_sorter.cli --in "/path/to/unsorted" --out "/path/to/sorted"
```

## Notes
- Some NudeNet builds emit `class`, others `label`. We handle both.
- Rules are normalized to UPPERCASE_WITH_UNDERSCORES for robust matching.
- Set `--no-coarse` to skip OpenNSFW2 gate.
- Use `--dup-hamming` to tune near-duplicate sensitivity (default 5).
- Enable `--censor-copies` to write censored siblings for sharing. Use `--censor-style` to choose between
  `pixelated`, `blurred`, or `black-box`, adjust intensity with `--censor-strength`, and change the
  overlay text (for `black-box`) via `--censor-label` (supports `{label}` placeholder for the detection label).
- Run `--censor-existing /path/to/sorted` to read previously generated JSON sidecars, crop censorship to the
  recorded bounding boxes, and emit new copies suffixed with `_censored` (override with `--censor-suffix`).
