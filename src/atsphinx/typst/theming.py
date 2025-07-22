"""Theming support for Typst builders.

This module is inspired :py:mod:`sphinx.theming`, but it is impleemented simplify.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from sphinx.errors import ThemeError

try:
    import tomllib  # type: ignore[unresolved-import]
except ImportError:
    import tomli as tomllib

if TYPE_CHECKING:
    from typing import Any

_BASE_THEMES_DIR = Path(__file__).parent / "themes"


class Theme:
    """Typst templating assets and configurations."""

    def __init__(self, name: str, config: dict[str, Any], dirs: list[Path]):  # noqa: D107
        self.name = name
        self._config = config
        self._dirs = dirs


def _verify_theme_path(theme_dir: Path) -> bool:
    """Verify that target directory is correct for theme."""
    theme_conf = theme_dir / "theme.toml"
    theme_typst = theme_dir / "document.typ.jinja"
    return (
        theme_dir.exists()
        and theme_dir.is_dir()
        and theme_conf.exists()
        and theme_conf.is_file()
        and theme_typst.exists()
        and theme_typst.is_file()
    )


def load_theme(name: str) -> Theme:
    """Find theme directory and load as theme object.

    If it is not found, raise error.
    """

    def _load_theme(theme_path: Path) -> Theme:
        """Create theme object from theme path."""
        name = theme_path.stem
        config = tomllib.loads((theme_path / "theme.toml").read_text(encoding="utf8"))
        return Theme(name, config, [theme_path])

    # Find from built-in themes
    theme_dir = _BASE_THEMES_DIR / name
    if _verify_theme_path(theme_dir):
        return _load_theme(theme_dir)
    raise ThemeError("Typst builder theme '%s' is not found." % name)
