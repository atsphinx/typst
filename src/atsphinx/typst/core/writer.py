"""Writer and relative classes."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.util.docutils import SphinxTranslator

from . import elements

if TYPE_CHECKING:
    from sphinx.builders import Builder


class TypstTranslator(SphinxTranslator):
    """Custom translator that has converter from dotctree to Typst syntax."""

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.dom: elements.Document = elements.Document()
        self._ptr = self.dom
        self._indent_level = 0

    def _not_proc(self, node):
        pass

    def _move_ptr_to_parent(self, node):
        self._ptr = self._ptr.parent

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
