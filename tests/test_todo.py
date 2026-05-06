"""Test for adapted ``sphinx.ext.todo``."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("typst", testroot="with-todo")
def test_not_included(app: SphinxTestApp):
    app.build()
    out = app.outdir / "index.typ"
    assert "Test it." not in out.read_text()


@pytest.mark.sphinx(
    "typst",
    testroot="with-todo",
    confoverrides={"todo_include_todos": True},
)
def test_included(app: SphinxTestApp):
    app.build()
    out = app.outdir / "index.typ"
    print(out.read_text())
    assert "Test it." in out.read_text()
