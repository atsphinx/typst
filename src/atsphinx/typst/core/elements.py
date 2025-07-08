"""Classes for Typst elements.

Elements is tree style object and have ``to_text`` method to render document.
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

import textwrap
from functools import lru_cache

import jinja2
from anytree import Node


class Text(Node):
    def to_text(self):
        return self.name


class Element(Node):
    LABEL: str = ""
    TEMPLATE: str = """\
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
        print(self.TEMPLATE)
        print(self.get_template())
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
