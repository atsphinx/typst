"""Text styling elements.

These elements can be created by reStructuredText's standard syntax.

:ref: https://typst.app/docs/reference/text/
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from ._templating import env
from .base import Element

if TYPE_CHECKING:
    import jinja2


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
    """Code-block element.

    Currently, this element doesn't render as function style
    to control easily from Sphinx.

    :ref: https://typst.app/docs/reference/text/raw/
    """

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


class FunctionalText(Element):
    """Element base-class to render decorated text.

    This is for inline syntax.
    """

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
