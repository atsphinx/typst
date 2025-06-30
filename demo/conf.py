"""Configuration for demo build that works correctly on current version."""

# -- Project information
project = "Demo of atsphinx-typst"
copyright = "2025, Kazuya Takei"
author = "Kazuya Takei"
release = "0.0.0"

# -- General configuration
extensions = []
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "alabaster"
html_static_path = ["_static"]
