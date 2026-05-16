"""Generate Typst sources and PDF from Sphinx document."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rst2typst import transforms

from . import adapters, builders, config

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.1.1"


def setup(app: Sphinx):  # noqa: D103
    # Builders
    app.add_builder(builders.TypstBuilder)
    app.add_builder(builders.TypstPDFBuilder)
    app.add_transform(transforms.RemapFootnotes)
    # Configurations
    config.setup(app)
    # Connect
    app.connect("builder-inited", adapters.autoload_adapters)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
