"""Custom builders."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.errors import SphinxError

from . import writer

if TYPE_CHECKING:
    from docutils import nodes


class TypstBuilder(Builder):
    """Custom builder to generate Typst source from doctree."""

    name = "typst"
    format = "typst"
    default_translator_class = writer.TypstTranslator

    def get_outdated_docs(self):  # noqa: D102
        return "all targets"

    def prepare_writing(self, docnames: set[str]) -> None:  # noqa: D102
        # TODO: Implement after if it needs
        pass

    def write_documents(self, docnames):  # noqa: D102
        for docname in self.config.typst_documents:
            self.write_doc(docname, self.env.get_doctree(docname))

    def write_doc(self, docname, doctree):  # noqa: D102
        doctree = self.env.get_doctree(docname)
        doctree = self.assemble_doctree(doctree)
        visitor: writer.TypstTranslator = self.create_translator(doctree, self)  # type: ignore[assignment]
        doctree.walkabout(visitor)
        out = Path(self.app.outdir) / f"{docname}.typ"
        out.write_text(visitor.dom.to_text(), encoding="utf8")

    def assemble_doctree(self, doctree: nodes.document) -> nodes.document:
        """Find toctree and merge children doctree into parent doctree.

        This method is to generate single Typst document.
        """

        def _unpack_doctree(doctree: nodes.document) -> list[nodes.Node]:
            parts = []
            for toctree in doctree.findall(addnodes.toctree):
                toctree.parent.remove(toctree)
                for title, entry in toctree["entries"]:
                    child_ = self.env.get_doctree(entry)
                    parts.append(child_)
            return [doctree] + parts

        root = doctree.copy()
        for child in _unpack_doctree(doctree):
            root.append(child)
        return root

    def get_target_uri(self, docname, typ=None):  # noqa: D102
        # TODO: Implement it!
        return ""


class TypstPDFBuilder(TypstBuilder):
    """PDF creation builder from doctree.

    This is similar to the relationship between
    the latexpdf builder and the latex builder.
    """

    name = "typstpdf"
    format = "typst"

    def init(self) -> None:
        """Check that python env has typst package."""
        try:
            import typst  # noqa - Only try importing
        except ImportError:
            raise SphinxError("Require 'typst' to run 'typstpdf' builder.")

    def write_doc(self, docname: str, doctree: nodes.document) -> None:  # noqa: D102
        # TODO: Implement it!
        import typst

        super().write_doc(docname, doctree)
        src = Path(self.app.outdir) / f"{docname}.typ"
        out = Path(self.app.outdir) / f"{docname}.pdf"
        typst.compile(src, output=out)
