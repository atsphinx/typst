"""Drawing elements.

:ref: https://typst.app/docs/reference/visualize/
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import Element

if TYPE_CHECKING:
    from typing import Optional


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
