"""Standard tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__compatibility(app: SphinxTestApp):
    """Test to pass."""
    app.build()


@pytest.mark.sphinx("typst")
def test__it(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    assert (app.outdir / "index.typ").exists()
