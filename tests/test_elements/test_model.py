# TODO: Write more tests.
# ruff: noqa: D101, D102, D107
import textwrap

import pytest

from atsphinx.typst.elements import model as t
from atsphinx.typst.elements.base import Text


class TestHeading:
    def test_valid_level(self):
        elm = t.Heading()
        elm.level = 1
        Text("Section title", parent=elm)
        assert elm.to_text() == textwrap.dedent("""\
#heading(
  level: 1,
  [
    Section title
  ]
)""")

    def test_valid_level_2(self):
        elm = t.Heading()
        elm.level = 2
        Text("Section title", parent=elm)
        assert elm.to_text() == textwrap.dedent("""\
#heading(
  level: 2,
  [
    Section title
  ]
)""")

    def test_invalid_level(self):
        elm = t.Heading()
        elm.level = 0
        assert elm.to_text() == ""


class TestBulletList:
    @pytest.mark.skip(reason="Thinking cases")
    def test_it(self):
        pass


class TestNumberedList:
    @pytest.mark.skip(reason="Thinking cases")
    def test_it(self):
        pass


class TestTable:
    @pytest.mark.skip(reason="Thinking cases")
    def test_it(self):
        pass


class TestQuote:
    @pytest.mark.skip(reason="Thinking cases")
    def test_it(self):
        pass


class TestFigure:
    @pytest.mark.skip(reason="Thinking cases")
    def test_it(self):
        pass


class TestLink:
    def test_display_url(self):
        elm = t.Link("http://example.com")
        assert elm.to_text() == textwrap.dedent("""\
#link(
  "http://example.com",
  [
    http://example.com
  ],
)""")

    def test_with_text(self):
        elm = t.Link("http://example.com", content="EXAMPLE.COM")
        assert elm.to_text() == textwrap.dedent("""\
#link(
  "http://example.com",
  [
    EXAMPLE.COM
  ],
)""")
