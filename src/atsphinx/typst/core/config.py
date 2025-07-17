"""Configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config


class DocumentSettings(TypedDict):
    """Build settings each documets."""

    entry: str
    """Docname of entrypoint."""
    filename: str
    """Output filename (without ext)."""
    title: str
    """Title of document."""
    theme: str
    """Generate theme."""


DEFAULT_DOCUMENT_SETTINGS = {
    "theme": "manual",
}


def set_config_defaults(app: Sphinx, config: Config):
    """Inject default values of configured ``typest_documents``."""
    document_settings = config.typst_documents or []
    for idx, user_value in enumerate(document_settings):
        document_settings[idx] = DEFAULT_DOCUMENT_SETTINGS | user_value


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value(
        "typst_documents",
        [{"entry": "index", "title": "index", "theme": "manual"}],
        "env",
        list[str],
    )
    app.connect("config-inited", set_config_defaults)
