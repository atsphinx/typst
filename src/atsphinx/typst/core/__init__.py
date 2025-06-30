"""Core features of Typst buider.

This only provides builder with features for Sphinx and doctree components.
This is registered standalone
when call builder without register into ``extensions`` of ``conf.py``.
"""

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
