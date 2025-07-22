"""Templating environment of core elements."""
# TODO: Write docstrings after.
# ruff: noqa: D101, D102, D107

from __future__ import annotations

import sys
import textwrap

import jinja2


def load_template(name: str) -> str:
    """Load template from class var.

    :param name: Class name to use as template.
    :returns: Template string.
    """
    import atsphinx.typst.elements  # noqa

    module = sys.modules["atsphinx.typst.elements"]
    if not hasattr(module, name):
        raise Exception(f"{name} is not found.")
    return textwrap.dedent(getattr(module, name).TEMPLATE).strip("\n")


env = jinja2.Environment(loader=jinja2.FunctionLoader(load_template))
env.policies["json.dumps_kwargs"]["ensure_ascii"] = False
