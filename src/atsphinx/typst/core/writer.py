"""Writer and relative classes."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.util.docutils import SphinxTranslator

from . import elements

if TYPE_CHECKING:
    from typing import Optional

    from sphinx.builders import Builder


class TypstTranslator(SphinxTranslator):
    """Custom translator that has converter from dotctree to Typst syntax."""

    optional = [
        # TODO: Implement after for configure document itself.
        "document",
        # NOTE: Currently, these need not render anything.
        "list_item",
        "field",
        "field_name",
        "field_body",
    ]

    ELEMENT_MAPPING: dict[str, Optional[tuple[type[nodes.Element], bool]]] = {
        "paragraph": (elements.Paragraph, True),
        "title": (elements.Heading, True),
        "section": (elements.Section, True),
        "bullet_list": (elements.BulletList, True),
        "field_list": (elements.Table, True),
        "docinfo": (elements.Table, True),
        "enumerated_list": (elements.NumberedList, True),
        "emphasis": (elements.Emphasis, True),
        "strong": (elements.Strong, True),
    }
    """Controls for mapping Typst elements and docutils nodes.

    If a node class need not work as element, value of dict must be ``None``.

    If a node class requires element, value of dict must be these tuple.

    1. First value is class of element.
    2. Second value is boolean that is required nest.
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.dom: elements.Document = elements.Document()
        self._ptr = self.dom
        self._indent_level = 0

    def _find_mepped_element(self, node) -> Optional[tuple[type[nodes.Element], bool]]:
        for node_class in node.__class__.__mro__:
            if node_class.__name__ in self.ELEMENT_MAPPING:
                return self.ELEMENT_MAPPING[node_class.__name__]
        return None

    def unknown_visit(self, node: nodes.Node):
        map = self._find_mepped_element(node)
        if map is None:
            super().unknown_visit(node)
            return
        elm_class, move_ptr = map
        elm = elm_class(parent=self._ptr)
        if move_ptr:
            self._ptr = elm

    def unknown_departure(self, node: nodes.Node):
        map = self._find_mepped_element(node)
        if map is None:
            super().unknown_departure(node)
            return
        elm_class, move_ptr = map
        if move_ptr:
            self._ptr = self._ptr.parent

    def _not_proc(self, node):
        pass

    def _move_ptr_to_parent(self, node):
        self._ptr = self._ptr.parent

    def _add_node(self, node):
        pass

    def visit_Text(self, node: nodes.Text):
        self._ptr = elements.Text(node.astext(), parent=self._ptr)

    depart_Text = _move_ptr_to_parent
