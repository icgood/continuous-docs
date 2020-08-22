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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import pkg_resources

import cloud_sptheme as csp


# -- Project information -----------------------------------------------------

project = 'docpkg'
copyright = '2020, Ian Good'
author = 'Ian Good'

# The short X.Y version
project_version = pkg_resources.require(project)[0].version
version_parts = project_version.split('.')
version = '.'.join(version_parts[0:2])
# The full version, including alpha/beta/rc tags
release = project_version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx_autodoc_typehints',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'cloud'

# set the theme path to point to cloud's theme data
html_theme_path = [csp.get_theme_dir()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

autodoc_member_order = 'bysource'
autodoc_default_flags = ['show-inheritance']
napoleon_numpy_docstring = False

intersphinx_mapping = {'https://docs.python.org/3/': None}
