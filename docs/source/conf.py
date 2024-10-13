# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# sys.path.insert(0, os.path.abspath("../../src/"))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "manager_cw_bot_api")))


project = 'Manager CW Bot'
copyright = '2024, Alexander Laptev, CW'
author = 'Alexander Laptev, CW'
version = '6.0.0'
release = '6.0.0'
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.viewcode", "sphinx_favicon", 'sphinx_rtd_theme',
]

# Keep the type hints outside the function signature, moving them to the
# descriptions of the relevant function/methods.
autodoc_typehints = "description"
autodoc_mock_imports = ["manager_cw_bot_api"]


templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_permalinks_icon = '<span>#</span>'

html_theme = 'renku'
html_show_sourcelink = False
html_show_sphinx = False
html_static_path = ['_static']
# html_theme_options = {
#     'prev_next_buttons_location': None
# }

favicons = [
   {"rel": "icon", "href": "favicons/FaviconSVG_ManagerCWBotAPI.svg", "type": "image/svg+xml"},
   {"rel": "icon", "sizes": "16x16", "href": "favicons/favicon/favicon-16x16.png", "type": "image/png"},
   {"rel": "icon", "sizes": "32x32", "href": "favicons/favicon/favicon-32x32.png", "type": "image/png"},
   {"rel": "apple-touch-icon", "sizes": "180x180", "href": "favicons/favicon/apple-touch-icon-180x180.png", "type": "image/png"},
   {"rel": "mask-icon", "href": "favicons/favicon/safari-pinned-tab.svg", "color": "#5bbad5"}
]

# html_favicon = os.path.abspath("../../src/docs_src/favicon/favicon.ico")

html_logo = "../../docs/build/html/_static/favicons/manager_cw_bot_logo_black_and_cw-white_200pxX200px.svg"

