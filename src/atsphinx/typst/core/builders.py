"""Custom builders."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from sphinx.builders import Builder

if TYPE_CHECKING:
    from docutils import nodes


class TypstBuilder(Builder):
    """Custom builder to generate Typst source from doctree."""

    name = "typst"
    format = "typst"

    def get_outdated_docs(self):  # noqa: D102
        return "all targets"

    def prepare_writing(self, docname: set[str]) -> None:  # noqa: D102
        # TODO: Implement after if it needs
        pass

    def write_doc(self, docname: str, doctree: nodes.document) -> None:  # noqa: D102
        # TODO: Implement it!
        out = Path(self.app.outdir) / f"{docname}.typ"
        out.write_text("")
