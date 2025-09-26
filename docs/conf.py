from __future__ import annotations
import os
import sys
from datetime import datetime
from importlib.metadata import version as pkg_version, PackageNotFoundError

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../src'))

project = 'selfie-sorter'
author = 'Taylor (“Tay-Tay”)'
current_year = str(datetime.now().year)
copyright = f'{current_year}, {author}'

# Project version strings
try:
    release = pkg_version('selfie_sorter')
except PackageNotFoundError:
    release = '0.0.0'
version = '.'.join(release.split('.')[:2])

# -- General config ----------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosectionlabel',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_param = True
napoleon_use_rtype = False
napoleon_attr_annotations = True

autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'show-inheritance': True,
    'inherited-members': True,
}
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# 🚨 This line tells Sphinx to pull the class docstring from __init__,
# so Parameters only appear once.
autoclass_content = 'init'

# Make section labels unique across files
autosectionlabel_prefix_document = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

html_theme = 'furo'
html_static_path = ['_static']
html_title = f'{project} {release}'
html_show_sourcelink = True

myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'linkify',
]

templates_path = ['_templates']

master_doc = 'index'
