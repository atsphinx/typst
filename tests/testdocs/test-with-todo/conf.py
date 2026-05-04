# noqa: D100

extensions = [
    "sphinx.ext.todo",
    "atsphinx.typst",
]

typst_documents = [
    {
        "entrypoint": "index",
        "filename": "index",
        "theme": "manual",
        "title": "Test documentation",
    }
]
