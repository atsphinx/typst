"""Custom elements for docutils nodes."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from ..base import Element


class Admonition(Element):
    LABEL = "admonition"
    TEMPLATE = """\
        #docutils.admonition(
          "{{ title }}",
          [
            {%- for content in contents %}
            {{ content | indent(4, first=False) }}
            {%- endfor %}
          ],
        )
    """

    title: str

    def to_text(self):
        return self.get_template().render(
            title=self.title,
            contents=[c.to_text() for c in self.children],
        )


class Field(Element):
    LABEL = "fiield"
    TEMPLATE = """\
        #docutils.field(
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


class Section(Element):
    """Sphinx's section element."""

    LABEL = "section"
    TEMPLATE: str = """\
        {%- for content in contents -%}
        {{ content }}
        {% endfor %}
    """
