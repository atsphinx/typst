"""Classes for Typst elements.

Elements is tree style object and have ``to_text`` method to render document.
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

import sys
import textwrap
from functools import lru_cache
from typing import TYPE_CHECKING

import jinja2
from anytree import Node

if TYPE_CHECKING:
    from typing import ClassVar, Optional


def load_template(name: str) -> str:
    """Load template from class var.

    :param name: Class name to use as template.
    :returns: Template string.
    """
    module = sys.modules[load_template.__module__]
    if not hasattr(module, name):
        raise Exception(f"{name} is not found.")
    return textwrap.dedent(getattr(module, name).TEMPLATE).strip("\n")


env = jinja2.Environment(loader=jinja2.FunctionLoader(load_template))
env.policies["json.dumps_kwargs"]["ensure_ascii"] = False


class Element(Node):
    """Abstract of all elements.

    This defines common methods and class vars.
    """

    LABEL: ClassVar[str] = ""
    TEMPLATE: ClassVar[str] = """\
        {%- for content in contents %}
        {{ content }}
        {%- endfor %}
    """
    """Template string when ``to_text`` runs."""

    def __init__(self, parent=None, children=None, **kwargs):
        """Set ``cls.LABEL`` for node name of anytree when it is created."""
        super().__init__(self.LABEL, parent, children, **kwargs)

    @classmethod
    @lru_cache()
    def get_template(cls) -> jinja2.Template:
        """Create template object from class vars."""
        return jinja2.Template(textwrap.dedent(cls.TEMPLATE).strip("\n"))

    def to_text(self):
        """Convert from element to Typst source."""
        return self.get_template().render(contents=[c.to_text() for c in self.children])


class Source(Element):
    """Raw Typst source (It is not Typst's ``raw`` element!).

    This is from Sphinx ``raw`` directive, and it is used to set Typst customize.
    """

    LABEL = "#raw"

    content: str
    """Content to insert into source."""

    def __init__(self, content: str, parent=None, children=None, **kwargs):
        super().__init__(parent, children, **kwargs)
        self.content = content

    def to_text(self):
        return self.content


class Text(Element):
    """Plain text element."""

    LABEL = "#text"

    content: str
    """Text content itself."""

    def __init__(self, content: str, parent=None, children=None, **kwargs):
        super().__init__(parent, children, **kwargs)
        self.content = content

    def to_text(self):
        return self.content


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
        {%- endfor %}
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

    label: Optional[str] = None
    """RefID of document."""

    def to_text(self):
        content = self.children[0].to_text() if self.children else ""
        return self.get_template().render(
            level=self.depth, content=content, label=self.label
        )


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


class Raw(Element):
    """Inline highlighting element.

    :ref: https://typst.app/docs/reference/text/raw/
    """

    TEMPLATE = """\
        #raw(
          {{ content|tojson|indent(2, first=False)}}
        )
    """

    content: str

    def __init__(self, content: str, parent=None, children=None, **kwargs):
        super().__init__(parent, children, **kwargs)
        self.content = content

    @classmethod
    @lru_cache()
    def get_template(cls) -> jinja2.Template:
        # Override to work 'ensure_ascii' settings by tojson.
        return env.get_template("Raw")

    def to_text(self):
        return self.get_template().render(content=self.content)


class RawBlock(Element):
    """Code-block element."""

    TEMPLATE = """\
        ```{{lang}}
        {{content}}
        ```
    """

    content: str
    lang: str
    """Highlighting language."""

    def __init__(self, content: str, lang: str, parent=None, children=None, **kwargs):
        super().__init__(parent, children, **kwargs)
        self.content = content
        self.lang = lang

    def to_text(self):
        return self.get_template().render(content=self.content, lang=self.lang)


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


class FunctionalText(Element):
    """Element base-class to render decorated text."""

    TEMPLATE = """\
        #{{label}}[
          {%- for content in contents %}
          {{ content | indent(2, first=False) }}
          {%- endfor %}
        ]
    """

    def to_text(self):
        return self.get_template().render(
            label=self.LABEL, contents=[c.to_text() for c in self.children]
        )


class Emphasis(FunctionalText):
    """Emphasized text.

    :ref: https://typst.app/docs/reference/model/emph/
    """

    LABEL = "emph"


class Strong(FunctionalText):
    """Strong emphasized text.

    :ref: https://typst.app/docs/reference/model/strong/
    """

    LABEL = "strong"


class Image(Element):
    """Embedding image.

    :ref: https://typst.app/docs/reference/visualize/image/
    """

    LABEL = "image"
    TEMPLATE = """\
        #image(
          "{{ elm.uri }}",
          {%- if elm.width %}
          width: {{ elm.width }},
          {%- endif %}
          {%- if elm.alt %}
          alt: "{{ elm.alt }}",
          {%- endif %}
        )
    """

    uri: str
    width: Optional[str]
    alt: Optional[str]

    def __init__(
        self,
        uri: str,
        width: Optional[str] = None,
        alt: Optional[str] = None,
        parent=None,
        children=None,
        **kwargs,
    ):
        super().__init__(parent, children, **kwargs)
        self.uri = uri
        self.width = width
        self.alt = alt

    def to_text(self):
        return self.get_template().render(elm=self)


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
        self.content = content

    def to_text(self):
        return self.get_template().render(dest=self.uri, content=self.content)
