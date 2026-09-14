"""Template: a parsed template plus the logic to render it and to resolve its own
<%include file="..."/> references.

`resolve_include()` is a *separate* code path from `TemplateLookup.get_template()` (see
`lookup.py`) -- it exists because an include's `file` is resolved relative to the directory the
*including* template's own source file lives in (`self.source_dir`), not by re-searching every
directory `TemplateLookup` knows about.
"""

from __future__ import annotations

import os


class Template:
    def __init__(
        self,
        text: str,
        uri: str | None = None,
        lookup: "object | None" = None,
        source_dir: str | None = None,
    ):
        from .ast import parse
        from .lexer import tokenize

        self.text = text
        self.uri = uri
        self.lookup = lookup
        # Directory this template's own source file lives in (None for in-memory templates with
        # no on-disk file, e.g. Template(text) built directly in a test -- such templates cannot
        # use relative <%include>).
        self.source_dir = source_dir
        self.ast = parse(tokenize(text))

    def render(self, **context) -> str:
        from .compiler import Compiler

        return Compiler(dict(context), current_template=self).render(self.ast)

    def resolve_include(self, file: str) -> "Template":
        """Load a <%include file="..."/> target relative to this template's own source_dir."""
        if self.source_dir is None:
            raise LookupError(f"cannot resolve include {file!r}: template has no source_dir")
        # Strip a leading slash so "/partial.html" resolves relative to source_dir instead of
        # being treated as filesystem-absolute.
        normalized = file[1:] if file.startswith("/") else file
        path = os.path.join(self.source_dir, normalized)
        if not os.path.isfile(path):
            raise LookupError(f"Cannot locate template for uri {file!r}")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        return Template(text, uri=file, lookup=self.lookup, source_dir=self.source_dir)
