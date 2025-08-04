# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D106, D107
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from docutils import nodes

from atsphinx.typst import builders as t

if TYPE_CHECKING:
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
