==============
atsphinx-typst
==============

Generate Typst sources and PDF from Sphinx document.

Features
========

* Provide ``typst`` and ``typstpdf`` builder
  to generate Typst document (and PDF) from doctree.
* TODO: Provide utility directives and roles for Typst syntax.

Getting started
===============

.. caution:: Currently, This is not published anywhere yet.

.. code:: console

   pip install atsphinx-typst
   # If you also want to build PDF, install with extra 'pdf'
   pip install 'atsphinx-typst[pdf]'

You can run ``typst`` and ``typstpdf`` builder without set it into extensions.

.. code:: console

   make typst
   make typstpdf

Milestones
==========

v0.1 (for working)
------------------

* Supports core directives and roles.
* Supports generating PDF using ``typst`` python project.

v1.0 (for stable)
-----------------

* Use for PDF of sphinx-revealjs's documentation.
* Publish my private tech ZINE.


