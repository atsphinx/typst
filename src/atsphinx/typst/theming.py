"""Theming support for Typst builders.

This module is inspired :py:mod:`sphinx.theming`, but it is impleemented simplify.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from sphinx.errors import ThemeError
from sphinx.jinja2glue import BuiltinTemplateLoader

try:
    import tomllib  # type: ignore[unresolved-import]
except ImportError:
    import tomli as tomllib

if TYPE_CHECKING:
    from typing import Any, TypedDict

    from sphinx.config import Config

    from .builders import TypstBuilder

    class _ThemeToml_Theme(TypedDict, total=False):
        inherit: str
        imports: list[str]

    class _ThemeToml(TypedDict, total=False):
        theme: _ThemeToml_Theme
        options: dict


_BASE_THEMES_DIR = Path(__file__).parent / "themes"


class Theme:
    """Typst templating assets and configurations."""

    def __init__(self, name: str, config: ThemeConfig, dirs: list[Path]):  # noqa: D107
        self.name = name
        self._config = config
        self._dirs = dirs
        self._templates = BuiltinTemplateLoader()

    def init(self, builder: TypstBuilder):  # noqa: D102
        self._templates.init(builder, self)

    def get_parent_theme(self) -> str | None:
        """Retrieve parent theme name if it is exists."""
        return self._config.inherit

    def get_theme_dir(self) -> Path:
        """Retrieve base directory of theme."""
        return Path(self._dirs[0])

    def get_theme_dirs(self):  # noqa: D102
        # This is to work BuiltinTemplateLoader.init
        return self._dirs

    def write_doc(self, out: Path, context: ThemeContext):
        """Write content as document."""
        ctx = asdict(context) | {
            "theme": self._config,
        }
        content = self._templates.render("document.typ.jinja", ctx)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf8")


@dataclass
class ThemeConfig:
    """Resolved configuration of theme.

    This provides behavior that how dow theme work on builder.
    """

    inherit: str | None
    module_imports: list[str]
    default_options: dict[str, Any]

    @classmethod
    def make_default(cls) -> ThemeConfig:
        """Create object of default configuration values of theme."""
        return cls(inherit=None, module_imports=[], default_options={})

    @classmethod
    def resolve(cls, configs: list[_ThemeToml]) -> ThemeConfig:
        """Merge all configurations of TOML's values."""
        obj = cls.make_default()
        for config in configs:
            if "inherit" in config["theme"]:
                obj.inherit = config["theme"]["inherit"]
            obj.default_options = config.get("options", {})
            obj.module_imports += config["theme"].get("imports", [])
        return obj


@dataclass
class ThemeContext:
    """Default context values for templating."""

    title: str
    config: Config
    date: str
    body: str


def _verify_theme_path(theme_dir: Path) -> bool:
    """Verify that target directory is correct for theme."""
    theme_conf = theme_dir / "theme.toml"
    return (
        theme_dir.exists()
        and theme_dir.is_dir()
        and theme_conf.exists()
        and theme_conf.is_file()
    )


def load_theme(name: str) -> Theme:
    """Find theme directory and load as theme object.

    If it is not found, raise error.

    :param name: Target theme name.
    :returns: Theme object.
    :raises: ThemeError if argumented name or ihnerit name is not theme.
    """

    def _find_theme_path(name: str) -> Path:
        """Search theme path in order to rules.

        When it does not found, it raises ThemeError.
        """
        # Search from built-in themes
        theme_dir = _BASE_THEMES_DIR / name
        if _verify_theme_path(theme_dir):
            return theme_dir
        raise ThemeError("Typst builder theme '%s' is not found." % name)

    def _parse_theme(theme_path: Path) -> tuple[list[_ThemeToml], list[Path]]:
        """Parse and stack theme resources.

        It works recursive when there is 'extend' in config.
        """
        config: _ThemeToml = tomllib.loads(
            (theme_path / "theme.toml").read_text(encoding="utf8")
        )
        if "inherit" not in config["theme"]:
            return [config], [theme_path]
        configs, dirs = _parse_theme(_find_theme_path(config["theme"]["inherit"]))
        return configs + [config], dirs + [theme_path]

    def _load_theme(theme_path: Path) -> Theme:
        """Create theme object from theme path."""
        name = theme_path.stem
        configs, dirs = _parse_theme(theme_path)
        config = ThemeConfig.resolve(configs)
        dirs.reverse()
        return Theme(name, config, dirs)

    theme_path = _find_theme_path(name)
    return _load_theme(theme_path)
