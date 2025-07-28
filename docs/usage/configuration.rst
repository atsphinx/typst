Configuration
=============

Currently, you can configure behviors of atsphinx-typst by some values.

.. confval:: typst_documents
    :type: list[dict]
    :default: ``[]``

    List of documents that you want to create as Typst format.
    You must set it as list having "Document Settings" dict objects.

    Dict keys:

    .. list-table::

        - * entrypoint
          * Docname for generating document.
        - * filename
          * Output filename (excluded extension).
        - * title
          * Document title that is used title page and PDF metadata.
        - * theme
          * Generating style.
        - * toctree_only
          * WHen it is ``True``, builder only writes contents of toctree from ``entrypoint``.

    You can write out multiple layout documents from same project.

    .. code-block:: python

        typst_documents = [
            {
                "entrypoint": "index",
                "filename": "document-for-pdf",
                "title": "Documentation (PDF style)",
                "theme": "manual",
            },
            {
                "entrypoint": "index",
                "filename": "document-for-paper",
                "title": "Documentation (Paper style)",
                "theme": "manual-paper",
            },
        ]

.. confval:: typst_static_path
    :type: list[str | Path]
    :default: ``[]``

    List of path for "Static assets".
