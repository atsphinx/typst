===============
Getting started
===============

Installation
============

It is published on PyPI.
You can install it by pip or other package management tools.

.. note:: Currently, it is not published yet.

.. code-block:: console

    pip install atsphinx-typst

If you want to generate PDF too, you should set ``pdf`` extra.

.. code-block:: console

    pip install 'atsphinx-typst[pdf]'

Usage
=====

You can run ``typst`` builder without editing your ``conf.py``. 

.. code-block:: console

    # To build Typst sources. 
    make typst
    # To build Typst sources and PDF files. 
    make typstpdf

When you call ``typst`` builder, it generate ``BUILD_DIR/typst``.
