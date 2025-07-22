"""Generate Typst sources and PDF from Sphinx document."""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import builders, config

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.0.2"


def setup(app: Sphinx):  # noqa: D103
    # Builders
    app.add_builder(builders.TypstBuilder)
    app.add_builder(builders.TypstPDFBuilder)
    # Configurations
    config.setup(app)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
