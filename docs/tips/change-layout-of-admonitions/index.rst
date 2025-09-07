============================
Change layout of admonitions
============================

atsphinx-typst renders admonitions using box layout.

.. figure:: ./default-admonition-layout.png
    :align: center

    Layout of admonition in bundle module.

When you want to change layout of admonitions,
override function by custom template.

.. literalinclude:: ../../../tests/testdocs/test-override-typst-module/_templates/document.typ.jinja
    :caption: _templates/document.typ.jinja
    :language: typst
