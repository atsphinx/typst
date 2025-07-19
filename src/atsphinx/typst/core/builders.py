"""Custom builders."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING

from docutils import nodes
from sphinx import addnodes
from sphinx._cli.util.colour import darkgreen
from sphinx.builders import Builder
from sphinx.errors import SphinxError
from sphinx.locale import _
from sphinx.util.nodes import inline_all_toctrees

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
        doctree = self.assemble_doctree(docname, document_settings["toctree_only"])
        visitor: writer.TypstTranslator = self.create_translator(doctree, self)  # type: ignore[assignment]
        doctree.walkabout(visitor)
        today_fmt = self.config.today_fmt or _("%b %d, %Y")
        context = themes.ThemeContext(
            title=document_settings["title"],
            config=self.config,
            date=date.today().strftime(today_fmt),
            body=visitor.dom.to_text(),
        )
        out = Path(self.app.outdir) / f"{document_settings['filename']}.typ"
        theme.write_doc(out, context)

    def assemble_doctree(self, docname: str, toctree_only: bool) -> nodes.document:
        """Find toctree and merge children doctree into parent doctree.

        This method is to generate single Typst document.

        .. todo::

           We must see how does inline_all_toctrees work.
        """
        root = self.env.get_doctree(docname)
        if toctree_only:
            root_section = nodes.section()
            for toctree in root.findall(addnodes.toctree):
                root_section += toctree
            root = root.copy()
            root += root_section
        tree = inline_all_toctrees(self, {docname}, docname, root, darkgreen, [docname])
        return tree

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

    def write_doc(self, document_settings: DocumentSettings) -> None:  # noqa: D102
        # TODO: Implement it!
        import typst

        super().write_doc(document_settings)
        src = Path(self.app.outdir) / f"{document_settings['filename']}.typ"
        out = Path(self.app.outdir) / f"{document_settings['filename']}.pdf"
        typst.compile(src, output=out)
