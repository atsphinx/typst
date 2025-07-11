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
    from typing import ClassVar


def load_template(name: str) -> str:
    """Load template from class var.

    :param name: Class name to use as template.
    :returns: Template string.
    """
    module = sys.modules[load_template.__module__]
    if not hasattr(module, name):
        print(dir(module))
        raise Exception(f"{name} is not found.")
    return textwrap.dedent(getattr(module, name).TEMPLATE).strip("\n")


env = jinja2.Environment(loader=jinja2.FunctionLoader(load_template))
env.policies["json.dumps_kwargs"]["ensure_ascii"] = False


class Element(Node):
    LABEL: ClassVar[str] = ""
    TEMPLATE: ClassVar[str] = """\
        {%- for content in contents %}
        {{ content }}
        {%- endfor %}
    """

    def __init__(self, parent=None, children=None, **kwargs):
        super().__init__(self.LABEL, parent, children, **kwargs)

    @classmethod
    @lru_cache()
    def get_template(cls) -> jinja2.Template:
        return jinja2.Template(textwrap.dedent(cls.TEMPLATE).strip("\n"))

    def to_text(self):
        return self.get_template().render(contents=[c.to_text() for c in self.children])


class Source(Element):
    LABEL = "#raw"
    content: str

    def __init__(self, content: str, parent=None, children=None, **kwargs):
        super().__init__(parent, children, **kwargs)
        self.content = content

    def to_text(self):
        return self.content


class Text(Element):
    LABEL = "#text"
    content: str

    def __init__(self, content: str, parent=None, children=None, **kwargs):
        super().__init__(parent, children, **kwargs)
        self.content = content

    def to_text(self):
        return self.content


class Document(Element):
    LABEL = "document"
    TEMPLATE = """\
        {% for content in contents %}
        {{ content }}
        {% endfor %}
    """


class Section(Element):
    LABEL = "section"
    TEMPLATE: str = """\
        {%- for content in contents -%}
        {{ content }}
        {%- endfor %}
    """


class Heading(Element):
    LABEL = "heading"
    TEMPLATE = """\
        #heading(
          level: {{level}},
          [{{content}}]
        )
    """

    def to_text(self):
        content = self.children[0].to_text() if self.children else ""
        return self.get_template().render(level=self.depth, content=content)


class Paragraph(Element):
    LABEL = "par"
    TEMPLATE: str = """\
        {%- for content in contents -%}
        {{ content }}
        {%- endfor %}
    """


class List(Element):
    TEMPLATE = """\
        {{ prefix }}{{ funcname }}(
          {%- for content, delimiter in contents %}
          {%- if not loop.first %}{{delimiter}}{% endif %}
          {{ content | indent(2, first=False) }}
          {%- endfor %}
        )
    """

    def to_text(self):
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
    LABEL = "list"


class NumberedList(List):
    LABEL = "enum"


class Table(Element):
    LABEL = "table"
    TEMPLATE = """\
        #table(
          columns: 2,
          {%- for content in contents %}
          {%- if not loop.first %},{% endif %}
          [
            {{ content | indent(4, first=False) }}
          ]
          {%- endfor %}
        )
    """

    def to_text(self):
        contents = [f"{c.to_text()}" for c in self.children]
        return self.get_template().render(contents=contents)


class Raw(Element):
    TEMPLATE = """\
        #raw(
          {{ content|tojson }}
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


class Quote(Element):
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
    LABEL = "emph"


class Strong(FunctionalText):
    LABEL = "strong"
