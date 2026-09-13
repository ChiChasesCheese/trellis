"""Turning a raw scalar string (whatever text followed a ':' or a '- ') into an actual Python
value: int, float, bool, None, or -- if nothing else matches -- the string itself.

This is deliberately separate from the parser/lexer: the parser only ever needs to know "where do
the mappings and lists nest", never "is this text secretly a number". Isolating that judgment call
here also makes it trivial to unit test on its own, string in, value out.
"""

from __future__ import annotations

_BOOL_TRUE = {"true", "True", "TRUE"}
_BOOL_FALSE = {"false", "False", "FALSE"}
_NULL = {"null", "Null", "NULL", "~"}


def coerce_scalar(raw: str | None) -> object:
    """Convert one YAML-subset scalar token to a Python value.

    Quoted strings (single or double) are unwrapped and returned verbatim, no further coercion.
    Unquoted text is tried as bool, then null, then int, then float, in that order, and falls
    back to the original string unchanged if none of those parse.
    """
    if raw is None:
        return None

    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]

    if raw in _BOOL_TRUE:
        return True
    if raw in _BOOL_FALSE:
        return False
    if raw in _NULL:
        return None

    try:
        return int(raw)
    except ValueError:
        pass

    try:
        return float(raw)
    except ValueError:
        pass

    return raw


def scalar_to_text(value: object) -> str:
    """The inverse of coerce_scalar's *type* decisions (not its exact source formatting) -- used
    when flattening a parsed document back out to CSV cell text."""
    if value is None:
        return ""
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)
