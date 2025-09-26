Installation
============

Supported environments
----------------------
* Python 3.12+ recommended
* Windows, Linux, macOS
* Optional: :mod:`opennsfw2` if you want the coarse NSFW gate

Install with Poetry (recommended)
---------------------------------
.. code-block:: bash

   # From the repo root
   poetry install
   # Include docs extras if you plan to build docs locally
   poetry install --with docs

Optional model dependencies
---------------------------
To enable the coarse probability gate:

.. code-block:: bash

   poetry run python -m pip install opennsfw2

Verifying your install
----------------------
.. code-block:: bash

   poetry run python -c "import selfie_sorter, sys; print('OK', selfie_sorter.__version__)"

Building the docs locally
-------------------------
.. code-block:: bash

   cd docs
   poetry run sphinx-build -b html . _build/html
   # or live reload while editing
   poetry run sphinx-autobuild . _build/html --watch ../src/selfie_sorter
