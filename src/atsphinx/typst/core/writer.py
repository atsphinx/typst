"""Writer and relative classes."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.util.docutils import SphinxTranslator

from . import elements

if TYPE_CHECKING:
    from typing import Callable, Optional, Tuple

    from sphinx.builders import Builder


class TypstTranslator(SphinxTranslator):
    """Custom translator that has converter from dotctree to Typst syntax."""

    ELEMENT_MAPPING = {
        "emphasis": (elements.Emphasis, True),
        "strong": (elements.Strong, True),
    }

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.dom: elements.Document = elements.Document()
        self._ptr = self.dom
        self._indent_level = 0

    def _find_mepped_element(
        self, node
    ) -> Optional[Tuple[Callable[..., nodes.Element], bool]]:
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

    # TODO: Implement after
    visit_document = _not_proc
    depart_document = _not_proc

    def visit_section(self, node: nodes.section):
        self._ptr = elements.Section(parent=self._ptr)

    depart_section = _move_ptr_to_parent

    def visit_Text(self, node: nodes.Text):
        self._ptr = elements.Text(node.astext(), parent=self._ptr)

    depart_Text = _move_ptr_to_parent

    def visit_title(self, node: nodes.title):
        self._ptr = elements.Heading(parent=self._ptr)

    depart_title = _move_ptr_to_parent

    def visit_paragraph(self, node: nodes.paragraph):
        self._ptr = elements.Paragraph(parent=self._ptr)

    depart_paragraph = _move_ptr_to_parent

    def visit_bullet_list(self, node: nodes.bullet_list):
        self._ptr = elements.BulletList(parent=self._ptr)

    depart_bullet_list = _move_ptr_to_parent

    def visit_enumerated_list(self, node: nodes.enumerated_list):
        self._ptr = elements.NumberedList(parent=self._ptr)

    depart_enumerated_list = _move_ptr_to_parent

    visit_list_item = _not_proc
    depart_list_item = _not_proc

    def visit_field_list(self, node: nodes.field_list):
        self._ptr = elements.Table(parent=self._ptr)

    depart_field_list = _move_ptr_to_parent

    visit_field = _not_proc
    depart_field = _not_proc
    visit_field_name = _not_proc
    depart_field_name = _not_proc
    visit_field_body = _not_proc
    depart_field_body = _not_proc

    def visit_docinfo(self, node: nodes.docinfo):
        self._ptr = elements.Table(parent=self._ptr)

    depart_docinfo = _move_ptr_to_parent
