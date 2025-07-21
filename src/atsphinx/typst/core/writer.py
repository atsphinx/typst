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
    from collections.abc import Callable

    from sphinx.builders import Builder


logger = getLogger(__name__)


def _append_child_element(
    element_class: type[elements.Element],
) -> Callable[[TypstTranslator, nodes.Node], None]:
    """Descriptor to bind method for 'appending element as child'.

    This has two features.

    1. it creates argumented element as child of current pointer.
    2. it move pointer from parent to it.
    """

    def __append_child_element(self: TypstTranslator, node: nodes.Node) -> None:
        self._ptr = element_class(parent=self._ptr)

    return __append_child_element


class TypstTranslator(SphinxTranslator):
    """Custom translator that has converter from dotctree to Typst syntax.

    This defines visit/departuer methods in order to:

    1. Text node of docutils.
    2. Dependents (docutils, sphinx, and others ...)
    3. Alphabet ascending

    :ref: https://docutils.sourceforge.io/docs/ref/doctree.html
    """

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

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.dom: elements.Document = elements.Document()
        self._ptr = self.dom
        # Set to avoid rendering root hedering text.
        self._section_level = -1
        self._targets: list[nodes.target] = []

    def _move_ptr_to_parent(self, node=None):
        """Move pointer for parent of current node.

        This method should be used to assign departure methods
        when only visit method require to define.
        """
        self._ptr = self._ptr.parent

    # ------
    # visit/departuer methods
    # ------

    # : docutils

    def visit_Text(self, node: nodes.Text):
        """Work about visit text content of node.

        This type should manage content value itself.
        """
        self._ptr = elements.Text(node.astext(), parent=self._ptr)

    depart_Text = _move_ptr_to_parent

    def visit_Admonition(self, node):
        msg = "Currently, admonition-like directive is not supported."
        logger.info(msg)
        raise nodes.SkipNode()

    def visit_attribution(self, node: nodes.attribution):
        if isinstance(node.parent, nodes.block_quote):
            self._ptr.attribution = node.astext()
        raise nodes.SkipNode()

    visit_block_quote = _append_child_element(elements.Quote)

    depart_block_quote = _move_ptr_to_parent

    visit_bullet_list = _append_child_element(elements.BulletList)

    depart_bullet_list = _move_ptr_to_parent

    def visit_caption(self, node: nodes.caption):
        if isinstance(self._ptr, elements.Figure):
            para = elements.Paragraph(parent=self._ptr)
            elements.Text(node.astext(), parent=para)
        raise nodes.SkipNode()

    visit_docinfo = _append_child_element(elements.Element)

    depart_docinfo = _move_ptr_to_parent

    visit_emphasis = _append_child_element(elements.Emphasis)

    depart_emphasis = _move_ptr_to_parent

    visit_enumerated_list = _append_child_element(elements.NumberedList)

    depart_enumerated_list = _move_ptr_to_parent

    visit_field = _append_child_element(elements.Field)

    depart_field = _move_ptr_to_parent

    visit_field_body = _append_child_element(elements.Element)

    depart_field_body = _move_ptr_to_parent

    visit_field_list = _append_child_element(elements.Element)

    depart_field_list = _move_ptr_to_parent

    visit_field_name = _append_child_element(elements.Element)

    depart_field_name = _move_ptr_to_parent

    visit_figure = _append_child_element(elements.Figure)

    depart_figure = _move_ptr_to_parent

    def visit_image(self, node: nodes.image):
        elements.Image(
            node["uri"], node.get("width"), node.get("alt"), parent=self._ptr
        )
        raise nodes.SkipNode()

    def visit_legend(self, node: nodes.legend):
        pass

    def depart_legend(self, node: nodes.legend):
        pass

    def visit_literal(self, node: nodes.raw):
        elements.Raw(node.astext(), parent=self._ptr)
        raise nodes.SkipNode()

    def visit_literal_block(self, node: nodes.raw):
        elements.RawBlock(node.astext(), node.get("language", None), parent=self._ptr)
        raise nodes.SkipNode()

    visit_option_list = _append_child_element(elements.Table)

    depart_option_list = _move_ptr_to_parent

    visit_option_string = _append_child_element(elements.Strong)

    depart_option_string = _move_ptr_to_parent

    visit_paragraph = _append_child_element(elements.Paragraph)

    depart_paragraph = _move_ptr_to_parent

    def visit_raw(self, node: nodes.raw):
        if node.get("format") == "typst":
            elements.Source(node.astext(), parent=self._ptr)
        raise nodes.SkipNode()

    def visit_reference(self, node: nodes.reference):
        self._ptr = elements.Link(node["refuri"], node.astext(), parent=self._ptr)

    depart_reference = _move_ptr_to_parent

    def visit_section(self, node: nodes.section):
        self._ptr = elements.Section(parent=self._ptr)
        self._section_level += 1

    def depart_section(self, node):
        self._move_ptr_to_parent()
        self._section_level -= 1

    visit_strong = _append_child_element(elements.Strong)

    depart_strong = _move_ptr_to_parent

    def visit_table(self, node: nodes.table):
        self._ptr = elements.Table(parent=self._ptr)

    depart_table = _move_ptr_to_parent

    def visit_target(self, node: nodes.target):
        node_idx = node.parent.children.index(node)  # type: ignore[possibily-unbound-attribute]
        if node_idx < 0:
            self._targets.append(node)
        elif isinstance(self._ptr.children[-1], elements.Heading):
            self._ptr.children[-1].label = node["refid"]
        raise nodes.SkipNode()

    def visit_tgroup(self, node: nodes.tgroup):
        self._ptr.columns = int(node["cols"])

    def depart_tgroup(self, node):
        pass

    def visit_title(self, node: nodes.title):
        self._ptr = elements.Heading(parent=self._ptr)
        self._ptr.level = self._section_level
        if self._targets:
            target = self._targets.pop()
            self._ptr.label = target["refid"]

    depart_title = _move_ptr_to_parent
