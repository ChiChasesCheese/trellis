"""Turns raw YAML-subset text into a flat list of `Line` records: one per non-blank,
non-comment line, each carrying its indentation depth and what kind of content it holds.

`parser.py` never looks at raw text or counts spaces itself -- it only ever looks at these
records. Keeping "how many spaces does this line start with" separate from "what does this
block of lines mean" is what makes the parser's nesting logic readable on its own.
"""

from __future__ import annotations

from dataclasses import dataclass

# The two shapes a "- " list item's own line can take:
#   "- host: a.example.com"   -> mapping-inline: this item is a mapping, whose first key/value
#                                 (here "host"/"a.example.com") is written on the dash's own line
#   "- standalone-value"      -> scalar: the whole item is just this one value
LIST_ITEM_MAPPING = "mapping_inline"
LIST_ITEM_SCALAR = "scalar"


@dataclass
class Line:
    indent: int
    kind: str  # "list_item" or "map_entry"
    key: str | None = None  # map_entry's key, or a mapping-inline list_item's first key
    value: str | None = None  # raw (still-a-string) scalar value, or None if no inline value
    list_item_kind: str | None = None  # LIST_ITEM_MAPPING / LIST_ITEM_SCALAR, list_item only


def _leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _split_key_value(text: str) -> tuple[str, str | None]:
    """Split "key: value" into (key, value), or "key:" into (key, None) (a nested block follows
    on later, more-indented lines)."""
    if ":" not in text:
        raise ValueError(f"expected 'key: value' or 'key:', got {text!r}")
    key, _, rest = text.partition(":")
    rest = rest.strip()
    return key.strip(), (rest if rest else None)


def tokenize(text: str) -> list[Line]:
    lines: list[Line] = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = _leading_spaces(raw)
        body = raw[indent:]

        if body.startswith("- "):
            rest = body[2:].strip()
            if ":" in rest:
                key, value = _split_key_value(rest)
                lines.append(
                    Line(
                        indent=indent,
                        kind="list_item",
                        key=key,
                        value=value,
                        list_item_kind=LIST_ITEM_MAPPING,
                    )
                )
            else:
                lines.append(
                    Line(indent=indent, kind="list_item", value=rest, list_item_kind=LIST_ITEM_SCALAR)
                )
        else:
            key, value = _split_key_value(body)
            lines.append(Line(indent=indent, kind="map_entry", key=key, value=value))

    return lines
