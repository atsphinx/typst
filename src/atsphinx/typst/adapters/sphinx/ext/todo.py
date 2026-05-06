# noqa: D100
from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.ext.todo import todo_node

from atsphinx.typst.writer import TypstTranslator

if TYPE_CHECKING:
    from sphinx.application import Sphinx

# NOTE: Base behavior is implemented the same way as docutils' admonitions.
_visit_todo_node, _depart_todo_node = TypstTranslator._enclose_admonition(
    "todo_node",
)


def visit_todo_node(self: TypstTranslator, node: todo_node):  # noqa: D103
    if self.config.todo_include_todos:
        _visit_todo_node(self, node)
    else:
        raise nodes.SkipNode


def depart_todo_node(self: TypstTranslator, node: todo_node):  # noqa: D103
    if self.config.todo_include_todos:
        _depart_todo_node(self, node)


def setup(app: Sphinx):  # noqa: D103
    app.registry.add_translation_handlers(
        todo_node,
        typst=(visit_todo_node, depart_todo_node),
    )
