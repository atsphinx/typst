# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107
import textwrap

from atsphinx.typst.elements import text as t


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
