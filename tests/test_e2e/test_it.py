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
    out = app.outdir / "index.typ"
    assert out.exists()
    assert "Test doc for atsphinx-typst" not in out.read_text()


@pytest.mark.sphinx("typst", confoverrides={"extensions": []})
def test__auto_adding_extension(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    assert (app.outdir / "index.typ").exists()


@pytest.mark.sphinx(
    "typst",
    confoverrides={
        "typst_documents": [
            {
                "entry": "index",
                "filename": "document-1",
                "title": "test",
            },
            {
                "entry": "index",
                "filename": "document-2",
                "title": "test",
            },
        ]
    },
)
def test__multiple_output(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    assert (app.outdir / "document-1.typ").exists()
    assert (app.outdir / "document-2.typ").exists()
