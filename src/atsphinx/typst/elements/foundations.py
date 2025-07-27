"""Foundation elements.

:ref: https://typst.app/docs/reference/foundations/
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from .base import Element


class Label(Element):
    """Label for element.

    :ref: https://typst.app/docs/reference/foundations/label/
    """

    LABEL = "label"
    TEMPLATE = """\
        {% if defined %} #{% endif %}label("{{ refid }}")
    """

    refid: str

    def __init__(
        self, refid: str, defined: bool = False, parent=None, children=None, **kwargs
    ):
        super().__init__(parent, children, **kwargs)
        self.refid = refid
        self.defined = defined

    def to_text(self):
        return self.get_template().render(
            defined=self.defined,
            refid=self.refid,
        )
