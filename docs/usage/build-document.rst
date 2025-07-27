Build document
==============

You can run ``typst`` builder without editing your ``conf.py`` after install. [#fn]_

.. [#fn] Sphinx can search builder automately because it registers module of builder into entrypoint.

.. code-block:: console

    # To build Typst sources.
    make typst
    # To build Typst sources and PDF files.
    make typstpdf

When you call ``typst`` builder, it generate ``BUILD_DIR/typst``.
