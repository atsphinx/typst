"""Configuration."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config


class DocumentSettings(TypedDict):
    """Build settings each documets."""

    entrypoint: str
    """Docname of entrypoint."""
    filename: str
    """Output filename (without ext)."""
    title: str
    """Title of document."""
    theme: str
    """Generate theme."""
    toctree_only: bool
    """When it is ``True``, builder only write contents of toctree from 'entrypoint'."""


DEFAULT_DOCUMENT_SETTINGS = {
    "theme": "manual",
    "toctree_only": False,
}


def compute_configurations(app: Sphinx, config: Config):
    """Clean up configurations for this extensions."""
    # 1. Inject default values of configured ``typst_documents``.
    document_settings = config.typst_documents or []
    if not document_settings:
        document_settings.append(
            {
                "entrypoint": config.root_doc,
                "filename": f"document-{config.language}",
                "title": f"{config.project} Documentation [{config.language.upper()}]",
                "theme": "manual",
            }
        )
    for idx, user_value in enumerate(document_settings):
        document_settings[idx] = DEFAULT_DOCUMENT_SETTINGS | user_value
    config.typst_documents = document_settings

    # 2. Cast string path to Path object.
    typst_static_path = []
    for p in config.typst_static_path:
        if isinstance(p, Path):
            typst_static_path.append(p)
            continue
        typst_static_path.append(app.confdir / p)
    config.typst_static_path = typst_static_path


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("typst_documents", [], "env", list[dict])
    app.add_config_value("typst_static_path", [], "env", [list[str | Path]])
    app.connect("config-inited", compute_configurations)
