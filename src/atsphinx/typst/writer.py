"""Writer and relative classes.

Order of definitions.

1. Write about docutils elements.
   They are declared in order to
   `Element Reference <https://docutils.sourceforge.io/docs/ref/doctree.html#element-reference>`_.
2. Write about Spinx elements.
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

from importlib import metadata
from pathlib import Path
from typing import TYPE_CHECKING

from docutils import nodes
from rst2typst.writer import TypstTranslator as BaseTypstTranslator
from sphinx import addnodes
from sphinx.util.docutils import SphinxTranslator
from sphinx.util.index_entries import split_index_msg
from sphinx.util.logging import getLogger

if TYPE_CHECKING:
    from sphinx.builders import Builder


logger = getLogger(__name__)


# TODO: It should be defined in rst2typst.
def _typst_local_package_fullname(name: str, version: str | None = None) -> str:
    if version is None:
        version = metadata.version(name)
    return f"@local/{name}:{version}"


class TypstTranslator(SphinxTranslator, BaseTypstTranslator):
    """Custom translator that has converter from dotctree to Typst syntax."""

    optional = [
        # Sphinx's nodes
        "desc_signature",
        "legend",
        "pending_xref",
    ]

    def __init__(self, document: nodes.document, builder: Builder) -> None:
        super().__init__(document, builder)
        super(BaseTypstTranslator, self).__init__(document)
        # Set to avoid rendering root hedering text.
        self._section_level = -1
        self.document.settings.no_import_local_package = False
        self.context = {
            "has_index": False,
        }

    # ------
    # visit/departuer methods
    # ------
    def visit_title(self, node: nodes.title):
        if isinstance(node.parent, nodes.section) and self._section_level < 1:
            raise nodes.SkipNode
        super().visit_title(node)

    # TODO: It should separate transform and translate.
    def visit_container(self, node: nodes.container):
        if node.get("literal_block"):
            self.body.append(f"{self._hi.prefix}#figure(\n")
            self._hi.push("  ")
            literal = node.children.pop()
            node.children.insert(0, literal)

    def depart_container(self, node: nodes.container):
        if node.get("literal_block"):
            self._hi.pop()
            self.body.append(f"{self._hi.indent})\n")

    def visit_image(self, node: nodes.image):
        uri = node["uri"]
        source = Path(self.document["source"])
        uri_path = source.parent / uri
        uri_dest = self.builder._images_dir / uri_path.relative_to(
            self.builder.app.srcdir
        )
        uri_map = uri_dest.relative_to(self.builder.outdir)
        self.builder.images.setdefault(uri_path, uri_dest)
        node["uri"] = uri_map
        super().visit_image(node)

    def visit_reference(self, node):
        # NOTE: It may be should implement in rst2typst.
        if node.get("internal", False):
            uri = node["refuri"][1:]
            self.body.append(f"#link(<{uri}>)[")
            return
        super().visit_reference(node)

    # Implements for Sphinx's nodes
    # =============================
    def visit_desc(self, node: addnodes.desc):
        self.packages.add(_typst_local_package_fullname("atsphinx-typst"), "desc")
        self.body.append(f"{self._hi.prefix}#desc(\n")
        self._hi.push("  ")

    def depart_desc(self, node: addnodes.desc):
        self._hi.pop()
        self.body.append(f"{self._hi.indent})\n")

    def visit_desc_signature(self, node: addnodes.desc_signature):
        self.body.append(f"{self._hi.prefix}[\n")
        self._hi.push("  ")

    def depart_desc_signature(self, node: addnodes.desc_signature):
        for id in node.get("ids", []):
            self.body.append(f" <{id}>")
        self._hi.pop()
        self.body.append(f"{self._hi.prefix}],\n")

    def visit_desc_name(self, node: addnodes.desc_name):
        self.body.append(f"{self._hi.indent}#strong(delta: 400)[")

    def depart_desc_name(self, node: addnodes.desc_name):
        self.body.append("]")

    def visit_desc_content(self, node: addnodes.desc_content):
        self.body.append(f"{self._hi.prefix}[\n")
        self._hi.push("  ")

    def depart_desc_content(self, node: addnodes.desc_content):
        self._hi.pop()
        self.body.append(f"{self._hi.indent}],\n")

    def visit_index(self, node: addnodes.index):
        # NOTE: This is very simple implementation.
        #   There may be a more correct implementation.
        # TODO: Implement other cases.

        def _escape(txt: str) -> str:
            return txt.replace("\\", "\\\\").replace('"', '\\"')

        self.packages.add("@preview/in-dexter:0.7.2")
        self.context["has_index"] = True
        for entry in node.get("entries", []):
            entrytype, entryname, _target, _ignored, _key = entry
            if entrytype != "pair":
                logger.info("Currently, it only suports 'pair' typed entries.")
                continue

            parts = split_index_msg(entrytype, entryname)
            index_name, index_group = parts
            index_path = f'"{_escape(index_group)}", "{_escape(index_name)}"'
            self.body.append(f"#index({index_path}, apply-casing: false)")

    def depart_index(self, node: addnodes.index):
        pass

    def visit_start_of_file(self, node: addnodes.start_of_file):
        # NOTE: Implement this when rendering anything as the "start of file."
        pass

    def depart_start_of_file(self, node: addnodes.start_of_file):
        pass
