"""od15 JSON Parser -- reference solution.

Source (MED, TrueInterview via kevin-2023-code/Tech-Interview-Questions "Implement a JSON
Parser", LLD, undated): the confirmed shape is "parse one JSON value, output minified JSON or
INVALID". The exact grammar enforced, the canonical string re-escaping rule, iterative depth
handling, duplicate-key policy, and the path query language are all reconstructed and stated in
problem.md. `json` (stdlib) is used only in the TEST file for cross-checking, never here.

Internal representation: every parsed value is a small tagged tuple so numbers can be echoed back
using their ORIGINAL source text (never round-tripped through float, which would silently change
"1.50" to "1.5" or "1e2" to "100.0"):
    ('str', python_str)          -- already escape-decoded
    ('num', raw_source_text)     -- verbatim substring, grammar-validated but not reparsed
    ('bool', True | False)
    ('null',)
    ('arr', [value, ...])
    ('obj', [(key_str, value), ...])   -- unique keys, order = first-seen position (dict-like)

Part1: hand-rolled tokenizer (validates string escapes and number grammar at the lexical level)
plus a stack-based structural parser (validates bracket/comma/colon placement, rejects trailing
garbage) and a matching minifier.
Part2: both the parser and the minifier use an EXPLICIT stack of open containers -- never Python
recursion -- so `[[[...]]]` nested 10**5 deep never risks RecursionError.
Part3: `parse(text, on_duplicate_key=...)` ("last" replaces in place, keeping first-seen
position -- like a Python dict; "error" raises ValueError on any repeated key in the same
object) and `query_path(value, path)` for a small path language like "a.b[2].c".
"""

from __future__ import annotations

import sys

_DIGITS = frozenset("0123456789")
_HEXDIGITS = frozenset("0123456789abcdefABCDEF")
_SIMPLE_ESCAPES = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}


# --------------------------------------------------------------------------- tokenizer
def _scan_hex4(s: str, i: int) -> tuple[int, int]:
    hex4 = s[i : i + 4]
    if len(hex4) < 4 or any(ch not in _HEXDIGITS for ch in hex4):
        raise ValueError(f"invalid \\u escape at position {i}")
    return int(hex4, 16), i + 4


def _scan_string(s: str, i: int) -> tuple[str, int]:
    """s[i] == '\"'. Returns (decoded_value, index_just_past_closing_quote)."""
    n = len(s)
    j = i + 1
    out: list[str] = []
    while True:
        if j >= n:
            raise ValueError("unterminated string literal")
        c = s[j]
        if c == '"':
            return "".join(out), j + 1
        if c == "\\":
            j += 1
            if j >= n:
                raise ValueError("unterminated escape sequence")
            e = s[j]
            if e in _SIMPLE_ESCAPES:
                out.append(_SIMPLE_ESCAPES[e])
                j += 1
            elif e == "u":
                code, j = _scan_hex4(s, j + 1)
                if 0xD800 <= code <= 0xDBFF:
                    if j + 1 < n and s[j] == "\\" and s[j + 1] == "u":
                        low, j2 = _scan_hex4(s, j + 2)
                        if 0xDC00 <= low <= 0xDFFF:
                            out.append(chr(0x10000 + (code - 0xD800) * 0x400 + (low - 0xDC00)))
                            j = j2
                        else:
                            raise ValueError("unpaired high surrogate in \\u escape")
                    else:
                        raise ValueError("unpaired high surrogate in \\u escape")
                elif 0xDC00 <= code <= 0xDFFF:
                    raise ValueError("unpaired low surrogate in \\u escape")
                else:
                    out.append(chr(code))
            else:
                raise ValueError(f"invalid escape character '\\{e}'")
        elif ord(c) < 0x20:
            raise ValueError("control character must be escaped in a string")
        else:
            out.append(c)
            j += 1


def _scan_number(s: str, i: int) -> tuple[str, int]:
    n = len(s)
    start = i
    if s[i] == "-":
        i += 1
        if i >= n or s[i] not in _DIGITS:
            raise ValueError("invalid number: expected digit after '-'")
    if i >= n or s[i] not in _DIGITS:
        raise ValueError("invalid number")
    if s[i] == "0":
        i += 1
    else:
        while i < n and s[i] in _DIGITS:
            i += 1
    if i < n and s[i] == ".":
        i += 1
        if i >= n or s[i] not in _DIGITS:
            raise ValueError("invalid number: expected digit after '.'")
        while i < n and s[i] in _DIGITS:
            i += 1
    if i < n and s[i] in "eE":
        i += 1
        if i < n and s[i] in "+-":
            i += 1
        if i >= n or s[i] not in _DIGITS:
            raise ValueError("invalid number: expected digit in exponent")
        while i < n and s[i] in _DIGITS:
            i += 1
    return s[start:i], i


def _tokenize(s: str) -> list[tuple[str, object]]:
    tokens: list[tuple[str, object]] = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in " \t\n\r":
            i += 1
        elif c in "{}[]:,":
            tokens.append((c, c))
            i += 1
        elif c == '"':
            value, i = _scan_string(s, i)
            tokens.append(("string", value))
        elif c == "-" or c in _DIGITS:
            raw, i = _scan_number(s, i)
            tokens.append(("number", raw))
        elif s.startswith("true", i):
            tokens.append(("true", True))
            i += 4
        elif s.startswith("false", i):
            tokens.append(("false", False))
            i += 5
        elif s.startswith("null", i):
            tokens.append(("null", None))
            i += 4
        else:
            raise ValueError(f"unexpected character {c!r} at position {i}")
    return tokens


# --------------------------------------------------------------------------- structural parser
def _parse_tokens(tokens: list[tuple[str, object]], on_duplicate_key: str) -> tuple[tuple, int]:
    """Iterative (explicit stack of open-container frames, no Python recursion) recursive-descent
    parse. Returns (value, index_just_past_the_top_level_value); caller checks for trailing
    tokens."""
    n = len(tokens)
    pos = 0
    stack: list[dict] = []

    def start_value():
        nonlocal pos
        if pos >= n:
            raise ValueError("unexpected end of input, expected a value")
        kind, val = tokens[pos]
        if kind == "{":
            pos += 1
            stack.append({"type": "object", "pairs": [], "index_by_key": {}, "need": "after_open"})
            return None
        if kind == "[":
            pos += 1
            stack.append({"type": "array", "items": [], "need": "after_open"})
            return None
        if kind == "string":
            pos += 1
            return ("str", val)
        if kind == "number":
            pos += 1
            return ("num", val)
        if kind == "true":
            pos += 1
            return ("bool", True)
        if kind == "false":
            pos += 1
            return ("bool", False)
        if kind == "null":
            pos += 1
            return ("null",)
        raise ValueError(f"unexpected token {kind!r}, expected a value")

    def attach(value):
        frame = stack[-1]
        if frame["type"] == "array":
            frame["items"].append(value)
        else:
            key = frame.pop("pending_key")
            if key in frame["index_by_key"]:
                if on_duplicate_key == "error":
                    raise ValueError(f"duplicate key: {key!r}")
                frame["pairs"][frame["index_by_key"][key]] = (key, value)
            else:
                frame["index_by_key"][key] = len(frame["pairs"])
                frame["pairs"].append((key, value))
        frame["need"] = "after_value"

    value = start_value()
    if value is not None:
        return value, pos

    while stack:
        frame = stack[-1]
        if frame["type"] == "array":
            need = frame["need"]
            if need in ("after_open", "after_comma"):
                if need == "after_open" and pos < n and tokens[pos][0] == "]":
                    pos += 1
                    closed = ("arr", frame["items"])
                    stack.pop()
                    if not stack:
                        return closed, pos
                    attach(closed)
                    continue
                v = start_value()
                if v is not None:
                    attach(v)
                continue
            if need == "after_value":
                if pos >= n:
                    raise ValueError("unexpected end of input inside array")
                kind = tokens[pos][0]
                if kind == "]":
                    pos += 1
                    closed = ("arr", frame["items"])
                    stack.pop()
                    if not stack:
                        return closed, pos
                    attach(closed)
                elif kind == ",":
                    pos += 1
                    frame["need"] = "after_comma"
                else:
                    raise ValueError(f"expected ',' or ']' in array, got {kind!r}")
                continue
            raise AssertionError(need)
        else:  # object
            need = frame["need"]
            if need in ("after_open", "after_comma"):
                if need == "after_open" and pos < n and tokens[pos][0] == "}":
                    pos += 1
                    closed = ("obj", frame["pairs"])
                    stack.pop()
                    if not stack:
                        return closed, pos
                    attach(closed)
                    continue
                if pos >= n or tokens[pos][0] != "string":
                    raise ValueError("expected a string key in object")
                frame["pending_key"] = tokens[pos][1]
                pos += 1
                frame["need"] = "after_key"
                continue
            if need == "after_key":
                if pos >= n or tokens[pos][0] != ":":
                    raise ValueError("expected ':' after object key")
                pos += 1
                frame["need"] = "after_colon"
                continue
            if need == "after_colon":
                v = start_value()
                if v is not None:
                    attach(v)
                continue
            if need == "after_value":
                if pos >= n:
                    raise ValueError("unexpected end of input inside object")
                kind = tokens[pos][0]
                if kind == "}":
                    pos += 1
                    closed = ("obj", frame["pairs"])
                    stack.pop()
                    if not stack:
                        return closed, pos
                    attach(closed)
                elif kind == ",":
                    pos += 1
                    frame["need"] = "after_comma"
                else:
                    raise ValueError(f"expected ',' or '}}' in object, got {kind!r}")
                continue
            raise AssertionError(need)
    raise AssertionError("unreachable: stack emptied without returning a value")


def parse(text: str, on_duplicate_key: str = "last") -> tuple:
    """Parse exactly one JSON value from `text`. Raises ValueError if `text` is not a single
    valid JSON document (malformed syntax, or non-whitespace trailing garbage after the value).
    `on_duplicate_key`: 'last' (later occurrence wins, keeping the FIRST occurrence's position --
    the same behavior as repeatedly assigning into a Python dict) or 'error' (any repeated key
    within the same object raises ValueError)."""
    if on_duplicate_key not in ("last", "error"):
        raise ValueError(f"invalid on_duplicate_key policy: {on_duplicate_key!r}")
    tokens = _tokenize(text)
    value, pos = _parse_tokens(tokens, on_duplicate_key)
    if pos != len(tokens):
        raise ValueError("trailing data after JSON value")
    return value


# --------------------------------------------------------------------------- canonical re-escaping
def _escape_string(s: str) -> str:
    """Canonical re-escaping rule (documented, since the source input may have used a different
    but equivalent escaping): escape only '\"', '\\\\', the five short forms (\\b \\f \\n \\r \\t),
    and any other control character (< 0x20) as lowercase \\u00xx. Never escape '/' (valid
    un-escaped either way). Never escape non-ASCII characters -- they are written out as literal
    UTF-8 text, matching json.dumps(..., ensure_ascii=False)."""
    out = ['"']
    for ch in s:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ord(ch) < 0x20:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


# --------------------------------------------------------------------------- iterative minifier
def _emit_value_start(value: tuple, out: list[str], stack: list[list]) -> None:
    tag = value[0]
    if tag == "arr":
        stack.append(["arr", value[1], 0])
    elif tag == "obj":
        stack.append(["obj", value[1], 0])
    elif tag == "str":
        out.append(_escape_string(value[1]))
    elif tag == "num":
        out.append(value[1])
    elif tag == "bool":
        out.append("true" if value[1] else "false")
    elif tag == "null":
        out.append("null")
    else:
        raise AssertionError(tag)


def serialize(value: tuple) -> str:
    """Minified JSON text for `value`. Iterative (explicit stack of [kind, items/pairs, index]
    frames) -- a 10**5-deep chain of single-element arrays never touches the Python call stack."""
    out: list[str] = []
    stack: list[list] = []
    _emit_value_start(value, out, stack)
    while stack:
        frame = stack[-1]
        kind, collection, idx = frame
        if kind == "arr":
            if idx == 0:
                out.append("[")
            if idx < len(collection):
                if idx > 0:
                    out.append(",")
                frame[2] += 1
                _emit_value_start(collection[idx], out, stack)
            else:
                out.append("]")
                stack.pop()
        else:  # obj
            if idx == 0:
                out.append("{")
            if idx < len(collection):
                if idx > 0:
                    out.append(",")
                key, val = collection[idx]
                frame[2] += 1
                out.append(_escape_string(key))
                out.append(":")
                _emit_value_start(val, out, stack)
            else:
                out.append("}")
                stack.pop()
    return "".join(out)


def minify(text: str) -> str:
    """Parse then re-serialize; raises ValueError if `text` is not valid JSON (callers wrap this
    to produce the "INVALID" sentinel for the command stream)."""
    return serialize(parse(text))


# --------------------------------------------------------------------------- Part 3: path query
def _parse_path(path: str) -> list:
    if path == "":
        return []
    tokens: list = []
    for segment in path.split("."):
        if segment == "":
            raise ValueError("empty path segment")
        bracket = segment.find("[")
        name, rest = (segment, "") if bracket == -1 else (segment[:bracket], segment[bracket:])
        if name:
            tokens.append(name)
        while rest:
            if not rest.startswith("["):
                raise ValueError(f"malformed path segment: {segment!r}")
            close = rest.find("]")
            if close == -1:
                raise ValueError(f"malformed path segment: {segment!r}")
            idx_str = rest[1:close]
            if not idx_str.isdigit():
                raise ValueError(f"malformed array index: {idx_str!r}")
            tokens.append(int(idx_str))
            rest = rest[close + 1 :]
    return tokens


def query_path(value: tuple, path: str) -> str:
    """Navigate `value` per a small path language: '.' descends into an object member by key,
    '[N]' descends into an array by 0-based index; the two compose ("a.b[2].c"). Returns the
    minified JSON text of the value found. Raises ValueError for a malformed path or a type
    mismatch (indexing an array with a key, or an object with '[N]'), KeyError for a missing
    object key, IndexError for an out-of-range array index."""
    node = value
    for token in _parse_path(path):
        if isinstance(token, str):
            if node[0] != "obj":
                raise ValueError(f"cannot look up key {token!r}: not an object")
            match = [v for k, v in node[1] if k == token]
            if not match:
                raise KeyError(token)
            node = match[0]
        else:
            if node[0] != "arr":
                raise ValueError(f"cannot index [{token}]: not an array")
            items = node[1]
            if token < 0 or token >= len(items):
                raise IndexError(token)
            node = items[token]
    return serialize(node)


# --------------------------------------------------------------------------- command stream
def _part1_or_2(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        _cmd, _, json_text = line.partition(" ")
        try:
            out.append(minify(json_text))
        except ValueError:
            out.append("INVALID")
    return out


def part1(lines: list[str]) -> list[str]:
    return _part1_or_2(lines)


def part2(lines: list[str]) -> list[str]:
    return _part1_or_2(lines)


def part3(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        fields = line.split(" ", 2)
        cmd = fields[0]
        if cmd == "PARSE_DUP":
            policy, json_text = fields[1], fields[2]
            try:
                out.append(serialize(parse(json_text, on_duplicate_key=policy)))
            except ValueError as exc:
                out.append("DUPLICATE" if "duplicate key" in str(exc) else "INVALID")
        elif cmd == "PATH":
            path, json_text = fields[1], fields[2]
            try:
                value = parse(json_text)
            except ValueError:
                out.append("INVALID")
                continue
            try:
                out.append(query_path(value, path))
            except (ValueError, KeyError, IndexError):
                out.append("NOTFOUND")
        else:
            raise ValueError(f"unknown command: {line!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = [ln for ln in lines[1:] if ln.strip()]
    out = {1: part1, 2: part2, 3: part3}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
