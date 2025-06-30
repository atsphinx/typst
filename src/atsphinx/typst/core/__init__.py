"""Core component for only Sphinx and docutils standard features."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .. import __version__
from . import builders

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: Sphinx):  # noqa: D103
    # Builders
    app.add_builder(builders.TypstBuilder)
    app.add_builder(builders.TypstPDFBuilder)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
