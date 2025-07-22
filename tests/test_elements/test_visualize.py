# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107
import textwrap

from atsphinx.typst.elements import visualize as t


class TestImage:
    def test_default(self):
        elm = t.Image("./example.png")
        assert elm.to_text() == textwrap.dedent("""\
#image(
  "./example.png",
)""")

    def test_with_param(self):
        elm = t.Image("./example.png", alt="Dummy")
        assert elm.to_text() == textwrap.dedent("""\
#image(
  "./example.png",
  alt: "Dummy",
)""")
