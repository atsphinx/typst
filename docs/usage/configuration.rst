Configuration
=============

Currently, you can configure behviors of atsphinx-typst by some values.

.. confval:: typst_documents
    :type: list[dict]
    :default: ``[]``

    List of documents that you want to create as Typst format.
    You must set it as list having "Document Settings" dict objects.

    Dict keys:

    .. confval:: typst_documents[].entrypoint
       :type: ``str``

       Docname for generating document.

    .. confval:: typst_documents[].filename
       :type: ``str``

       Output filename (excluded extension).

    .. confval:: typst_documents[].title
       :type: ``str``

       The title of document. It is used title page and PDF metadata.

    .. confval:: typst_documents[].author
       :type: ``str``

       The author text of document. It is used title page and PDF metadata.

    .. confval:: typst_documents[].edition
       :type: ``str``

       The publishing edition of document. It is used title page.

    .. confval:: typst_documents[].theme
       :type: ``str``

       Generating style.

    .. confval:: typst_documents[].font
       :type: ``str``

       Default font name or family to use for building PDF.

    .. confval:: typst_documents[].toctree_only
       :type: ``bool`` | ``atsphinx.typst.config.TOCTREE_ONLY_LITERAL``

       When it is ``True``, builder only writes contents of toctree from :confval:`entrypoint <typst_documents[].entrypoint>`.

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

.. confval:: typst_font_paths
    :type: list[str | Path]
    :default: ``[]``

    List of path stored additional fonts.
