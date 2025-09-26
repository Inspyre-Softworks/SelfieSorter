Quickstart
=========

Minimal example
---------------
Sort a directory of images into ``explicit/``, ``suggestive/``, ``safe/``
(and ``dupes/`` for near-duplicates), using defaults.

.. code-block:: python

   from pathlib import Path
   from selfie_sorter.config import SortConfig
   from selfie_sorter.coarse_gate import CoarseGate
   # from selfie_sorter.sorter import Sorter   # hypothetical main orchestrator

   cfg = SortConfig(
       root_in=Path('~/Pictures/input').expanduser(),
       root_out=Path('~/Pictures/sorted').expanduser(),
       use_coarse_gate=True,
   )
   gate = CoarseGate(cfg)
   print('Gate enabled:', gate.enabled)

   # sorter = Sorter(cfg, gate=gate)
   # sorter.run()

Windows PowerShell one-liner
----------------------------
.. code-block:: powershell

   poetry run python - <<'PY'
   from pathlib import Path
   from selfie_sorter.config import SortConfig
   from selfie_sorter.coarse_gate import CoarseGate
   cfg = SortConfig(Path(r'C:\images\in'), Path(r'C:\images\out'))
   print('Gate:', CoarseGate(cfg).enabled)
   PY

What gets created
-----------------
* ``<root_out>/explicit/`` — explicit images
* ``<root_out>/suggestive/`` — suggestive images
* ``<root_out>/safe/`` — safe images (if ``move_safe=True``)
* ``<root_out>/dupes/`` — near-duplicates (perceptual hash)
* JSON sidecars (if ``write_sidecar=True``)

Next steps
----------
* See :doc:`configuration` for all options.
* Learn the :doc:`cli` usage.
* Understand the :doc:`workflow` pipeline.
