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


class Test_TypstBuilder:
    class Test_assemble_doctree:
        @pytest.mark.sphinx("typst", testroot="hidden-toctree")
        @pytest.mark.parametrize("arg", [(True,), ("all",)])
        def test__toctree_only(self, app: SphinxTestApp, arg):
            """Test to pass."""
            app.build()
            builder: t.TypstBuilder = app.builder
            tree = builder.assemble_doctree("index", arg)
            assert len(list(tree.findall(nodes.section))) == 3

        @pytest.mark.sphinx("typst", testroot="hidden-toctree")
        def test__exclude_hidden(self, app: SphinxTestApp):
            """Test to pass."""
            app.build()
            builder: t.TypstBuilder = app.builder
            tree = builder.assemble_doctree("index", "exclude_hidden")
            assert len(list(tree.findall(nodes.section))) == 1

        @pytest.mark.sphinx(
            "typst",
            testroot="root",
            confoverrides={
                "typst_documents": [
                    {
                        "entrypoint": "index",
                        "filename": "index",
                        "theme": "manual",
                        "font_set": "Noto Serif CJK JP",
                        "title": "Test documentation",
                    }
                ]
            },
        )
        def test__document_font(self, app: SphinxTestApp):
            """Test to pass."""
            app.build()
            out = app.outdir / "index.typ"
            assert '#set text(font: "Noto Serif CJK JP")' in out.read_text()


class Test_TypstPDFBuilder:
    class Test_assemble_doctree:
        @pytest.mark.sphinx(
            "typstpdf",
            testroot="root",
            confoverrides={
                "typst_font_paths": ["/tmp"],
            },
        )
        def test__additional_fonts(self, app: SphinxTestApp, mocker: MockFixture):
            """Test to pass."""
            import typst

            mocker.patch("typst.compile", return_value=None)
            spy = mocker.spy(typst, "compile")
            app.build()
            assert "font_paths" in spy.call_args.kwargs

    class Test_override_module:
        @pytest.mark.sphinx("typstpdf", testroot="override-typst-module")
        def test__document_font(self, app: SphinxTestApp):
            """Test to pass."""
            app.build()
            assert (app.outdir / "index.typ").exists()
            assert (app.outdir / "index.pdf").exists()
