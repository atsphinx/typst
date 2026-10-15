"""Standard tests."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test__compatibility(app: SphinxTestApp):
    """Test to pass."""
    app.build()


@pytest.mark.sphinx("typst")
def test__it(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    out = app.outdir / "index.typ"
    assert out.exists()
    assert "Test doc for atsphinx-typst" not in out.read_text()


@pytest.mark.sphinx("typstpdf")
def test__it_pdf(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    out = app.outdir / "index.typ"
    assert out.exists()
    assert "Test doc for atsphinx-typst" not in out.read_text()
    out = app.outdir / "index.pdf"
    assert out.exists()


@pytest.mark.sphinx("typst", confoverrides={"extensions": []})
def test__auto_adding_extension(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    assert (app.outdir / "index.typ").exists()


@pytest.mark.sphinx(
    "typst",
    confoverrides={
        "typst_documents": [
            {
                "entrypoint": "index",
                "filename": "document-1",
                "title": "test",
            },
            {
                "entrypoint": "index",
                "filename": "document-2",
                "title": "test",
            },
        ]
    },
)
def test__multiple_output(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    assert (app.outdir / "document-1.typ").exists()
    assert (app.outdir / "document-2.typ").exists()


@pytest.mark.sphinx("typst", testroot="with-images")
def test__copy_content_images(app: SphinxTestApp):
    """Test to pass."""
    app.build()
    assert (app.outdir / "index.typ").exists()
    assert (app.outdir / "_images/example.png").exists()
    assert (app.outdir / "_images/example.png").is_file()


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references(app: SphinxTestApp):
    """Test cross-referencing documents using :doc: role."""
    app.build()
    out = app.outdir / "index.typ"
    assert out.exists()
    content = out.read_text()
    # Check that cross-reference content is present
    assert "Cross-Reference Test Documentation" in content
    # Verify that referenced pages are included in the main document
    assert "Page 1" in content
    assert "Page 2" in content
    assert "Nested Page" in content
    # Check that cross-references are converted to Typst links.
    # A plain :doc: link carries no section anchor, so it points at the
    # document-level label (see TypstTranslator._write_anchor()).
    assert "#link(<page1>)" in content
    assert "#link(<page2>)" in content
    assert "#link(<subdir:nested>)" in content
    assert "#link(<>)" not in content
    # Verify that section labels are created for the first section of each document
    assert "<page1:page-1>" in content
    assert "<page2:page-2>" in content
    assert "<subdir:nested:nested-page>" in content
    # Verify content from referenced pages is included
    assert "first page in our cross-reference test" in content
    assert "second page in our cross-reference test" in content
    assert "nested page in a subdirectory" in content
    # Edge case: document without sections
    assert "This document has no sections" in content
    # Verify that a document-level label is generated for documents without sections
    assert "#link(<no_sections>)" in content


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_ref_role_resolves_to_actual_target(app: SphinxTestApp):
    """:ref: must resolve to the actual target, not be treated as a docname.

    For ``:ref:`custom-target``` the target is the explicit
    ``.. _custom-target:`` label in page2.rst, which is a distinct id from
    the section's own auto-generated ``target-section`` id - :ref: must
    resolve to the former, and that label must actually exist in the
    output.
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert "#link(<page2:custom-target>)" in content
    assert content.count("<page2:custom-target>") >= 2


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_bare_relative_doc_path(app: SphinxTestApp):
    """A bare relative :doc: target resolves to the current doc's directory.

    Per Sphinx docs: ":doc:`parrot` occurring in sketches/index links to
    sketches/parrot" - i.e. no ``../``/``./`` prefix is needed.
    ``subdir/nested.rst`` references ``:doc:`sibling``` with no prefix, so
    it must resolve to ``subdir/sibling``, not a top-level ``sibling``
    document.
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert "#link(<subdir:sibling>)" in content
    assert "Sibling Page" in content


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_no_sections_label_is_actually_defined(app: SphinxTestApp):
    """A no-sections document must not link to a label that's never emitted.

    ``no_sections.rst`` has no headings, so it never gets a section label.
    A whole-document ``:doc:`` reference to it must still resolve to some
    label that is actually defined in the output (the document-level
    anchor), not a dangling reference.
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert "#link(<no_sections>)" in content
    # One occurrence is the `#link(<no_sections>)` reference itself; a
    # second, independent occurrence must exist as the actual label
    # definition it points to.
    assert content.count("<no_sections>") >= 2


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_implicit_title_uses_document_title(app: SphinxTestApp):
    """Implicit-title :doc: must use the target document's title as link text.

    Per Sphinx docs: "If no explicit link text is given... the link caption
    will be the title of the given document."
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert "#link(<page1>)[Page 1]" in content
    assert "#link(<page2>)[Page 2]" in content


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_labels_use_valid_typst_syntax(app: SphinxTestApp):
    """Every generated label must only use characters Typst's <label> syntax allows.

    Per Typst's docs, a label's name may only contain letters, numbers, ``_``,
    ``-``, ``:`` and ``.``. ``:confval:`my_option[]``` has a reftarget
    containing ``[``/``]`` (mirroring this project's own real
    ``typst_documents[].entrypoint`` confval), which is copied verbatim into
    the generated label and breaks the Typst parser ("unclosed label").
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    label_pattern = re.compile(r"<([^<>\s]+)>")
    valid_label = re.compile(r"^[A-Za-z0-9_.:-]+$")
    invalid = [m for m in label_pattern.findall(content) if not valid_label.match(m)]
    assert invalid == []


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_label_before_paragraph_gets_anchor(app: SphinxTestApp):
    """An explicit label directly before a plain paragraph must not be dropped.

    ``PropagateTargets`` merges ``.. _label-before-paragraph:`` into the
    following paragraph the same way it merges a label into a following
    section (``ids=[]``, ``refid`` set on the target). Unlike a section,
    a plain paragraph has no id-emitting logic of its own in this writer,
    so nothing else will emit this anchor - ``visit_target`` must recognize
    that and write it directly instead of assuming it is "handled
    elsewhere".
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert "#metadata(none) <index:label-before-paragraph>" in content


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_label_before_confval_gets_anchor(app: SphinxTestApp):
    """An explicit label directly before a ``desc`` node must not be dropped.

    ``.. _label-before-confval:`` immediately precedes a ``.. confval::``
    directive. ``PropagateTargets`` merges the label onto the parent
    ``desc`` node, not onto its ``desc_signature`` child, so it is a
    distinct id from the confval's own auto-generated
    ``confval-labelled_option`` id. ``depart_desc_signature`` only emits
    anchors for the signature's own ids, so this one needs its own anchor
    from ``visit_target``.
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert "#metadata(none) <index:label-before-confval>" in content
    assert "<index:confval-labelled_option>" in content


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_same_page_refid_link_is_namespaced(app: SphinxTestApp):
    """A plain RST ``title_`` link must produce a namespaced Typst anchor.

    A same-page reference written as `` `Section Title`_ `` in RST (or an
    equivalent ``#anchor`` link in MyST) resolves to a ``reference`` node
    with ``refid='anchor-id'`` but with the ``internal`` attribute *absent*
    (not set to ``True``).  The base rst2typst writer handles this by
    emitting ``#link(<anchor-id>)`` without any namespace, which fails at
    Typst compile time when all documents are merged into one file.
    ``visit_reference`` must namespace the label even when ``internal`` is
    not set.
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    # The link must carry the document namespace, not a bare anchor.
    assert "#link(<page1:anchor-target>)" in content
    # The label definition it points to must also exist in the output.
    assert content.count("<page1:anchor-target>") >= 2


@pytest.mark.sphinx("typst", testroot="cross-references")
def test__cross_references_external_hyperlink_is_not_namespaced(app: SphinxTestApp):
    """A genuine external hyperlink must render as a plain, un-namespaced link.

    Unlike RST `Title`_ same-page anchors, a real external hyperlink (e.g.
    `` `Example <https://...>`_ ``) has neither ``internal`` nor ``refid``
    set - only ``refuri`` pointing at an actual URL. ``visit_reference``
    must let this fall through to the base rst2typst writer unchanged,
    rather than trying to treat the URL as a docname to namespace.
    """
    app.build()
    content = (app.outdir / "index.typ").read_text()
    assert '#link("https://example.com/")[' in content


@pytest.mark.sphinx("typstpdf", testroot="cross-references")
def test__cross_references_pdf_compiles(app: SphinxTestApp):
    """The merged document with cross-references must still compile to PDF.

    Combines several of the issues above (dangling labels, label characters
    Typst rejects) into one end-to-end check that the generated Typst source
    is actually valid.
    """
    app.build()
    assert (app.outdir / "index.pdf").exists()
