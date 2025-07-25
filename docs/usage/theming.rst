=======
Theming
=======

Item of :confval:`typst_documents` has `theme` property.
It controls some behaviors of document likely HTML theming (using :confval:`html_theme`).

Example
=======

.. code-block:: python
    :caption: conf.py

    typst_documents = [
        {
            "entrypoint": "index",
            "filename": "document",
            "title": "A documentation",
            # Set using theme name here!
            "theme": "manual",
        }
    ]

Built-in themes
===============

.. todo:: It should add images some sections.

basic
-----

This is base theme of all built-in themes.

There are many assets to render docutils nodes,
and it generate Typst document that is simple reporting style.

manual
------

This is theme to reproduce layout of PDF created from ``latexpdf`` builder.
