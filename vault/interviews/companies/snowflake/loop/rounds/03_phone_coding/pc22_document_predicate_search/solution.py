"""pc22 Document Predicate Search Engine -- reference solution.

An inverted index maps each word -> the set of doc ids that contain it, maintained incrementally
by INSERT_DOC / DELETE_DOC so every query is answered by set algebra over that index (never by
scanning every document): OR is set union, AND is set intersection, NOT is "the universe of doc
ids currently in the index" minus the operand set.

Part1 (one-hand preview): CHECK_CONTAINS "a b c" means OR over the words -- a plain union of
each word's posting set.
Part2 (reconstructed): the query becomes a real boolean expression with AND/OR keywords and
the usual precedence, AND binding tighter than OR (so "a AND b OR c" is "(a AND b) OR c").
NOT and parentheses are deliberately rejected here with ValueError -- they are not introduced
until Part3, and a Part2 caller should get a clear error rather than a silently-wrong parse.
Part3 (reconstructed): NOT and parenthesised grouping, via a small recursive-descent parser
(grammar: expr := term (OR term)* ; term := factor (AND factor)* ; factor := NOT factor
| WORD | '(' expr ')'), plus DELETE_DOC to remove a document (and its postings) from the index.
"""

from __future__ import annotations

import re
import sys

_TOKEN_RE = re.compile(r"\(|\)|[^\s()]+")


def _tokenize(expr: str) -> list[str]:
    return _TOKEN_RE.findall(expr)


class _Parser:
    """Recursive-descent parser for expr := term (OR term)* ; term := factor (AND factor)* ;
    factor := NOT factor | WORD | '(' expr ')'."""

    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self) -> str:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self) -> tuple:
        node = self._expr()
        if self.pos != len(self.tokens):
            raise ValueError(f"unexpected trailing token {self._peek()!r} in query")
        return node

    def _expr(self) -> tuple:
        node = self._term()
        while self._peek() == "OR":
            self._advance()
            node = ("OR", node, self._term())
        return node

    def _term(self) -> tuple:
        node = self._factor()
        while self._peek() == "AND":
            self._advance()
            node = ("AND", node, self._factor())
        return node

    def _factor(self) -> tuple:
        tok = self._peek()
        if tok is None:
            raise ValueError("unexpected end of query")
        if tok == "NOT":
            self._advance()
            return ("NOT", self._factor())
        if tok == "(":
            self._advance()
            node = self._expr()
            if self._peek() != ")":
                raise ValueError("expected closing ')'")
            self._advance()
            return node
        if tok in ("AND", "OR", ")"):
            raise ValueError(f"unexpected token {tok!r} in query")
        self._advance()
        return ("WORD", tok)


def _parse_query(expr: str) -> tuple:
    return _Parser(_tokenize(expr)).parse()


def _eval_sets(node: tuple, index: dict, universe: set) -> set:
    kind = node[0]
    if kind == "WORD":
        return set(index.get(node[1], ()))
    if kind == "AND":
        return _eval_sets(node[1], index, universe) & _eval_sets(node[2], index, universe)
    if kind == "OR":
        return _eval_sets(node[1], index, universe) | _eval_sets(node[2], index, universe)
    if kind == "NOT":
        return universe - _eval_sets(node[1], index, universe)
    raise ValueError(f"bad AST node {node!r}")  # pragma: no cover -- defensive


def _reject_not_and_parens(tokens: list[str]) -> None:
    if "NOT" in tokens or "(" in tokens or ")" in tokens:
        raise ValueError("NOT and parentheses are not supported until Part3")


class DocumentIndex:
    """Inverted-index-backed document store: word -> set of doc ids containing it."""

    def __init__(self) -> None:
        self._docs: dict[int, set[str]] = {}
        self._index: dict[str, set[int]] = {}

    def insert_doc(self, doc_id: int, words: list[str]) -> None:
        """Re-inserting an existing id replaces that document (old postings are removed first)."""
        self.delete_doc(doc_id)
        word_set = set(words)
        self._docs[doc_id] = word_set
        for w in word_set:
            self._index.setdefault(w, set()).add(doc_id)

    def delete_doc(self, doc_id: int) -> None:
        """No-op if doc_id was never inserted (idempotent)."""
        words = self._docs.pop(doc_id, None)
        if words is None:
            return
        for w in words:
            bucket = self._index.get(w)
            if bucket is not None:
                bucket.discard(doc_id)
                if not bucket:
                    del self._index[w]

    def check_contains_or(self, query: str) -> list[int]:
        """Part1: OR over the space-separated words in `query` (no AND/OR/NOT keywords)."""
        result: set[int] = set()
        for w in query.split():
            result |= self._index.get(w, set())
        return sorted(result)

    def check_contains_bool(self, query: str) -> list[int]:
        """Part2: AND/OR with AND binding tighter. NOT and parentheses raise ValueError."""
        tokens = _tokenize(query)
        _reject_not_and_parens(tokens)
        node = _Parser(tokens).parse()
        return sorted(_eval_sets(node, self._index, set(self._docs)))

    def check_contains_full(self, query: str) -> list[int]:
        """Part3: full grammar (AND/OR/NOT/parentheses)."""
        node = _parse_query(query)
        return sorted(_eval_sets(node, self._index, set(self._docs)))


# --------------------------------------------------------------------------- line-driven wrappers
def _format_ids(ids: list[int]) -> str:
    return "NONE" if not ids else " ".join(map(str, ids))


def _split_check_contains(line: str) -> str:
    """'CHECK_CONTAINS "a b c"' -> 'a b c' (strip the command name and the surrounding quotes)."""
    rest = line[len("CHECK_CONTAINS "):].strip()
    if len(rest) < 2 or rest[0] != '"' or rest[-1] != '"':
        raise ValueError(f"malformed CHECK_CONTAINS line {line!r} (query must be quoted)")
    return rest[1:-1]


def part1(lines: list[str]) -> list[str]:
    """commands: 'INSERT_DOC id w1 w2 ...' / 'CHECK_CONTAINS "a b c"' (OR over words)."""
    idx = DocumentIndex()
    out = []
    for line in lines:
        if line.startswith("INSERT_DOC "):
            parts = line.split()
            idx.insert_doc(int(parts[1]), parts[2:])
        elif line.startswith("CHECK_CONTAINS "):
            out.append(_format_ids(idx.check_contains_or(_split_check_contains(line))))
        else:
            raise ValueError(f"unknown command {line!r}")
    return out


def part2(lines: list[str]) -> list[str]:
    """same commands as Part1, but CHECK_CONTAINS's query is a full AND/OR boolean expression."""
    idx = DocumentIndex()
    out = []
    for line in lines:
        if line.startswith("INSERT_DOC "):
            parts = line.split()
            idx.insert_doc(int(parts[1]), parts[2:])
        elif line.startswith("CHECK_CONTAINS "):
            out.append(_format_ids(idx.check_contains_bool(_split_check_contains(line))))
        else:
            raise ValueError(f"unknown command {line!r}")
    return out


def part3(lines: list[str]) -> list[str]:
    """adds 'DELETE_DOC id'; CHECK_CONTAINS supports NOT and parentheses."""
    idx = DocumentIndex()
    out = []
    for line in lines:
        if line.startswith("INSERT_DOC "):
            parts = line.split()
            idx.insert_doc(int(parts[1]), parts[2:])
        elif line.startswith("DELETE_DOC "):
            idx.delete_doc(int(line.split()[1]))
        elif line.startswith("CHECK_CONTAINS "):
            out.append(_format_ids(idx.check_contains_full(_split_check_contains(line))))
        else:
            raise ValueError(f"unknown command {line!r}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
