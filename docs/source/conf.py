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
import os
import sys
sys.path.insert(0, os.path.abspath('../../fyp2020-username/'))


# -- Project information -----------------------------------------------------

project = 'fyp2020-username'
copyright = '2021, <Full name>'
author = '<Full name>'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',        # docstrings
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',     # gh-pages needs a .nojekyll file
    'sphinx_gallery.gen_gallery'  # example galleries
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# ------------------
# Napoleon extension
# ------------------
# Configuration parameters for napoleon extension
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True


# ------------------
# Sphinx gallery
# ------------------
# Information about the sphinx gallery configuration
# https://sphinx-gallery.github.io/stable/configuration.html

# Import library
from sphinx_gallery.sorting import FileNameSortKey

# Configuration for sphinx_gallery
sphinx_gallery_conf = {
    # path to your example scripts
    'examples_dirs': ['../../examples/tutorial'],
    # path to where to save gallery generated output
    'gallery_dirs': ['../source/_examples/tutorial'],
    # Other
    'line_numbers': True,
    'download_all_examples': False,
    'within_subsection_order': FileNameSortKey}

# ------------------
# Todo extension
# ------------------
todo_include_todos = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Substitute project name into .rst files when |project_name| is used
rst_epilog = '.. |project_name| replace:: %s' % project
