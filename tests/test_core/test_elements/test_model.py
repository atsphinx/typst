# TODO: Write more tests.
# ruff: noqa: D101, D102, D107
import textwrap

from atsphinx.typst.core.elements import model as t


class TestLint:
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
