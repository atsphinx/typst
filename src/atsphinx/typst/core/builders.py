"""Custom builders."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.errors import SphinxError

from . import themes, writer

if TYPE_CHECKING:
    from docutils import nodes

    from .config import DocumentSettings


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
        for document_settings in self.config.typst_documents:
            self.write_doc(document_settings)

    def write_doc(self, document_settings: DocumentSettings):  # noqa: D102
        docname = document_settings["entry"]
        theme = themes.get_theme(document_settings["theme"])
        doctree = self.env.get_doctree(docname)
        doctree = self.assemble_doctree(doctree)
        visitor: writer.TypstTranslator = self.create_translator(doctree, self)  # type: ignore[assignment]
        doctree.walkabout(visitor)
        out = Path(self.app.outdir) / f"{docname}.typ"
        out.write_text(
            theme.get_template().render(body=visitor.dom.to_text()), encoding="utf8"
        )

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

    def write_doc(self, docment_settings: DocumentSettings) -> None:  # noqa: D102
        # TODO: Implement it!
        import typst

        super().write_doc(docment_settings)
        src = Path(self.app.outdir) / f"{docment_settings['entry']}.typ"
        out = Path(self.app.outdir) / f"{docment_settings['title']}.pdf"
        typst.compile(src, output=out)
