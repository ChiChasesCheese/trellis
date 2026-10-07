"""Tokenizer and recursive-descent parser for rule expressions.

    expr    := or
    or      := and ("or" and)*
    and     := not ("and" not)*
    not     := "not" not | compare
    compare := atom (("<" | "<=" | ">" | ">=" | "==" | "!=" | "in") atom)?
    atom    := NUMBER | STRING | "true" | "false" | path | "(" expr ")" | "any" "(" expr ")"
    path    := IDENT ("." IDENT)*
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from rulelang.errors import ConfigError


class RuleSyntaxError(ConfigError):
    """A rule that cannot be loaded; carries the 1-based position of the problem."""

    def __init__(self, reason: str, line: int = 1, column: int = 1, rule: str | None = None):
        where = f"rule {rule!r}: " if rule else ""
        super().__init__(f"{where}{reason} (line {line}, column {column})")
        self.reason = reason
        self.line = line
        self.column = column


@dataclass(frozen=True)
class Token:
    kind: str  # number | string | ident | op | lparen | rparen | dot | eof
    text: str
    line: int
    col: int


_TOKEN = re.compile(
    r"""(?P<ws>\s+)
      | (?P<number>\d+(?:\.\d+)?)
      | (?P<string>"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*')
      | (?P<ident>[A-Za-z_][A-Za-z0-9_]*)
      | (?P<op><=|>=|==|!=|<|>)
      | (?P<lparen>\()
      | (?P<rparen>\))
      | (?P<dot>\.)""",
    re.VERBOSE,
)
_KEYWORDS = {"and", "or", "not", "in", "any", "true", "false"}


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    pos, line, line_start = 0, 1, 0
    while pos < len(source):
        m = _TOKEN.match(source, pos)
        col = pos - line_start + 1
        if m is None:
            raise RuleSyntaxError(f"unexpected character {source[pos]!r}", line, col)
        kind, text = m.lastgroup, m.group()
        if kind == "ident" and text in _KEYWORDS:
            kind = "keyword"
        if kind != "ws":
            tokens.append(Token(kind, text, line, col))
        newlines = text.count("\n")
        if newlines:
            line += newlines
            line_start = pos + text.rindex("\n") + 1
        pos = m.end()
    tokens.append(Token("eof", "", line, pos - line_start + 1))
    return tokens


# ---------------------------------------------------------------- AST

@dataclass(frozen=True)
class Literal:
    value: float | str | bool
    line: int
    col: int


@dataclass(frozen=True)
class Field:
    path: str
    line: int
    col: int


@dataclass(frozen=True)
class Not:
    operand: "Node"


@dataclass(frozen=True)
class BoolOp:
    op: str  # and | or
    left: "Node"
    right: "Node"


@dataclass(frozen=True)
class Compare:
    op: str
    left: "Node"
    right: "Node"
    line: int
    col: int


@dataclass(frozen=True)
class Any:
    operand: "Node"
    line: int
    col: int


Node = Literal | Field | Not | BoolOp | Compare | Any

_COMPARE_OPS = {"<", "<=", ">", ">=", "==", "!="}


class _Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0

    @property
    def tok(self) -> Token:
        return self.tokens[self.i]

    def _next(self) -> Token:
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def _is_kw(self, word: str) -> bool:
        return self.tok.kind == "keyword" and self.tok.text == word

    def _fail(self, expected: str) -> RuleSyntaxError:
        tok = self.tok
        found = "end of rule" if tok.kind == "eof" else repr(tok.text)
        return RuleSyntaxError(f"expected {expected}, found {found}", tok.line, tok.col)

    def parse(self) -> Node:
        node = self.or_()
        if self.tok.kind != "eof":
            raise self._fail("'and', 'or' or end of rule")
        return node

    def or_(self) -> Node:
        node = self.and_()
        while self._is_kw("or"):
            self._next()
            node = BoolOp("or", node, self.and_())
        return node

    def and_(self) -> Node:
        node = self.not_()
        while self._is_kw("and"):
            self._next()
            node = BoolOp("and", node, self.not_())
        return node

    def not_(self) -> Node:
        if self._is_kw("not"):
            self._next()
            return Not(self.not_())
        return self.compare()

    def compare(self) -> Node:
        left = self.atom()
        tok = self.tok
        if (tok.kind == "op" and tok.text in _COMPARE_OPS) or self._is_kw("in"):
            self._next()
            return Compare(tok.text, left, self.atom(), tok.line, tok.col)
        return left

    def atom(self) -> Node:
        tok = self.tok
        if tok.kind == "number":
            self._next()
            return Literal(float(tok.text), tok.line, tok.col)
        if tok.kind == "string":
            self._next()
            return Literal(re.sub(r"\\(.)", r"\1", tok.text[1:-1]), tok.line, tok.col)
        if self._is_kw("true") or self._is_kw("false"):
            self._next()
            return Literal(tok.text == "true", tok.line, tok.col)
        if self._is_kw("any"):
            self._next()
            self._expect("lparen", "'(' after any")
            inner = self.or_()
            self._expect("rparen", "')'")
            return Any(inner, tok.line, tok.col)
        if tok.kind == "lparen":
            self._next()
            inner = self.or_()
            self._expect("rparen", "')'")
            return inner
        if tok.kind == "ident":
            parts = [self._next().text]
            while self.tok.kind == "dot":
                self._next()
                if self.tok.kind != "ident":
                    raise self._fail("a field name after '.'")
                parts.append(self._next().text)
            return Field(".".join(parts), tok.line, tok.col)
        raise self._fail("a field, a literal or '('")

    def _expect(self, kind: str, what: str) -> None:
        if self.tok.kind != kind:
            raise self._fail(what)
        self._next()


def parse(source: str) -> Node:
    return _Parser(tokenize(source)).parse()
