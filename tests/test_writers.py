# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D106, D107
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from docutils import nodes

from atsphinx.typst import builders as t

if TYPE_CHECKING:
    from pytest_mock import MockFixture
    from sphinx.testing.util import SphinxTestApp


class Test_TypstTranslator:
    class Test_visit_mermaid:
        @pytest.mark.sphinx("typst", testroot="with-mermaid-nodep")
        def test__no_sphinxcontrib_mermaid(self, app: SphinxTestApp):
            """Build succeeds when sphinxcontrib.mermaid is not installed.

            The ``with-mermaid-nodep`` testroot does not load ``sphinxcontrib.mermaid``
            so the ``.. mermaid::`` directive is unknown and produces no node - the
            translator's ``visit_mermaid`` is never reached, but the build must still
            complete and emit a ``.typ`` file.
            """
            app.build()
            out = app.outdir / "index.typ"
            assert out.exists()

        @pytest.mark.sphinx("typst", testroot="with-mermaid", freshenv=True)
        def test__render_produces_image(self, app: SphinxTestApp, mocker: MockFixture):
            """When render_mm succeeds the SVG is embedded as an image directive."""
            import atsphinx.typst.writer as w

            fake_relfn = "_images/mermaid-abc123.svg"
            fake_outfn = "/tmp/mermaid-abc123.svg"
            mocker.patch.object(
                w.TypstTranslator,
                "mermaid_render_to_svg",
                return_value=(fake_relfn, fake_outfn),
            )
            app.build()
            out = app.outdir / "index.typ"
            assert out.exists()
            content = out.read_text()
            # The SVG path should appear in the generated Typst source
            assert "mermaid-abc123.svg" in content

        @pytest.mark.sphinx("typst", testroot="with-mermaid", freshenv=True)
        def test__render_failure_is_skipped(self, app: SphinxTestApp, mocker: MockFixture):
            """A render error is caught, logged as a warning, and build still succeeds."""
            import atsphinx.typst.writer as w

            mocker.patch.object(
                w.TypstTranslator,
                "mermaid_render_to_svg",
                side_effect=RuntimeError("mmdc crashed"),
            )
            mock_logger = mocker.patch.object(w, "logger")
            app.build()
            out = app.outdir / "index.typ"
            assert out.exists()
            mock_logger.warning.assert_called_once()
