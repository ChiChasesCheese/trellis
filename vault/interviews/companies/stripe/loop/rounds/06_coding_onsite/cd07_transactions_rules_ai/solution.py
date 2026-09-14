"""cd07 Transactions + rules (AI Programming Exercise) — reference solution.

Part 1: `field == value` only. Part 2: adds !=, >, <, >=, <=, and `field in [v1, v2, ...]` (one
comparison per rule). Part 3: adds AND/OR/NOT + parentheses, `not` > `and` > `or`, and per-rule
`ERROR line k: <reason>` for rules that fail to parse (skipped, not fatal).

Each part reuses the same tokenizer/parser/evaluator; `part` only widens which grammar productions
are legal, so Part n is always a strict subset of Part n+1's grammar.
"""

from __future__ import annotations

import re
import sys

FIELDS = {"id", "amount", "currency", "country", "card_brand", "merchant"}
KEYWORDS = {"and", "or", "not", "in"}

RULE_RE = re.compile(r"^(ALLOW|BLOCK)\s+if\s+(.+)$")
TOKEN_RE = re.compile(
    r"(?P<LP>\()|(?P<RP>\))|(?P<LB>\[)|(?P<RB>\])|(?P<COMMA>,)"
    r"|(?P<OP>==|!=|>=|<=|>|<)|(?P<WORD>[A-Za-z0-9_.]+)"
)


class RuleError(ValueError):
    """A rule line that fails to tokenize or parse."""


# ---------------------------------------------------------------- tokenizer
def _tokenize(text: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    i, n = 0, len(text)
    while i < n:
        if text[i].isspace():
            i += 1
            continue
        m = TOKEN_RE.match(text, i)
        if not m:
            raise RuleError(f"unexpected character {text[i]!r}")
        tokens.append((m.lastgroup, m.group(m.lastgroup)))
        i = m.end()
    return tokens


# ---------------------------------------------------------------- parser
class _Parser:
    """Recursive descent: expr := or_expr; or_expr := and_expr ('or' and_expr)*;
    and_expr := unary ('and' unary)*; unary := 'not' unary | primary;
    primary := '(' expr ')' | comparison; comparison := operand OP operand | operand 'in' '[' .. ']'.
    AST nodes: ('and', l, r) | ('or', l, r) | ('not', x) | ('cmp', op, left, right) | ('in', left, items).
    """

    def __init__(self, tokens: list[tuple[str, str]], part: int, allow_bool: bool):
        self.tokens = tokens
        self.pos = 0
        self.part = part
        self.allow_bool = allow_bool

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _is_kw(self, tok, kw: str) -> bool:
        return tok is not None and tok[0] == "WORD" and tok[1].lower() == kw

    def parse(self):
        node = self._or() if self.allow_bool else self._comparison()
        if self.pos != len(self.tokens):
            raise RuleError(f"unexpected token {self._peek()[1]!r}")
        return node

    def _or(self):
        node = self._and()
        while self._is_kw(self._peek(), "or"):
            self._advance()
            node = ("or", node, self._and())
        return node

    def _and(self):
        node = self._not()
        while self._is_kw(self._peek(), "and"):
            self._advance()
            node = ("and", node, self._not())
        return node

    def _not(self):
        if self._is_kw(self._peek(), "not"):
            self._advance()
            return ("not", self._not())
        return self._primary()

    def _primary(self):
        tok = self._peek()
        if tok is None:
            raise RuleError("unexpected end of condition")
        if tok[0] == "LP":
            self._advance()
            node = self._or()
            if not (self._peek() and self._peek()[0] == "RP"):
                raise RuleError("missing closing ')'")
            self._advance()
            return node
        return self._comparison()

    def _operand(self) -> str:
        tok = self._peek()
        if tok is None or tok[0] != "WORD":
            raise RuleError("expected a field or value")
        if tok[1].lower() in KEYWORDS:
            raise RuleError(f"unexpected keyword {tok[1]!r}")
        self._advance()
        return tok[1]

    def _comparison(self):
        left = self._operand()
        tok = self._peek()
        if tok and tok[0] == "OP":
            op = self._advance()[1]
            if self.part == 1 and op != "==":
                raise RuleError("part 1 only supports '=='")
            right = self._operand()
            return ("cmp", op, left, right)
        if self._is_kw(tok, "in"):
            if self.part == 1:
                raise RuleError("part 1 does not support 'in'")
            self._advance()
            if not (self._peek() and self._peek()[0] == "LB"):
                raise RuleError("expected '[' after 'in'")
            self._advance()
            items: list[str] = []
            if not (self._peek() and self._peek()[0] == "RB"):
                items.append(self._operand())
                while self._peek() and self._peek()[0] == "COMMA":
                    self._advance()
                    items.append(self._operand())
            if not (self._peek() and self._peek()[0] == "RB"):
                raise RuleError("missing closing ']'")
            self._advance()
            return ("in", left, items)
        raise RuleError("expected a comparison operator or 'in' after field")


def parse_condition(text: str, part: int):
    tokens = _tokenize(text)
    if not tokens:
        raise RuleError("empty condition")
    return _Parser(tokens, part, allow_bool=(part == 3)).parse()


# ---------------------------------------------------------------- evaluation
def _resolve(token: str, txn: dict):
    return txn[token] if token in FIELDS else token


def _looks_int(x) -> bool:
    try:
        int(str(x).strip())
        return True
    except ValueError:
        return False


def _compare(op: str, lv, rv) -> bool:
    if op in ("==", "!="):
        eq = int(lv) == int(rv) if (_looks_int(lv) and _looks_int(rv)) else str(lv) == str(rv)
        return eq if op == "==" else not eq
    l, r = int(lv), int(rv)  # ordering ops: numeric only (spec: exercised on `amount`)
    if op == ">":
        return l > r
    if op == "<":
        return l < r
    if op == ">=":
        return l >= r
    return l <= r  # "<="


def _eval(node, txn: dict) -> bool:
    kind = node[0]
    if kind == "and":
        return _eval(node[1], txn) and _eval(node[2], txn)
    if kind == "or":
        return _eval(node[1], txn) or _eval(node[2], txn)
    if kind == "not":
        return not _eval(node[1], txn)
    if kind == "cmp":
        _, op, left, right = node
        return _compare(op, _resolve(left, txn), _resolve(right, txn))
    # kind == "in"
    _, left, items = node
    return str(_resolve(left, txn)) in {str(_resolve(v, txn)) for v in items}


# ---------------------------------------------------------------- parsing input sections
def _split_sections(lines: list[str]) -> tuple[list[str], list[str]]:
    rules: list[str] = []
    txns: list[str] = []
    current: str | None = None
    for raw in lines:
        ln = raw.strip()
        if not ln:
            continue
        if ln == "RULES":
            current = "RULES"
            continue
        if ln == "TRANSACTIONS":
            current = "TRANSACTIONS"
            continue
        (rules if current == "RULES" else txns if current == "TRANSACTIONS" else []).append(ln)
    return rules, txns


def _parse_txn(line: str) -> dict:
    parts = [p.strip() for p in line.split(",")]
    while len(parts) < 6:
        parts.append("")
    tid, amount, currency, country, card_brand, merchant = parts[:6]
    try:
        amount_val: object = int(amount)
    except ValueError:
        amount_val = amount  # left as string; comparisons against it just won't match numerically
    return {
        "id": tid,
        "amount": amount_val,
        "currency": currency,
        "country": country,
        "card_brand": card_brand,
        "merchant": merchant,
    }


def _evaluate(lines: list[str], part: int) -> list[str]:
    rule_lines, txn_lines = _split_sections(lines)
    out: list[str] = []
    compiled: list[tuple[int, str, tuple]] = []  # (rule line no., ALLOW|BLOCK, ast)

    for i, raw in enumerate(rule_lines, start=1):
        m = RULE_RE.match(raw)
        if not m:
            if part == 3:
                out.append(f"ERROR line {i}: rule must start with 'ALLOW if' or 'BLOCK if'")
            continue
        action, cond_text = m.group(1), m.group(2)
        try:
            ast = parse_condition(cond_text, part)
        except RuleError as e:
            if part == 3:
                out.append(f"ERROR line {i}: {e}")
            continue
        compiled.append((i, action, ast))

    for raw in txn_lines:
        txn = _parse_txn(raw)
        decision, suffix = "ALLOW", ""
        for line_no, action, ast in compiled:
            if _eval(ast, txn):
                decision, suffix = action, f" (rule {line_no})"
                break
        out.append(f"{txn['id']} {decision}{suffix}")
    return out


def part1(lines: list[str]) -> list[str]:
    return _evaluate(lines, 1)


def part2(lines: list[str]) -> list[str]:
    return _evaluate(lines, 2)


def part3(lines: list[str]) -> list[str]:
    return _evaluate(lines, 3)


PARTS = {1: part1, 2: part2, 3: part3}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw_lines = stdin.read().splitlines()
    lines = [ln for ln in raw_lines if ln.strip()]
    out: list[str] = []
    if lines and lines[0].strip().upper().startswith("PART"):
        part = int(lines[0].split()[1])
        out = PARTS[part](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
