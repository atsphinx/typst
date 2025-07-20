"""Base and essential elements."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

import textwrap
from functools import lru_cache
from typing import TYPE_CHECKING

import jinja2
from anytree import Node

if TYPE_CHECKING:
    from typing import ClassVar


class Element(Node):
    """Abstract of all elements.

    This defines common methods and class vars.
    """

    LABEL: ClassVar[str] = ""
    """Name to show as anytree node."""
    TEMPLATE: ClassVar[str] = """\
        {%- for content in contents -%}
        {{ content }}
        {%- endfor -%}
    """
    """Template string when ``to_text`` runs."""

    def __init__(self, parent=None, children=None, **kwargs):
        """Set ``cls.LABEL`` for node name of anytree when it is created."""
        super().__init__(self.LABEL, parent, children, **kwargs)

    @classmethod
    @lru_cache()
    def get_template(cls) -> jinja2.Template:
        """Create template object from class vars."""
        return jinja2.Template(textwrap.dedent(cls.TEMPLATE).lstrip("\n"))

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
        return self.content + "\n"


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
