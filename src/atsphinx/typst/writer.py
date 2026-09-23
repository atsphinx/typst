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
    # Merged into one Typst file, so labels need a per-document namespace
    # to avoid id collisions (e.g. two "Installation" sections).
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
        # Current document, for namespacing labels (like LaTeX's curfilestack).
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

        # ids[0] (the heading's own slug) is anchored inline in depart_title;
        # ids[1:] (explicit labels above the heading) anchor here, before
        # the heading, so a :ref: lands at the section's top.
        if isinstance(node.parent, nodes.section):
            docname = _doc_label(self.curfilestack[-1])
            for node_id in node.parent.get("ids", [])[1:]:
                self._write_anchor(f"{docname}:{node_id}")

        super().visit_title(node)

    def depart_title(self, node: nodes.title):
        """Add a label to section titles for cross-referencing."""
        docname = _doc_label(self.curfilestack[-1])
        if isinstance(node.parent, nodes.section):
            ids = node.parent.get("ids", [])
        else:
            ids = []

        if ids:
            # Label goes after the title text, before the newline: == Title <label>
            self.body.append(f" <{docname}:{ids[0]}>")

        super().depart_title(node)

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
        # Key off refid/refuri directly (like Sphinx's LaTeX writer), not
        # ``internal``: plain anchor refs (RST `Title`_, MyST #anchor) get
        # refid without Sphinx ever setting ``internal``.
        if "refid" in node:
            uri = f"{_doc_label(self.curfilestack[-1])}:{node['refid']}"
        elif node.get("internal", False):
            # Sphinx-resolved cross-doc reference, shaped "docname" or
            # "docname#labelid".
            if "refuri" not in node:
                raise ExtensionError(
                    "<reference> requires 'refuri' or 'refid' attribute"
                )
            docname, _, labelid = node["refuri"].partition("#")
            uri = _doc_label(docname)
            if labelid:
                uri += f":{labelid}"
        else:
            # Plain external hyperlink - nothing to namespace.
            return super().visit_reference(node)
        return self.body.append(f"#link(<{uri}>)[")

    def visit_target(self, node: nodes.target) -> None:
        docname = _doc_label(self.curfilestack[-1])

        if not node.get("ids") and node.get("refid"):
            # PropagateTargets forwarded this target's id onto whatever
            # followed it (section, paragraph, desc, ...), clearing our
            # own ids. Walk past chained targets to find that node, like
            # LaTeX's visit_target does.
            next_node = node.next_node(ascend=True)
            while isinstance(next_node, nodes.target):
                next_node = next_node.next_node(ascend=True)

            if isinstance(next_node, nodes.section):
                # Already anchored by visit_title/depart_title's ids loop.
                raise nodes.SkipNode

            # Forwarded onto a node with no id-handling of its own (e.g. a
            # paragraph, or a desc - depart_desc_signature only anchors the
            # signature's own ids). Nothing else emits this, so do it here.
            self._write_anchor(f"{docname}:{node['refid']}")
            raise nodes.SkipNode

        # A standalone target PropagateTargets left untouched (e.g. one at
        # the end of a document) - anchor it directly, like ids[1:] above.
        target_id = node["ids"][0] if node.get("ids") else None
        if target_id:
            self._write_anchor(f"{docname}:{target_id}")
        raise nodes.SkipNode

    # Implements for Sphinx's nodes
    # =============================
    def visit_pending_xref(self, node: addnodes.pending_xref):
        # resolve_references() already replaced resolvable pending_xrefs
        # with plain reference nodes; only unresolved ones reach here.
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
        # Namespaced like section headings, see depart_title().
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
        docname = node["docname"]
        self.curfilestack.append(docname)
        self._write_anchor(_doc_label(docname))

    def depart_start_of_file(self, node: addnodes.start_of_file):
        self.curfilestack.pop()

    def _write_anchor(self, label: str) -> None:
        # An invisible label not attached to any visible content - for
        # document-level anchors and for ids that can't share a heading's
        # own label (see depart_title()).
        self.body.append(f"#metadata(none) <{label}>\n")
