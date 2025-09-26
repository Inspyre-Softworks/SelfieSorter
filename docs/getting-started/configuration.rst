Configuration
=============

High-level
----------
Most tuning lives in :class:`~selfie_sorter.config.SortConfig`.

Key options
-----------
.. list-table::
   :header-rows: 1

   * - Field
     - Type
     - Purpose
   * - ``root_in``
     - :class:`~pathlib.Path`
     - Input directory scanned recursively.
   * - ``root_out``
     - :class:`~pathlib.Path`
     - Destination root for sorted output.
   * - ``use_coarse_gate``
     - ``bool``
     - Enable :class:`~selfie_sorter.coarse_gate.CoarseGate` if available.
   * - ``nsfw_threshold``
     - ``float``
     - Threshold for coarse score (0..1).
   * - ``explicit_rules``
     - ``tuple[str, ...]``
     - Labels counted as explicit.
   * - ``suggestive_rules``
     - ``tuple[str, ...]``
     - Labels counted as suggestive.
   * - ``dup_hamming``
     - ``int``
     - Hamming distance for near-duplicate detection.
   * - ``strip_metadata``
     - ``bool``
     - Remove EXIF/GPS in-place.
   * - ``write_sidecar``
     - ``bool``
     - Write JSON sidecars with decisions.
   * - ``move_safe``
     - ``bool``
     - Move safe images to ``root_out/safe/``.

Example
-------
.. code-block:: python

   from pathlib import Path
   from selfie_sorter.config import SortConfig

   cfg = SortConfig(
       root_in=Path('~/Pictures/in').expanduser(),
       root_out=Path('~/Pictures/out').expanduser(),
       use_coarse_gate=True,
       nsfw_threshold=0.8,
       dup_hamming=5,
       strip_metadata=True,
       write_sidecar=True,
       move_safe=False,
   )
