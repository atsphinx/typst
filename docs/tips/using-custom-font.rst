=================
Using custom font
=================

When you want to build PDF using other lanuage than English (e.g. Japanese),
it requires other font file to render all text correctly.

Step
====

Download custom font
--------------------

At first, you should find TTF font and download it.

Configure Sphinx document
-------------------------

If the downloaded fonts are installed on your system,
``atsphinx-typst`` can use them without any additional configuration.
If you prefer to use them without installing,
you need to specify the path to the font files in :confval:`typst_font_paths`.

.. code-block:: python
    :caption: conf.py

    typst_font_paths = [
        "/PATH/TO/CUSTOM_FONT_DIR"
    ]

Set font into your document setting
-----------------------------------

Set the :confval:`font <typst_documents[].font>` option
in your :confval:`typst_documents` configuration to the desired font name [#]_, then run the build.

.. [#] This should be the font name, not the font filename.

.. code-block:: python
    :caption: conf.py

    typst_documents = [
        {
            "entrypoint": "index",
            "filename": "Document",
            "theme": "manual",
            "title": "My document",
            "font": "Noto Serif CJK JP",  # Write it
            "toctree_only": True,
        }
    ]

Extras
======

Use other font for heading text
-------------------------------

Override template to set other font.

.. code-block:: typst
    :caption: _templates/document.typ.jinja

    {%- extends '!document.typ.jinja' %}

    {%- block preamble %}
      {{ super() }}
      #show heading: it => text(font: "Noto Sans CJK JP", it.body)
    {%- endblock %}
