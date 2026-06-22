Nested Page
===========

This is a nested page in a subdirectory.

Nested Content
--------------

This page demonstrates cross-referencing from a subdirectory.

Navigation from Subdirectory
-----------------------------

* Back to the main document
* Go to :doc:`../page1`
* Go to :doc:`../page2`

Using absolute paths:

* Absolute link to page1: :doc:`/page1`

Using a bare relative path (no ``../`` or ``./`` prefix), which per Sphinx
docs resolves relative to this document's own directory, i.e. to
``subdir/sibling``:

* Bare relative link to sibling: :doc:`sibling`
