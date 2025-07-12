"""Custom builders."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

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

    def prepare_writing(self, docname: set[str]) -> None:  # noqa: D102
        # TODO: Implement after if it needs
        pass

    def write_doc(self, docname: str, doctree: nodes.document) -> None:  # noqa: D102
        # TODO: Implement it!
        visitor: writer.TypstTranslator = self.create_translator(doctree, self)  # type: ignore[assignment]
        doctree.walkabout(visitor)
        out = Path(self.app.outdir) / f"{docname}.typ"
        out.write_text(visitor.dom.to_text())

    def get_target_uri(self, docname, typ=None):  # noqa: D102
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
