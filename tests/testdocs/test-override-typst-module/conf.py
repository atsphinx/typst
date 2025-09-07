# noqa: D100

extensions = [
    "atsphinx.typst",
]
templates_path = ["_templates"]

typst_documents = [
    {
        "entrypoint": "index",
        "filename": "index",
        "theme": "manual",
        "title": "Test documentation",
    }
]
