"""Writer and relative classes."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.logging import getLogger

from . import elements

if TYPE_CHECKING:
    from typing import Optional

    from sphinx.builders import Builder


logger = getLogger(__name__)


class TypstTranslator(SphinxTranslator):
    """Custom translator that has converter from dotctree to Typst syntax."""

    optional = [
        # TODO: Implement after for configure document itself.
        "document",
        # NOTE: Currently, these need not render anything.
        "description",
        "list_item",
        "field",
        "option_list_item",
        "option_group",
        "option",
        "colspec",
        "thead",
        "tbody",
        "row",
        "entry",
        "compound",
        "start_of_file",
    ]

    ELEMENT_MAPPING: dict[str, type[nodes.Element]] = {
        "paragraph": elements.Paragraph,
        "bullet_list": elements.BulletList,
        "field_list": elements.Element,
        "field": elements.Field,
        "field_name": elements.Element,
        "field_body": elements.Element,
        "option_list": elements.Table,
        "option_string": elements.Strong,
        "docinfo": elements.Element,
        "enumerated_list": elements.NumberedList,
        "emphasis": elements.Emphasis,
        "strong": elements.Strong,
        "block_quote": elements.Quote,
        "figure": elements.Figure,
    }
    """Controls for mapping Typst elements and docutils nodes.

    If a node requires only to add element with empty content,
    you should add pair of node name and element class into this.
    """

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.dom: elements.Document = elements.Document()
        self._ptr = self.dom
        # Set to avoid rendering root hedering text.
        self._section_level = -1
        self._targets: list[nodes.target] = []

    def _find_mepped_element(self, node) -> Optional[type[nodes.Element]]:
        """Find registed element mapped from node.

        :returns: Matched Element subclass. If it does not matche, return None.
        """
        for node_class in node.__class__.__mro__:
            if node_class.__name__ in self.ELEMENT_MAPPING:
                return self.ELEMENT_MAPPING[node_class.__name__]
        return None

    def _move_ptr_to_parent(self, node=None):
        """Move pointer for parent of current node.

        This method should be used to assign departure methods
        when only visit method require to define.
        """
        self._ptr = self._ptr.parent

    def unknown_visit(self, node: nodes.Node):
        """Handle visit methods for unregistered nodes.

        When node class has mapping for element class,
        it creates element object as child of current pointed node,
        and it moves pointer for created object.
        """
        element_class = self._find_mepped_element(node)
        if element_class is None:
            super().unknown_visit(node)
            return
        self._ptr = element_class(parent=self._ptr)

    def unknown_departure(self, node: nodes.Node):
        """Handle depart methods for unregistered nodes.

        When node class has mapping for element class,
        and it moves pointer for parent of current node.
        """
        element_class = self._find_mepped_element(node)
        if element_class is None:
            super().unknown_departure(node)
            return
        self._move_ptr_to_parent()

    def visit_raw(self, node: nodes.raw):
        if node.get("format") == "typst":
            elements.Source(node.astext(), parent=self._ptr)
        raise nodes.SkipNode()

    def visit_literal(self, node: nodes.raw):
        elements.Raw(node.astext(), parent=self._ptr)
        raise nodes.SkipNode()

    def visit_literal_block(self, node: nodes.raw):
        elements.RawBlock(node.astext(), node.get("language", None), parent=self._ptr)
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

    def visit_Admonition(self, node):
        msg = "Currently, admonition-like directive is not supported."
        logger.info(msg)
        raise nodes.SkipNode()

    def visit_image(self, node: nodes.image):
        elements.Image(
            node["uri"], node.get("width"), node.get("alt"), parent=self._ptr
        )
        raise nodes.SkipNode()

    def visit_caption(self, node: nodes.caption):
        if isinstance(self._ptr, elements.Figure):
            para = elements.Paragraph(parent=self._ptr)
            elements.Text(node.astext(), parent=para)
        raise nodes.SkipNode()

    def visit_legend(self, node: nodes.legend):
        pass

    def depart_legend(self, node: nodes.legend):
        pass

    def visit_table(self, node: nodes.table):
        self._ptr = elements.Table(parent=self._ptr)

    depart_table = _move_ptr_to_parent

    def visit_tgroup(self, node: nodes.tgroup):
        self._ptr.columns = int(node["cols"])

    def depart_tgroup(self, node):
        pass

    def visit_reference(self, node: nodes.reference):
        self._ptr = elements.Link(node["refuri"], node.astext(), parent=self._ptr)

    depart_reference = _move_ptr_to_parent

    def visit_target(self, node: nodes.target):
        node_idx = node.parent.children.index(node)  # type: ignore[possibily-unbound-attribute]
        if node_idx < 0:
            self._targets.append(node)
        elif isinstance(self._ptr.children[-1], elements.Heading):
            self._ptr.children[-1].label = node["refid"]
        raise nodes.SkipNode()

    def visit_title(self, node: nodes.title):
        self._ptr = elements.Heading(parent=self._ptr)
        self._ptr.level = self._section_level
        if self._targets:
            target = self._targets.pop()
            self._ptr.label = target["refid"]

    depart_title = _move_ptr_to_parent

    def visit_section(self, node: nodes.section):
        self._ptr = elements.Section(parent=self._ptr)
        self._section_level += 1

    def depart_section(self, node):
        self._move_ptr_to_parent()
        self._section_level -= 1
