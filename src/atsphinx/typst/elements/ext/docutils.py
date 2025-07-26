"""Custom elements for docutils nodes."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from ..base import Element


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
