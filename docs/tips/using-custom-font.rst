=================
Using custom font
=================

When you want to build PDF using other lanuage than English (e.g. Japanese),
it requires other font file to render all text correctly.

Step
====

Download custom font
--------------------

Configure Sphinx document
-------------------------

.. code-block:: python
    :caption: conf.py

    typst_font_paths = [
        "/PATH/TO/CUSTOM_FONT_DIR"
    ]

Set font into your document setting
-----------------------------------

.. code-block:: python
    :caption: conf.py

    typst_documents = [
        {
            "entrypoint": "index",
            "filename": "Document",
            "theme": "manual",
            "title": "My document",
            "font_set": "Noto Serif CJK JP",  # Write it
            "toctree_only": True,
        }
    ]

Build it!
---------

Extras
======

Use other font for heading text
-------------------------------

Override template to set other font.

.. code-block:: typst
    :caption: _templates/document.typ.jinja

    {%- extends '!document.typ.jinja' %}

    {%- block layout %}
      {{ super() }}
      #show heading: it => text(font: "Noto Sans CJK JP", it.body)
    {%- endblock %}
