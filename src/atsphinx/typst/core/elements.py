"""Classes for Typst elements.

Elements is tree style object and have ``to_text`` method to render document.
"""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from anytree import Node


class Text(Node):
    def to_text(self, indent: int = 0):
        return f"\n{' ' * indent}".join(self.name.split("\n"))


class Element(Node):
    LABEL: str = ""

    def __init__(self, parent=None, children=None, **kwargs):
        super().__init__(self.LABEL, parent, children, **kwargs)

    def to_text(self, indent: int = 0):
        return "\n".join([c.to_text(indent) for c in self.children])


class Document(Element):
    LABEL = "document"

    def to_text(self, indent: int = 0):
        return "\n\n".join([c.to_text(indent) for c in self.children])


class Section(Element):
    LABEL = "section"

    def to_text(self, indent: int = 0):
        return "\n\n".join([c.to_text(indent) for c in self.children])


class Heading(Element):
    LABEL = "heading"

    def to_text(self, indent: int = 0):
        return f"{'=' * self.depth} {super().to_text(indent + self.depth + 1)}"


class Paragraph(Element):
    LABEL = "par"

    def to_text(self, indent: int = 0):
        return "\n".join(
            [
                f"{' ' * indent if idx > 0 else ''}{c.to_text(indent)}"
                for idx, c in enumerate(self.children)
            ]
        )


class BulletList(Element):
    LABEL = "list"

    def to_text(self, indent: int = 0):
        prefix = f"{' ' * indent}- "
        return "\n".join(
            [
                c.to_text(indent + 2)
                if isinstance(c, BulletList)
                else f"{prefix}{c.to_text(indent + 2)}"
                for c in self.children
            ]
        )


class NumberedList(Element):
    LABEL = "enum"

    def to_text(self, indent: int = 0):
        prefix = f"{' ' * indent}+ "
        return "\n".join(
            [
                c.to_text(indent + 2)
                if isinstance(c, BulletList)
                else f"{prefix}{c.to_text(indent + 2)}"
                for c in self.children
            ]
        )


class Table(Element):
    LABEL = "table"

    def to_text(self, indent: int = 0):
        text = [
            "#table(",
            "  columns: 2,",
        ]
        for c in self.children:
            text.append(f"  [{c.to_text(3)}],")
        text.append(")")
        return "\n".join(text)


if __name__ == "__main__":
    from anytree import RenderTree

    root = Document(
        children=[
            Heading(children=[Text("atspinx-typst's documentation")]),
            Paragraph(
                children=[
                    Text("Contents"),
                ]
            ),
            Section(
                children=[
                    Heading(children=[Text("Overview")]),
                    Paragraph(
                        children=[
                            Text("This is Sphinx extension."),
                        ]
                    ),
                ]
            ),
            Section(
                children=[
                    Heading(children=[Text("Examples")]),
                    BulletList(
                        children=[
                            Paragraph(
                                children=[Text("This is one of Sphinx extensions.")]
                            ),
                            Paragraph(children=[Text("This name is atsphinx-typst.")]),
                            BulletList(
                                children=[
                                    Paragraph(
                                        children=[
                                            Text("This is one of Sphinx extensions."),
                                            Text("This is one of Sphinx extensions."),
                                        ]
                                    ),
                                    Paragraph(
                                        children=[Text("This name is atsphinx-typst.")]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ]
    )

    print(RenderTree(root))
    print(root.to_text())
