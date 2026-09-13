"""TemplateLookup: the sanctioned, top-level entry point for loading a template by URI from a
set of search directories. `get_template()` strips *every* leading slash before joining against
each directory and confirms the result stays inside it (via `os.path.realpath` containment), so a
top-level `lookup.get_template("//../../etc/passwd")` is always safely rejected or resolved
within the sandbox.

Compare `template.py`'s `Template.resolve_include()`, which does its own normalization for
`<%include>` resolution *within* an already-loaded template, instead of reusing this one.
"""

from __future__ import annotations

import os

from .template import Template


class TemplateLookup:
    def __init__(self, directories: list[str]):
        self.directories = [os.path.abspath(d) for d in directories]

    def get_template(self, uri: str) -> Template:
        normalized = uri.lstrip("/")  # strip leading slashes so a URI can't look filesystem-absolute
        for directory in self.directories:
            candidate = os.path.join(directory, normalized)
            real_candidate = os.path.realpath(candidate)
            real_dir = os.path.realpath(directory)
            if real_candidate != real_dir and not real_candidate.startswith(real_dir + os.sep):
                continue  # escapes this search directory -- try the next one, if any
            if os.path.isfile(candidate):
                with open(candidate, encoding="utf-8") as f:
                    text = f.read()
                return Template(text, uri=uri, lookup=self, source_dir=directory)
        raise LookupError(f"Cannot locate template for uri {uri!r}")
