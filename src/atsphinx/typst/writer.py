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
from sphinx.errors import ExtensionError
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


def _doc_label(docname: str) -> str:
    # All documents are merged into a single Typst file, so every label
    # needs a per-document namespace to avoid collisions between e.g. two
    # documents that each have a "Installation" section.
    return docname.replace("/", ":")


class TypstTranslator(SphinxTranslator, BaseTypstTranslator):
    """Custom translator that has converter from dotctree to Typst syntax."""

    # NOTE: If you found ``NotImplementedError`` for node visitor/departure,
    #   add node name into ``optional`` and implement after.
    optional = [
        # "legend",  # Alredy added, but translator does not find.
        # TODO: Require implements to support apidoc.
        "desc_addname",
        "desc_annotation",
        "desc_sig_space",
        "desc_sig_name",
        "desc_parameter",
        "desc_parameterlist",
        "desc_returns",
        "desc_sig_punctuation",
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
        # Track current document for cross-references (like the LaTeX
        # writer's ``curfilestack``). The builder merges everything into
        # one doctree, so this is what lets us namespace labels per
        # document and tell which document a relative reference is in.
        self.curfilestack = [document["docname"]]

    # ------
    # visit/departuer methods
    # ------
    def visit_document(self, node: nodes.document):
        super().visit_document(node)
        self._write_anchor(_doc_label(self.curfilestack[-1]))

    def visit_title(self, node: nodes.title):
        if isinstance(node.parent, nodes.section) and self._section_level < 1:
            raise nodes.SkipNode

        super().visit_title(node)

    def depart_title(self, node: nodes.title):
        """Add a label to section titles for cross-referencing."""
        docname = _doc_label(self.curfilestack[-1])
        if isinstance(node.parent, nodes.section):
            ids = node.parent.get("ids", [])
        else:
            ids = []

        if ids:
            # Add the section label AFTER the title text but BEFORE
            # newlines. Typst syntax: == Title <label>
            self.body.append(f" <{docname}:{ids[0]}>")

        super().depart_title(node)

        # Sphinx may register more than one id for a section (e.g. an
        # explicit ``.. _target:`` placed right above the heading, used by
        # :ref:). Typst only allows a single label per element, so the
        # first id is attached directly to the heading above and every
        # other id gets its own invisible anchor here - the same way HTML
        # emits an empty anchor element for each extra id on a section.
        for node_id in ids[1:]:
            self._write_anchor(f"{docname}:{node_id}")

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

    def visit_reference(self, node: nodes.reference):
        # NOTE: It may be should implement in rst2typst.
        if not node.get("internal", False):
            return super().visit_reference(node)
        if "refid" in node:
            # Reference resolved within the current document (see
            # ``curfilestack``), e.g. a ``:ref:`` to a label in this file.
            uri = f"{_doc_label(self.curfilestack[-1])}:{node['refid']}"
        elif "refuri" in node:
            # Reference resolved to another document by Sphinx's standard
            # reference resolution (``Builder.get_relative_uri``), shaped
            # like ``docname`` or ``docname#labelid``.
            docname, _, labelid = node["refuri"].partition("#")
            uri = _doc_label(docname)
            if labelid:
                uri += f":{labelid}"
        else:
            raise ExtensionError("<reference> requires 'refuri' or 'refid' attribute")
        return self.body.append(f"#link(<{uri}>)[")

    # Implements for Sphinx's nodes
    # =============================
    def visit_pending_xref(self, node: addnodes.pending_xref):
        # NOTE: Implement this if rendering anything is needed.
        #   By the time the writer runs, ``resolve_references()`` has
        #   already replaced every resolvable ``pending_xref`` with a
        #   plain ``reference`` node (see ``assemble_doctree``); like in
        #   Sphinx's LaTeX writer, this is only reached for the rare case
        #   of an unresolved reference left in place.
        pass

    def depart_pending_xref(self, node: addnodes.pending_xref):
        pass

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
        # Namespaced the same way as section headings (see depart_title())
        # so that :py:class:, :confval:, etc. xrefs resolve consistently
        # across the merged document.
        docname = _doc_label(self.curfilestack[-1])
        ids = node.get("ids", [])
        if ids:
            self.body.append(f" <{docname}:{ids[0]}>")
        self._hi.pop()
        self.body.append(f"{self._hi.prefix}],\n")
        for node_id in ids[1:]:
            self._write_anchor(f"{docname}:{node_id}")

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
        # Track current document for cross-references (like LaTeX writer).
        docname = node["docname"]
        self.curfilestack.append(docname)
        self._write_anchor(_doc_label(docname))

    def depart_start_of_file(self, node: addnodes.start_of_file):
        self.curfilestack.pop()

    def _write_anchor(self, label: str) -> None:
        # An invisible, addressable label that isn't attached to any
        # visible content. Used to mark the start of a document - so a
        # whole-document ``:doc:`` reference (which carries no section
        # anchor) has something to link to even if that document has no
        # sections - and for ids on a section beyond the first, which
        # can't get a second label of their own (see depart_title()).
        self.body.append(f"#metadata(none) <{label}>\n")
