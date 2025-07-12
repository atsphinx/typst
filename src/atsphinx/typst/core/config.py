"""Configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value(
        "typst_documents",
        ["index"],
        "env",
        list[str],
    )
