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
Paragraph.
""",
            """
Paragraph.
""",
            id="Single paragraph",
        ),
        pytest.param(
            """
This is paragraph 1.
That is too.
    """,
            """
This is paragraph 1.
That is too.
    """,
            id="Multiline paragraph",
        ),
        pytest.param(
            """
This is paragraph 1.

That is paragraph 2.
    """,
            """
This is paragraph 1.

That is paragraph 2.
    """,
            id="Multiple paragraph",
        ),
        pytest.param(
            """
Title
=====
    """,
            """
#heading(
  level: 1,
  [Title]
)
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
#heading(
  level: 1,
  [Title]
)

Paragraph

#heading(
  level: 2,
  [Section 1]
)
    """,
            id="Heading with paragraph",
        ),
        pytest.param(
            """
* Item A
* Item B
    """,
            """
#list(
  [
    Item A
  ],
  [
    Item B
  ]
)
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
#list(
  [
    Item A
    Next line
  ],
  [
    Item B
  ]
)
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
#list(
  [
    Item A
  ]
  +list(
    [
      Sub item A
    ],
    [
      Sub item B
    ]
  ),
  [
    Item B
  ]
)
    """,
            id="Bullet list with nested",
        ),
        pytest.param(
            """
* Item A

  #. Sub item A
  #. Sub item B

* Item B
    """,
            """
#list(
  [
    Item A
  ]
  +enum(
    [
      Sub item A
    ],
    [
      Sub item B
    ]
  ),
  [
    Item B
  ]
)
    """,
            id="Bullet list with nested numberd list",
        ),
        pytest.param(
            """
#. Item A
#. Item B
    """,
            """
#enum(
  [
    Item A
  ],
  [
    Item B
  ]
)
    """,
            id="Enumerated list",
        ),
        pytest.param(
            """
:Language: Japanese
:Language2: English
:Description: Hello world
              This is atsphinx-typst.
""",
            """
#table(
  columns: 2,
  [
    Language
  ],
  [
    Japanese
  ],
  [
    Language2
  ],
  [
    English
  ],
  [
    Description
  ],
  [
    Hello world
    This is atsphinx-typst.
  ]
)
    """,
            id="Docinfo",
        ),
        pytest.param(
            """
Paragraph

:Language: Japanese
""",
            """
Paragraph

#table(
  columns: 2,
  [
    Language
  ],
  [
    Japanese
  ]
)
    """,
            id="Field list",
        ),
        pytest.param(
            """
*Content*
""",
            """
#emph[
  Content
]
    """,
            id="Emphasizes content",
        ),
        pytest.param(
            """
**Content**
""",
            """
#strong[
  Content
]
    """,
            id="strong content",
        ),
        pytest.param(
            """
This *is* **content**
""",
            """
This #emph[
  is
] #strong[
  content
]
    """,
            id="strong content",
        ),
        pytest.param(
            """
.. raw:: typst

    #heading([Hello])
""",
            """
#heading([Hello])
    """,
            id="raw typst source",
        ),
        pytest.param(
            """
.. raw:: python

    print("hello")
""",
            """
    """,
            id="raw other source",
        ),
        pytest.param(
            """
``print("テスト")``
""",
            """
#raw(
  "print(\\"テスト\\")"
)
""",
            id="inline raw code",
        ),
    ],
)
def test_syntax(app: SphinxTestApp, src: str, dest: str):
    # NOTE: Keep debugging print
    from anytree import RenderTree

    """Very simple test for syntax by Translator."""
    document = publish_doctree(src.strip())
    print(document)
    document.settings.strict_visitor = False
    visitor = t.TypstTranslator(document, app.builder)
    document.walkabout(visitor)
    print(RenderTree(visitor.dom))
    assert visitor.dom.to_text().strip() == dest.strip()
