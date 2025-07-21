from atsphinx.mini18n import get_template_dir as get_mini18n_template_dir

from atsphinx.typst import __version__ as version

# -- Project information
project = "atsphinx-typst"
copyright = "2025, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    # Bundled extensions
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # atsphinx extensions
    "atsphinx.mini18n",
    # Third-party extensions
]
templates_path = ["_templates", get_mini18n_template_dir()]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for i18n
language = "en"
gettext_compact = False
locale_dirs = ["_locales"]

# -- Options for HTML output
html_theme = "furo"
html_static_path = ["_static"]
html_title = f"{project} v{release}"
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/atsphinx/typst/",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
}
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "mini18n/snippets/select-lang.html",
        "sidebar/search.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# -- Options for LaTeX output
latex_documents = [
    (
        "index",
        "document.tex",
        f"{project} Documentation",
        "Kazuya Takei",
        "manual",
        1,
    ),
]

# -- Options for Typst outout
typst_documents = [
    {
        "entry": "index",
        "filename": "document",
        "theme": "manual",
        "title": f"{project} Documentation",
        "toctree_only": True,
    }
]

# -- Options for extensions
# sphinx.ext.intersphinx
intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
# sphinx.ext.todo
todo_include_todos = True
# atsphinx.mini18n
mini18n_default_language = "en"
mini18n_support_languages = ["en", "ja"]
mini18n_basepath = "/typst/"
