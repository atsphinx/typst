"""Test for adapter bridge."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("typst")
def test_default(app: SphinxTestApp):
    """Test case for none work ``autoload_adapters``."""
    extensions = [
        name
        for name, ext in app.extensions.items()
        if name.startswith("atsphinx.typst")
    ]
    assert len(extensions) == 1


@pytest.mark.sphinx("typst", confoverrides={"extensions": ["sphinx.ext.todo"]})
def test_autoload(app: SphinxTestApp):
    """Test behavior of ``autoload_adapters``.

    It can find ``sphinx.ext.todo``
    and register ``atsphinx.typst.adapters.sphinx.ext.todo``.
    """
    extensions = [
        name
        for name, ext in app.extensions.items()
        if name.startswith("atsphinx.typst")
    ]
    assert len(extensions) == 2
    assert "atsphinx.typst.adapters.sphinx.ext.todo" in app.extensions
