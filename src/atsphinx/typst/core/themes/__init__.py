"""Theme management of Typst builder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Template

_HERE = Path(__file__).parent


@dataclass
class Theme:
    """Document theme component."""

    template_path: Path

    def get_template(self) -> Template:
        """Retrieve template to render Typst source."""
        return Template(self.template_path.read_text(encoding="utf8"))


def get_theme(name: str) -> Theme:
    """Find and setup built-in theme."""
    theme_path = _HERE / name
    return Theme(template_path=theme_path / "page.typ.jinja")
