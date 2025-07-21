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
    toctree_only: bool
    """When it is ``True``, builder only write contents of toctree from 'entry'."""


DEFAULT_DOCUMENT_SETTINGS = {
    "theme": "manual",
    "toctree_only": False,
}


def set_config_defaults(app: Sphinx, config: Config):
    """Inject default values of configured ``typst_documents``."""
    document_settings = config.typst_documents or []
    if not document_settings:
        document_settings.append(
            {
                "entry": config.root_doc,
                "filename": f"document-{config.language}",
                "title": f"{config.project} Documentation [{config.language.upper()}]",
                "theme": "manual",
            }
        )
    for idx, user_value in enumerate(document_settings):
        document_settings[idx] = DEFAULT_DOCUMENT_SETTINGS | user_value
    config.typst_documents = document_settings


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("typst_documents", [], "env", list[dict])
    app.connect("config-inited", set_config_defaults)
