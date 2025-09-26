Workflow & Pipeline
===================

A typical run looks like this:

1. **Scan**: walk ``root_in`` recursively and discover images.
2. **Deduplicate**: compute perceptual hashes; group by Hamming distance (``dup_hamming``).
3. **Coarse gate** (optional): if :class:`~selfie_sorter.coarse_gate.CoarseGate.enabled` is true,
   fetch a probability with :func:`opennsfw2.predict_image`. If the score is below
   ``nsfw_threshold``, skip expensive detectors or mark as safe/suggestive depending on policy.
4. **Fine classification**: apply your detector(s) and map labels via ``explicit_rules`` /
   ``suggestive_rules``.
5. **Actions**:
   - Move files into ``explicit/``, ``suggestive/``, ``safe/``.
   - Write sidecar JSON if enabled.
   - Strip metadata if enabled.

Design notes
------------
* The coarse gate is **best-effort**—it returns ``None`` if unavailable or errors.
* Keep I/O bounded: batch moves, avoid redundant hashing, and persist a scan DB if needed.
