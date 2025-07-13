"""Theme management of Typst builder."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Template

if TYPE_CHECKING:
    from sphinx.config import Config

_HERE = Path(__file__).parent


@dataclass
class Theme:
    """Document theme component."""

    template_path: Path

    def get_template(self) -> Template:
        """Retrieve template to render Typst source."""
        return Template(self.template_path.read_text(encoding="utf8"))

    def write_doc(self, out: Path, context: ThemeContext):
        """Write content as document."""
        tmpl = self.get_template()
        content = tmpl.render(asdict(context))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf8")


@dataclass
class ThemeContext:
    """Default context values for templating."""

    title: str
    config: Config
    date: str
    body: str


def get_theme(name: str) -> Theme:
    """Find and setup built-in theme."""
    theme_path = _HERE / name
    return Theme(template_path=theme_path / "page.typ.jinja")
