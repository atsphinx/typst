# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107
import textwrap

from atsphinx.typst.elements import text as t
from atsphinx.typst.elements.base import Text


class TestRaw:
    def test_it(self):
        elm = t.Raw("Content")
        assert elm.to_text() == textwrap.dedent("""\
#raw(
  "Content"
)""")

    def test_with_escaped(self):
        elm = t.Raw('print("テスト")')
        assert elm.to_text() == textwrap.dedent("""\
#raw(
  "print(\\"テスト\\")"
)""")


class TestRawBlock:
    def test_single_it(self):
        elm = t.RawBlock(
            textwrap.dedent("""\
                print("テスト")
                print("Hello")
            """).strip("\n"),
            "python",
        )
        assert elm.to_text() == textwrap.dedent("""\
```python
print(\"テスト\")
print(\"Hello\")
```
""")


class TestEmphasis:
    def test_it(self):
        elm = t.Emphasis()
        Text("Content", parent=elm)
        assert elm.to_text() == textwrap.dedent("""\
#emph[
  Content
]""")


class TestStrong:
    def test_it(self):
        elm = t.Strong()
        Text("Content", parent=elm)
        assert elm.to_text() == textwrap.dedent("""\
#strong[
  Content
]""")
