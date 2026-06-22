Cross-Reference Test Documentation
===================================

This document tests cross-referencing to other documents as described in the Sphinx documentation.

Cross-Referencing Documents
---------------------------

Using the ``:doc:`` role to reference other documents:

* Link to page1: :doc:`page1`
* Link to page2: :doc:`page2`
* Link to page1 with custom text: :doc:`First Page <page1>`
* Link to page2 with custom text: :doc:`Second Page <page2>`

Using absolute paths:

* Absolute link to page1: :doc:`/page1`
* Absolute link to page2: :doc:`/page2`

Using relative paths with subdirectories:

* Link to nested page: :doc:`subdir/nested`

Cross-Referencing with Download Role
-------------------------------------

The ``:download:`` role can also reference documents:

* Download link: :download:`page1.rst <page1.rst>`

Other Reference Roles
----------------------

Sphinx resolves more than just ``:doc:`` through ``pending_xref`` nodes.
These should keep working the same way they do without the Typst builder:

* Ref to a named target in another document: :ref:`custom-target`
* Confval-style target containing brackets: :confval:`my_option[]`

.. confval:: my_option[]

   A configuration value whose name contains brackets, like the real
   ``typst_documents[].entrypoint`` confval used in this project's own docs.

Edge Cases
----------

Testing edge cases:

* Reference to document without sections: :doc:`no_sections`

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   page1
   page2
   subdir/nested
   subdir/sibling
   no_sections
