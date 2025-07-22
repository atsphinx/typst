# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

import pytest
from sphinx.errors import ThemeError

from atsphinx.typst import theming as t


def test__theme_not_found():
    with pytest.raises(ThemeError):
        t.load_theme("___")


def test__builtin_theme_found():
    theme = t.load_theme("manual")
    assert isinstance(theme, t.Theme)
