# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107
import textwrap

from atsphinx.typst import elements as t


class TestSource:
    def test_single_line(self):
        elm = t.Source("$ A = pi r^2 $")
        assert elm.to_text() == "$ A = pi r^2 $\n"

    def test_multi_lines(self):
        elm = t.Source(
            textwrap.dedent("""\
            #layout(size => {
              let half = 50% * size.width
              [Half a page is #half wide.]
            })
        """)
        )
        assert elm.to_text() == textwrap.dedent("""\
            #layout(size => {
              let half = 50% * size.width
              [Half a page is #half wide.]
            })

        """)


class TestText:
    def test_single_line(self):
        elm = t.Text("Lorem ipsum dolor sit amet,")
        assert elm.to_text() == "Lorem ipsum dolor sit amet,"

    def test_multi_lines(self):
        elm = t.Text(
            textwrap.dedent("""\
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """)
        )
        assert elm.to_text() == textwrap.dedent("""\
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        """)
