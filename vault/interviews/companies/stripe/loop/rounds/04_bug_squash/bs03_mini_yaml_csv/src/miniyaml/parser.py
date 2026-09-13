"""Turns a `Line` stream (see lexer.py) into a nested Python structure of dict/list/scalar,
by recursive descent over indentation depth: a "block" is a maximal run of sibling lines that
all sit at the same indent, and any line whose value is missing (a bare "key:") or whose list
item is a mapping opens a *child* block on the more-indented lines that follow it.

`Parser` is a small stateful object (a `pos` cursor into the line list) rather than a pile of
functions passing indices around, because `_parse_map_block` and `_parse_list_block` call each
other recursively and need to share one advancing cursor between them.
"""

from __future__ import annotations

from .lexer import LIST_ITEM_SCALAR, tokenize
from .scalars import coerce_scalar


class Parser:
    """One Parser can be reused for several `.parse()` calls; each call is independent of the
    ones before it."""

    def __init__(self):
        self.lines: list = []
        self.pos = 0

    def parse(self, text: str) -> dict | list:
        """Parse a full YAML-subset document `text` into a dict or list."""
        self.lines = tokenize(text)
        if not self.lines:
            return {}
        return self._parse_block(self.lines[0].indent)

    def _parse_block(self, indent: int):
        """Dispatch to a map or list block parser based on the first line's kind, for the run of
        sibling lines starting at self.pos that share the given indent."""
        if self.pos >= len(self.lines) or self.lines[self.pos].indent != indent:
            return {}
        if self.lines[self.pos].kind == "list_item":
            return self._parse_list_block(indent)
        return self._parse_map_block(indent)

    def _parse_map_block(self, indent: int) -> dict:
        result: dict = {}
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if line.indent != indent or line.kind != "map_entry":
                break
            self.pos += 1
            if line.value is not None:
                result[line.key] = coerce_scalar(line.value)
            elif self.pos < len(self.lines) and self.lines[self.pos].indent > indent:
                child_indent = self.lines[self.pos].indent
                result[line.key] = self._parse_block(child_indent)
            else:
                result[line.key] = None
        return result

    def _parse_list_block(self, indent: int) -> list:
        result: list = []
        while self.pos < len(self.lines):
            line = self.lines[self.pos]
            if line.indent != indent or line.kind != "list_item":
                break
            if line.list_item_kind == LIST_ITEM_SCALAR:
                result.append(coerce_scalar(line.value))
                self.pos += 1
            else:
                self.pos += 1
                entry = {line.key: coerce_scalar(line.value)}
                # The rest of this item's mapping (if any) is written on the lines below it,
                # aligned to where its first key started rather than to the dash.
                content_indent = indent + 1
                entry.update(self._parse_map_block(content_indent))
                result.append(entry)
        return result


def parse_text(text: str) -> dict | list:
    """Convenience one-shot parse: build a fresh Parser, parse, discard it."""
    return Parser().parse(text)
