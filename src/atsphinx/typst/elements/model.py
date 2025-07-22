"""Structure model elements.

:ref: https://typst.app/docs/reference/model/
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

import jinja2

from .base import Element

if TYPE_CHECKING:
    from typing import Optional


class Document(Element):
    """Document element."""

    LABEL = "document"
    TEMPLATE = """\
        {% for content in contents %}
        {{ content }}
        {% endfor %}
    """


class Section(Element):
    """Sphinx's section element."""

    LABEL = "section"
    TEMPLATE: str = """\
        {%- for content in contents -%}
        {{ content }}
        {% endfor %}
    """


class Heading(Element):
    """Section's heading element.

    :ref: https://typst.app/docs/reference/model/heading/
    """

    LABEL = "heading"
    TEMPLATE = """\
        #heading(
          level: {{level}},
          [
            {{content}}
            {%- if label %}
            #label("{{ label }}")
            {%- endif %}
          ]
        )
    """

    level: int = 0
    label: Optional[str] = None
    """RefID of document."""

    def to_text(self):
        content = self.children[0].to_text() if self.children else ""
        if self.level > 0:
            return self.get_template().render(
                level=self.level, content=content, label=self.label
            )
        return ""


class Paragraph(Element):
    """Paragraph of document."""

    LABEL = "par"
    TEMPLATE: str = """\
        {%- for content in contents -%}
        {{ content }}
        {%- endfor %}
    """


class List(Element):
    """Abstract element of list-type content."""

    TEMPLATE = """\
        {{ prefix }}{{ funcname }}(
          {%- for content, delimiter in contents %}
          {%- if not loop.first %}{{delimiter}}{% endif %}
          {{ content | indent(2, first=False) }}
          {%- endfor %}
        )
    """

    def to_text(self):
        """Render as Typst source.

        Typst must remove function symbol to use nested list.
        It replace ``+`` to join for parent.
        """
        prefix = "+" if isinstance(self.parent, List) else "#"
        contents = []
        for c in self.children:
            if isinstance(c, List):
                text = c.to_text()
                delimiter = ""
            else:
                text = jinja2.Template(
                    textwrap.dedent("""\
                    [
                      {{c|indent(2, first=False)}}
                    ]
                """).rstrip("\n")
                ).render(c=c.to_text())
                delimiter = ","
            contents.append((text, delimiter))
        return self.get_template().render(
            prefix=prefix, funcname=self.LABEL, contents=contents
        )


class BulletList(List):
    """Bullet list element.

    :ref: https://typst.app/docs/reference/model/list/
    """

    LABEL = "list"


class NumberedList(List):
    """Enumerated list element.

    :ref: https://typst.app/docs/reference/model/enum/
    """

    LABEL = "enum"


class Table(Element):
    """Table content element.

    .. note:: Currently, some elements use this if it is not table directive.

    .. todo:: This only renders simple style table, It should support thead design.

    :ref: https://typst.app/docs/reference/model/table/
    """

    LABEL = "table"
    TEMPLATE = """\
        #table(
          columns: {{ columns }},
          {%- for content in contents %}
          {%- if not loop.first %},{% endif %}
          [
            {{ content | indent(4, first=False) }}
          ]
          {%- endfor %}
        )
    """

    columns: int = 2

    def to_text(self):
        contents = [f"{c.to_text()}" for c in self.children]
        return self.get_template().render(contents=contents, columns=self.columns)


class Quote(Element):
    """Blockquote element.

    :ref: https://typst.app/docs/reference/model/quote/
    """

    LABEL = "quote"
    TEMPLATE = """\
        #quote(
          block: true,
          {%- if attribution %}
          attribution: [{{attribution}}],
          {%- endif %}
        )[
          {%- for content in contents %}
          {{ content | indent(2, first=False) }}
          {%- endfor %}
        ]
    """

    attribution: str = ""

    def to_text(self):
        return self.get_template().render(
            contents=[c.to_text() for c in self.children],
            attribution=self.attribution,
        )


class Field(Element):
    LABEL = "fiield"
    TEMPLATE = """\
        #sphinxField(
          [
            {{ title|indent(4, first=False) }}
          ],
          [
            {%- for content in contents %}
            {{ content | indent(4, first=False) }}
            {%- endfor %}
          ],
        )
    """

    def to_text(self):
        return self.get_template().render(
            title=self.children[0].to_text(),
            contents=[c.to_text() for c in self.children[1:]],
        )


class Figure(Element):
    """Component element included image and caption.

    :ref: https://typst.app/docs/reference/model/figure/
    """

    LABEL = "figure"
    TEMPLATE = """\
        #figure(
          {{ image|indent(2, first=False) }},
          {%- if caption %}
          caption: [
            {%- for content in caption %}
            {{ content | indent(4, first=False) }}
            {%- endfor %}
          ],
          {%- endif %}
        )
    """

    caption: Optional[str] = None

    def to_text(self):
        image = self.children[0].to_text()
        caption = []
        for idx, child in enumerate(self.children):
            if idx == 0:
                continue
            caption.append(child.to_text())
        return self.get_template().render(image=image, caption=caption)


class Link(Element):
    """Link to external website.

    :ref: https://typst.app/docs/reference/model/link/
    """

    LABEL = "link"
    TEMPLATE = """\
        #link(
          "{{ dest }}",
          [
            {{ content|indent(4, first=False) }}
          ],
        )
    """

    def __init__(
        self,
        uri: str,
        content: Optional[str] = None,
        parent=None,
        children=None,
        **kwargs,
    ):
        super().__init__(parent, children, **kwargs)
        self.uri = uri
        self.content = content or uri

    def to_text(self):
        return self.get_template().render(dest=self.uri, content=self.content)
