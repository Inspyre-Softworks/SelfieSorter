Command Line Interface
======================

If your project exposes a CLI (e.g., via ``entry_points``), here’s a suggested UX.
Adapt to your actual command/module names.

Basic usage
-----------
.. code-block:: bash

   poetry run selfie-sorter --in ~/Pictures/in --out ~/Pictures/out --coarse

Suggested options
-----------------
.. code-block:: text

   --in PATH              Input directory
   --out PATH             Output directory (created if missing)
   --coarse / --no-coarse Enable/disable coarse gate (OpenNSFW2)
   --nsfw-threshold F     Coarse threshold (0..1, default 0.8)
   --strip-metadata       Remove EXIF/GPS in place
   --sidecar / --no-sidecar  JSON sidecar writing
   --move-safe            Move safe images under out/safe/
   --dup-hamming N        Hamming distance for near-duplicate detection

PowerShell example
------------------
.. code-block:: powershell

   poetry run selfie-sorter `
     --in "$Env:USERPROFILE\Pictures\in" `
     --out "$Env:USERPROFILE\Pictures\out" `
     --coarse --nsfw-threshold 0.8 --strip-metadata
