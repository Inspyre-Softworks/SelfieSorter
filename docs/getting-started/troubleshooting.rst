Troubleshooting
===============

Sphinx docs build fails with intersphinx error
----------------------------------------------
**Symptom:** ``Invalid inventory location value '{}'``

**Fix:** In ``docs/conf.py`` use ``None`` for the inventory tuple:
``intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}``

Sphinx warns 'version has type function'
----------------------------------------
**Fix:** Alias the importlib function and set strings:
``from importlib.metadata import version as pkg_version`` then set
``release = pkg_version('selfie_sorter'); version = '.'.join(release.split('.')[:2])``.

Coarse gate always disabled
---------------------------
**Cause:** Either :mod:`opennsfw2` isn’t installed or
:attr:`~selfie_sorter.config.SortConfig.use_coarse_gate` is ``False``.

**Fix:** ``poetry run python -m pip install opennsfw2`` and ensure your config enables it.

Windows: 'make' not found
-------------------------
**Fix:** Use the batch file or call Sphinx directly:

.. code-block:: powershell

   poetry run make.bat html
   # or:
   poetry run sphinx-build -b html . _build/html
