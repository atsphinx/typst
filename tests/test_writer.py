"""Writer and relative classes."""

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

import pytest
from docutils.core import publish_doctree

from atsphinx.typst import writer as t

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
  [
    Title
  ]
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
  [
    Title
  ]
)

Paragraph

#heading(
  level: 2,
  [
    Section 1
  ]
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
#sphinxField(
  [
    Language
  ],
  [
    Japanese
  ],
)#sphinxField(
  [
    Language2
  ],
  [
    English
  ],
)#sphinxField(
  [
    Description
  ],
  [
    Hello world
    This is atsphinx-typst.
  ],
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

#sphinxField(
  [
    Language
  ],
  [
    Japanese
  ],
)
    """,
            id="Field list",
        ),
        pytest.param(
            """
Paragraph

-h  Help
-v  Show version
""",
            """
Paragraph

#table(
  columns: 2,
  [
    #strong[
      -h
    ]
  ],
  [
    Help
  ],
  [
    #strong[
      -v
    ]
  ],
  [
    Show version
  ]
)
    """,
            id="Option list",
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
``print("テスト")``
""",
            """
#raw(
  "print(\\"テスト\\")"
)
""",
            id="inline raw code",
        ),
        pytest.param(
            """
This is an ordinary paragraph, introducing a block quote.

    "It is my business to know things.  That is my trade."
""",
            """
This is an ordinary paragraph, introducing a block quote.

#quote(
  block: true,
)[
  "It is my business to know things.  That is my trade."
]
""",
            id="block quote",
        ),
        pytest.param(
            """
This is an ordinary paragraph, introducing a block quote.

    "It is my business to know things.  That is my trade."

    -- Sherlock Holmes
""",
            """
This is an ordinary paragraph, introducing a block quote.

#quote(
  block: true,
  attribution: [Sherlock Holmes],
)[
  "It is my business to know things.  That is my trade."
]
""",
            id="block quote with attribution",
        ),
        pytest.param(
            """
.. code:: python

    print("テスト")
    print("Hello")
""",
            """
```python
print(\"テスト\")
print(\"Hello\")
```
""",
            id="block raw code",
        ),
        pytest.param(
            """
.. hint:: Hello

.. warning:: world
""",
            """
""",
            id="Admonitions",
        ),
        pytest.param(
            """
.. image:: ./example.jpg
""",
            """
#image(
  "./example.jpg",
)
""",
            id="Simple image",
        ),
        pytest.param(
            """
.. image:: ./example.jpg
    :width: 50%
    :alt: Sample
""",
            """
#image(
  "./example.jpg",
  width: 50%,
  alt: "Sample",
)
""",
            id="Image with attributes",
        ),
        pytest.param(
            """
.. figure:: ./example.jpg
""",
            """
#figure(
  #image(
    "./example.jpg",
  ),
)
""",
            id="Simple figure",
        ),
        pytest.param(
            """
.. figure:: ./example.jpg

    This is sample.
""",
            """
#figure(
  #image(
    "./example.jpg",
  ),
  caption: [
    This is sample.
  ],
)
""",
            id="Figure with caption",
        ),
        pytest.param(
            """
.. figure:: ./example.jpg

    This is sample.

    Support multiline.
""",
            # NOTE: It removes blank line between caption and legend.
            """
#figure(
  #image(
    "./example.jpg",
  ),
  caption: [
    This is sample.
    Support multiline.
  ],
)
""",
            id="Figure with caption",
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
    visitor._section_level = 1
    document.walkabout(visitor)
    print(RenderTree(visitor.dom))
    assert visitor.dom.to_text().strip() == dest.strip()


@pytest.mark.parametrize(
    "src",
    [
        pytest.param(
            """
== ==== ========
ID Name Note
== ==== ========
1  Tom  Engineer
== ==== ========
""",
            id="Simple table",
        ),
        pytest.param(
            """
+--+----+--------+
|ID|Name|Note    |
+==+====+========+
|1 |Tom |Engineer|
+--+----+--------+
""",
            id="Grid table",
        ),
        pytest.param(
            """
.. csv-table::
    :header: ID,Name,Note

    1,Tom,Engineer
""",
            id="CSV table",
        ),
        pytest.param(
            """
.. list-table::

    * - ID
      - Name
      - Note
    * - 1
      - Tom
      - Engineer
""",
            id="List table",
        ),
    ],
)
def test_table_syntax(app: SphinxTestApp, src: str):
    dest = """
#table(
  columns: 3,
  [
    ID
  ],
  [
    Name
  ],
  [
    Note
  ],
  [
    1
  ],
  [
    Tom
  ],
  [
    Engineer
  ]
)
"""
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


@pytest.mark.parametrize(
    "src,dest",
    [
        pytest.param(
            """
http://example.com
""",
            """
#link(
  "http://example.com",
  [
    http://example.com
  ],
)
""",
        ),
        pytest.param(
            """
`Here <http://example.com>`_
""",
            """
#link(
  "http://example.com",
  [
    Here
  ],
)
""",
        ),
        pytest.param(
            """
`a link`_

.. _a link: http://example.com/
""",
            """
#link(
  "http://example.com/",
  [
    a link
  ],
)
""",
        ),
        pytest.param(
            """
.. _my-reference-label:

Section to cross-reference
--------------------------
""",
            """
#heading(
  level: 1,
  [
    Section to cross-reference
    #label("my-reference-label")
  ]
)
""",
        ),
    ],
)
def test_reference(app: SphinxTestApp, src: str, dest: str):
    # NOTE: Keep debugging print
    from anytree import RenderTree

    """Very simple test for syntax by Translator."""
    document = publish_doctree(src.strip())
    print(document)
    visitor = t.TypstTranslator(document, app.builder)
    visitor._section_level = 1
    document.walkabout(visitor)
    print(RenderTree(visitor.dom))
    assert visitor.dom.to_text().strip() == dest.strip()


def test_raw_typst_source(app: SphinxTestApp):
    src = """
        .. raw:: typst

            #heading([Hello])
        """
    document = publish_doctree(textwrap.dedent(src))
    visitor = t.TypstTranslator(document, app.builder)
    dest = """
        #heading([Hello])

        """
    document.walkabout(visitor)
    assert visitor.dom.to_text() == textwrap.dedent(dest)


def test_raw_not_typst_source(app: SphinxTestApp):
    src = """
        .. raw:: python

            print("hello")
        """
    document = publish_doctree(textwrap.dedent(src))
    visitor = t.TypstTranslator(document, app.builder)
    document.walkabout(visitor)
    assert visitor.dom.to_text() == textwrap.dedent("")
