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
# add censored copies organized under <out>/censored (pixelated by default)
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted" --censor-copies
# store censored copies in a custom directory (relative paths resolve under --out)
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted" --censor-copies \
  --censor-dir shared_censors
# pick a different censor style (blurred or a black box with a label)
poetry run selfie-sort --in "/path/to/unsorted" --out "/path/to/sorted" --censor-copies \
  --censor-style blurred
# retroactively generate censored copies from an already-sorted tree
poetry run selfie-sort --censor-existing "/path/to/sorted" --censor-style black-box \
  --censor-label "CENSORED" --censor-strength 32 --censor-dir retro_censored

# OR without Poetry (you provide exiftool on your PATH):
pip install pillow imagehash nudenet opennsfw2
python -m selfie_sorter.cli --in "/path/to/unsorted" --out "/path/to/sorted"
```

## Notes
- Some NudeNet builds emit `class`, others `label`. We handle both.
- Rules are normalized to UPPERCASE_WITH_UNDERSCORES for robust matching.
- Set `--no-coarse` to skip OpenNSFW2 gate.
- Use `--dup-hamming` to tune near-duplicate sensitivity (default 5).
- Enable `--censor-copies` to write censored versions under `<out>/censored`. Use `--censor-style` to choose between
  `pixelated`, `blurred`, or `black-box`, adjust intensity with `--censor-strength`, and change the
  overlay text (for `black-box`) via `--censor-label` (supports `{label}` placeholder for the detection label). Use
  `--censor-dir` to redirect the censored tree elsewhere (relative paths resolve under `--out`).
- Run `--censor-existing /path/to/sorted` to read previously generated JSON sidecars, crop censorship to the
  recorded bounding boxes, and emit new copies suffixed with `_censored` (override with `--censor-suffix`). By default
  the censored tree is written to `<root>/censored`; combine with `--censor-dir` to change the destination.
