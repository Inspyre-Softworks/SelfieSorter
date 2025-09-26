.PHONY: help clean html live

help:
	@echo "make html     - build docs"
	@echo "make live     - auto-reload docs server"
	@echo "make clean    - remove build"

clean:
	rm -rf _build api/_autosummary

html:
	poetry run sphinx-build -b html . _build/html

live:
	poetry run sphinx-autobuild . _build/html --watch ../src/selfie_sorter
