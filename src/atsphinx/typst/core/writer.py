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

    ELEMENT_MAPPING: dict[str, type[nodes.Element]] = {
        "paragraph": elements.Paragraph,
        "title": elements.Heading,
        "section": elements.Section,
        "bullet_list": elements.BulletList,
        "field_list": elements.Table,
        "docinfo": elements.Table,
        "enumerated_list": elements.NumberedList,
        "emphasis": elements.Emphasis,
        "strong": elements.Strong,
        "block_quote": elements.Quote,
    }
    """Controls for mapping Typst elements and docutils nodes.

    If a node requires only to add element with empty content,
    you should add pair of node name and element class into this.
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.dom: elements.Document = elements.Document()
        self._ptr = self.dom
        self._indent_level = 0

    def _find_mepped_element(self, node) -> Optional[type[nodes.Element]]:
        for node_class in node.__class__.__mro__:
            if node_class.__name__ in self.ELEMENT_MAPPING:
                return self.ELEMENT_MAPPING[node_class.__name__]
        return None

    def unknown_visit(self, node: nodes.Node):
        element_class = self._find_mepped_element(node)
        if element_class is None:
            super().unknown_visit(node)
            return
        self._ptr = element_class(parent=self._ptr)

    def unknown_departure(self, node: nodes.Node):
        element_class = self._find_mepped_element(node)
        if element_class is None:
            super().unknown_departure(node)
            return
        self._move_ptr_to_parent()

    def _move_ptr_to_parent(self, node=None):
        self._ptr = self._ptr.parent

    def visit_raw(self, node: nodes.raw):
        if node.get("format") == "typst":
            elements.Source(node.astext(), parent=self._ptr)
        raise nodes.SkipNode()

    def visit_literal(self, node: nodes.raw):
        elements.Raw(node.astext(), parent=self._ptr)
        raise nodes.SkipNode()

    def visit_Text(self, node: nodes.Text):
        """Work about visit text content of node.

        This type should manage content value itself.
        """
        self._ptr = elements.Text(node.astext(), parent=self._ptr)

    depart_Text = _move_ptr_to_parent

    def visit_attribution(self, node: nodes.attribution):
        if isinstance(node.parent, nodes.block_quote):
            self._ptr.attribution = node.astext()
        raise nodes.SkipNode()
