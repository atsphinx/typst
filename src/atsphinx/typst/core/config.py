"""Configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from sphinx.application import Sphinx


class DocumentSettings(TypedDict):
    """Build settings each documets."""

    entry: str
    """Docname of entrypoint."""
    filename: str
    """Output filename (without ext)."""
    title: str
    """Title of document."""
    theme: str = "manual"
    """Generate theme."""


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value(
        "typst_documents",
        [{"entry": "index", "title": "index", "theme": "manual"}],
        "env",
        list[str],
    )
