from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


class Test_TypstTranslator:  # noqa: D101
    @pytest.mark.sphinx("typst", testroot="toctree")
    def test__start_of_file(self, app: SphinxTestApp):  # noqa: D102
        app.build()
        out = (app.outdir / "index.typ").read_text()
        assert "<docname::section-1>" in out
        assert "<docname::section-1-1>" in out
