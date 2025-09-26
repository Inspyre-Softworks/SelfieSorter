\
@echo off
if "%1"=="clean" (
  rmdir /S /Q _build 2>nul
  rmdir /S /Q api\_autosummary 2>nul
  goto :eof
)
if "%1"=="html" (
  poetry run sphinx-build -b html . _build\html
  goto :eof
)
if "%1"=="live" (
  poetry run sphinx-autobuild . _build\html --watch ..\src\selfie_sorter
  goto :eof
)
echo Usage: make [clean|html|live]
