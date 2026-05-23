import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "ravelpy"
copyright = "2026, Derek Rowland"
author = "Derek Rowland"
release = "0.2.2"

extensions = [
    "myst_parser",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

autoapi_dirs = ["../ravelpy"]
autoapi_type = "python"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_python_class_content = "both"
autoapi_member_order = "groupwise"
autoapi_keep_files = False
autoapi_add_toctree_entry = True

html_theme = "furo"
html_title = "ravelpy"

myst_enable_extensions = ["colon_fence"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

exclude_patterns = ["_build"]
