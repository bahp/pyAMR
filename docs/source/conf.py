# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# https://github.com/sphinx-gallery/sphinx-gallery/issues/797
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath('../../pyamr/'))


# -- Project information -----------------------------------------------------

project = 'pyamr'
copyright = '2021-%s, Bernard Hernandez' % date.today().year
author = 'Bernard Hernandez'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration',         # see what files take longer.
    #'sphinx.ext.doctest',         # allows to test within docs.
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_gallery.gen_gallery',  # example galleries
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',         # docstrings
    'sphinx.ext.autosectionlabel', # adds labels to sections
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',      # gh-pages needs a .nojekyll file
    'sphinxcontrib.bibtex',
    'autodocsumm',
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

# ---------------------
# Autosummary extension
# ---------------------
# Generate autosummary even if no references
autosummary_generate = True

# ---------------------------
# Autosection label extension
# ---------------------------
# Make sure the target is unique
autosectionlabel_prefix_document = True

autodoc_default_options = {
    'autosummary': True,
}

"""
intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_reftypes = ["*"]
"""

# ------------------
# Plotly outcomes
# ------------------
# Include plotly
import plotly.io as pio
pio.renderers.default = 'sphinx_gallery'


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
    'examples_dirs': [
        '../../examples/tutorial',
        '../../examples/indexes',
        '../../examples/forecasting',
        #'../../examples/reports',
        '../../examples/visualization',
        '../../pyamr/examples'
    ],
    # path to where to save gallery generated output
    'gallery_dirs': [
        '../source/_examples/tutorial',
        '../source/_examples/indexes',
        '../source/_examples/forecasting',
        #'../source/_examples/reports',
        '../source/_examples/visualization',
        '../source/_examples/pyamr/examples'
    ],
    # Other
    'line_numbers': True,
    'download_all_examples': False,

    # Sort galleries
    # --------------
    'within_subsection_order': FileNameSortKey,

    # Add intersphinx links to the examples
    # -------------------------------------
    'prefer_full_module': [
        # a list of regex command of your module where the full module
        # name should be used for sphinx_gallery instead of the shortend
        'pyamr.*+\d{4}',
    ],
    'reference_url': {
        # The module you locally document uses None
        'sphinx_gallery': None,
    },

    # Mini galleries for API documentation
    # ------------------------------------
    # directory where function/class granular galleries are stored
    'backreferences_dir': '_backreferences',

    # Modules for which function/class level galleries are created.
    # In this case sphinx_gallery and numpy in a tuple of strings.
    'doc_module': ('numpy', 'pyamr'),

    # Objects to exclude from implicit backreferences. The default
    # option is an empty set, i.e. exclude nothing.
    'exclude_implicit_doc': {},
}

# ------------------
# Bibtex extension
# ------------------
bibtex_bibfiles = ['refs.bib']

# ------------------
# Todo extension
# ------------------
todo_include_todos = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    #'analytics_id': 'G-XXXXXXXXXX',  #  Provided by Google in your dashboard
    #'analytics_anonymize_ip': False,
    #'logo_only': False,
    #'display_version': True,
    #'prev_next_buttons_location': 'bottom',
    #'style_external_links': False,
    #'vcs_pageview_mode': '',
    #'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 8,
    'includehidden': True,
    'titles_only': False
}

# Configuration of sphin_rtd_theme
#html_logo = './_static/images/logo-ls2d-v1.png'
html_favicon = './_static/images/logo-pyamr-icon-v2.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add custom css file.
html_css_files = ['css/custom.css']

# Substitute project name into .rst files when |project_name| is used
rst_epilog = """"""
rst_epilog = """.. |project_name| replace:: %s""" % project

"""
    .. |project_name| replace:: %s
    .. |project_logo| image:: %s
        :width: 100
        :alt: pyAMR
"""
