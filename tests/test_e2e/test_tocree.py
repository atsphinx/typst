"""Cases for toctree option of document settingds."""

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("typst", testroot="toctree")
def test__it(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    out = app.outdir / "index.typ"
    print(out.read_text())
    assert out.exists()
    assert "#heading(" in out.read_text()
    assert "Test doc for atsphinx-typst" not in out.read_text()
    assert (
        textwrap.dedent("""\
        #heading(
          level: 1,
          [
            Section title 1
          ]
        )""")
        in out.read_text()
    )
    assert (
        textwrap.dedent("""\
        #heading(
          level: 2,
          [
            Sub section 1-1
          ]
        )""")
        in out.read_text()
    )
