==========
User guide
==========

Installation
============

It is going to publish on PyPI.

.. code-block:: console

    pip install atsphinx-typst

If you want to generate PDF too, you should set ``pdf`` extra.

.. code-block:: console

    pip install 'atsphinx-typst[pdf]'

Usage
=====

You need not to edit your ``conf.py`` to build by custom builders.

.. code-block:: console

    make typst

    make typstpdf

When you call ``typst`` builder, it generate ``BUILD_DIR/typst``.

Configuration
=============

.. todo:: Write it
