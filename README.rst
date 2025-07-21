==============
atsphinx-typst
==============

Faster PDF generator from Sphinx document using Typst.

Features
========

* Provide ``typst`` and ``typstpdf`` builder
  to generate Typst document (and PDF) from doctree.
* TODO: Provide utility directives and roles for Typst syntax.

Getting started
===============

.. code:: console

   pip install atsphinx-typst
   # If you also want to build PDF, install with extra 'pdf'
   pip install 'atsphinx-typst[pdf]'

You can run ``typst`` and ``typstpdf`` builder without set it into extensions.

.. code:: console

    # To generate Typst document.
    make typst
    # To generate Typst document and PDF from document.
    make typstpdf

Milestones
==========

v0.1 (for working)
------------------

* Supports core directives and roles.
* ✅ Supports generating PDF using ``typst`` python project.
* ✅ Gnerate PDF file of this project's project.

v1.0 (for stable)
-----------------

* Use for PDF of sphinx-revealjs's documentation.
* Publish my private tech ZINE.
