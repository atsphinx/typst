"""Writer and relative classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from docutils.core import publish_doctree

from atsphinx.typst.core import writer as t

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("typst")
@pytest.mark.parametrize(
    "src,dest",
    [
        pytest.param(
            """
Title
=====
    """,
            """
= Title
    """,
            id="Single heading",
        ),
        pytest.param(
            """
Title
=====

Paragraph

Section 1
---------
    """,
            """
= Title

Paragraph

== Section 1
    """,
            id="Heading with paragraph",
        ),
        pytest.param(
            """
* Item A
* Item B
    """,
            """
- Item A
- Item B
    """,
            id="Bullet list",
        ),
        pytest.param(
            """
* Item A
  Next line
* Item B
    """,
            r"""
- Item A
  Next line
- Item B
    """,
            id="Bullet list with line break",
        ),
        pytest.param(
            """
* Item A

  * Sub item A
  * Sub item B

* Item B
    """,
            """
- Item A
  - Sub item A
  - Sub item B
- Item B
    """,
            id="Bullet list with nested",
        ),
        pytest.param(
            """
#. Item A
#. Item B
    """,
            """
+ Item A
+ Item B
    """,
            id="Enumerated list",
        ),
    ],
)
def test_syntax(app: SphinxTestApp, src: str, dest: str):
    """Very simple test for syntax by Translator."""
    document = publish_doctree(src.strip())
    document.settings.strict_visitor = False
    visitor = t.TypstTranslator(document, app.builder)
    document.walkabout(visitor)
    assert visitor.dom.to_text().strip() == dest.strip()
