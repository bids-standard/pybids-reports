# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# from bids.ext.reports._version import __version__
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.pardir))
sys.path.insert(0, os.path.abspath("sphinxext"))

from github_link import make_linkcode_resolve

import bids.ext.reports

__version__ = bids.ext.reports.__version__

# The full version, including alpha/beta/rc tags
release = __version__
version = __version__

# -- Project information -----------------------------------------------------

project = "pybids-reports"
copyright = "2023, PyBIDS Developers"
author = "PyBIDS Developers"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_gallery.load_style",
    "sphinxarg.ext",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -----------------------------------------------------------------------------
# linkcode
# -----------------------------------------------------------------------------
# The following is used by sphinx.ext.linkcode to provide links to github
linkcode_resolve = make_linkcode_resolve(
    "bids.ext.reports",
    "https://github.com/bids-standard/pybids-reports/blob/{revision}/{package}/{path}#L{lineno}",
)

# -----------------------------------------------------------------------------
# intersphinx
# -----------------------------------------------------------------------------
_python_version_str = f"{sys.version_info.major}.{sys.version_info.minor}"
_python_doc_base = "https://docs.python.org/" + _python_version_str
intersphinx_mapping = {
    "python": (_python_doc_base, None),
    "numpy": ("https://numpy.org/doc/stable/", (None, "./_intersphinx/numpy-objects.inv")),
    "scipy": (
        "https://docs.scipy.org/doc/scipy/reference",
        (None, "./_intersphinx/scipy-objects.inv"),
    ),
    "bids": (
        "https://bids-standard.github.io/pybids",
        (None, "./_intersphinx/pybids-objects.inv"),
    ),
}
