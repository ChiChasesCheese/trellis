"""AST node types for minimako, plus the token-stream parser that builds them.

Five node types, matching the four control constructs the lexer knows about, plus the root:
TemplateNode (root), TextNode, ExpressionNode, IfNode, ForNode, IncludeNode.
`compiler.py` dispatches on `type(node).__name__` (visitor pattern) -- every node type here needs
a matching `visit_<Name>` method there.
"""

from __future__ import annotations

import re

from .lexer import Token, tokenize


class Node:
    pass


class TemplateNode(Node):
    def __init__(self, body: list[Node]):
        self.body = body


class TextNode(Node):
    def __init__(self, text: str):
        self.text = text


class ExpressionNode(Node):
    def __init__(self, expr: str):
        self.expr = expr


class IfNode(Node):
    def __init__(self, cond: str, body: list[Node]):
        self.cond = cond
        self.body = body


class ForNode(Node):
    def __init__(self, target: str, iter_expr: str, body: list[Node]):
        self.target = target
        self.iter_expr = iter_expr
        self.body = body


class IncludeNode(Node):
    def __init__(self, file: str):
        self.file = file


_FOR_RE = re.compile(r"^(\w+)\s+in\s+(.+)$")


def _split_for(expr: str) -> tuple[str, str]:
    m = _FOR_RE.match(expr)
    if not m:
        raise ValueError(f"invalid for-loop expression: {expr!r} (expected 'NAME in ITERABLE')")
    return m.group(1), m.group(2)


def _parse_body(tokens: list[Token], pos: int, stop: str | None) -> tuple[list[Node], int]:
    body: list[Node] = []
    while pos < len(tokens):
        kind, val = tokens[pos]
        if kind in ("endif", "endfor"):
            if kind != stop:
                raise ValueError(f"unexpected {kind!r} (expected {stop!r} or none)")
            return body, pos  # caller consumes the matching end token
        if kind == "text":
            body.append(TextNode(val))
            pos += 1
        elif kind == "expr":
            body.append(ExpressionNode(val))
            pos += 1
        elif kind == "include":
            body.append(IncludeNode(val))
            pos += 1
        elif kind == "if":
            inner, pos = _parse_body(tokens, pos + 1, stop="endif")
            pos += 1  # consume the endif
            body.append(IfNode(val, inner))
        elif kind == "for":
            target, iter_expr = _split_for(val)
            inner, pos = _parse_body(tokens, pos + 1, stop="endfor")
            pos += 1  # consume the endfor
            body.append(ForNode(target, iter_expr, inner))
        else:  # pragma: no cover - lexer never emits anything else
            raise ValueError(f"unknown token kind {kind!r}")
    if stop is not None:
        raise ValueError(f"missing {stop!r} to close block")
    return body, pos


def parse(tokens: list[Token]) -> TemplateNode:
    body, pos = _parse_body(tokens, 0, stop=None)
    return TemplateNode(body)


def parse_text(text: str) -> TemplateNode:
    return parse(tokenize(text))
