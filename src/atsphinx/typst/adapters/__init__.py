"""Adapter subpackage.

This package includes Sphinx extensions
that provide translation functions for custom nodes.
Each module is mapped to the same path as its corresponding Sphinx extension.
(e.g., `atsphinx.typst.adapter.sphinx.ext.todo` corresponds to `sphinx.ext.todo`)
"""

from __future__ import annotations

from importlib.util import find_spec
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def autoload_adapters(app: Sphinx):
    """Add adapter extensions based on registered extensions."""
    adapters = []
    for extname in app.extensions.keys():
        adapter_name = f"{__name__}.{extname}"
        try:
            if find_spec(adapter_name):
                adapters.append(adapter_name)
        except ModuleNotFoundError:
            # This happens when this parent module does not exist.
            pass
    for extname in adapters:
        app.setup_extension(extname)
