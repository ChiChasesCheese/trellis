"""q12 Platform Balance + Radar Rules — reference solution.

Balances are integer cents in a dict.  Part 2 rules are `field OP value` block rules.  Part 3 is a
tiny tokenizer + recursive-descent parser for
    rule := (ACCEPT|BLOCK) if expr ;  expr := and (OR and)* ;  and := primary (AND primary)*
    primary := "(" expr ")" | operand (=|!=) operand | :field:   (bare field = boolean attribute)
Missing field => False for every comparison and boolean (Radar semantics).  First matching rule wins;
no match => accept.
"""
from __future__ import annotations

import re
import sys

# ------------------------------------------------------------------ Part 1: ledger


def parse_query(qs: str) -> dict[str, str]:
    """'a=1&b=2' -> {'a': '1', 'b': '2'}; last duplicate wins; values kept literally (spaces allowed)."""
    fields: dict[str, str] = {}
    for pair in qs.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            fields[k.strip()] = v.strip()
    return fields


def split_command(line: str) -> tuple[str, str] | None:
    """'API: amount=1' -> ('API', 'amount=1'); None if there is no 'PREFIX:' shape."""
    if ":" not in line:
        return None
    prefix, rest = line.split(":", 1)
    return prefix.strip().upper(), rest.strip()


def as_int(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


class Ledger:
    def __init__(self) -> None:
        self.balances: dict[str, int] = {}

    def apply(self, fields: dict[str, str]) -> bool:
        """Apply an API update; False (ignored) when amount/merchant are missing or amount is not an int."""
        amount = as_int(fields.get("amount", ""))
        merchant = fields.get("merchant")
        if amount is None or not merchant:
            return False
        self.balances[merchant] = self.balances.get(merchant, 0) + amount  # may go negative
        return True

    def balance(self, fields: dict[str, str]) -> int:
        return self.balances.get(fields.get("merchant", ""), 0)


# ------------------------------------------------------------------ Part 2: simple block rules

SIMPLE_RULE = re.compile(r"^\s*(\w+)\s*(==|!=|<=|>=|<|>)\s*(.+?)\s*$")


def simple_rule_matches(rule: str, fields: dict[str, str]) -> bool:
    m = SIMPLE_RULE.match(rule)
    if not m:
        return False  # unparsable rule never matches
    field, op, value = m.groups()
    if field not in fields:
        return False  # missing field: no comparison matches, not even !=
    actual, a_int, v_int = fields[field], as_int(fields[field]), as_int(value)
    if a_int is not None and v_int is not None:  # numeric compare when both sides are ints
        lhs, rhs = a_int, v_int
    elif op in ("==", "!="):
        lhs, rhs = actual, value  # otherwise exact string compare
    else:
        return False
    return {"==": lhs == rhs, "!=": lhs != rhs, "<": lhs < rhs, ">": lhs > rhs,
            "<=": lhs <= rhs, ">=": lhs >= rhs}[op]


# ------------------------------------------------------------------ Part 3: Radar rule language

TOKEN = re.compile(r'\s*(?:(\()|(\))|(!=|=)|:([A-Za-z0-9_]+):|"([^"]*)"|([A-Za-z_]+))')


def tokenize(text: str) -> list[tuple[str, str]]:
    """-> [(kind, value)] with kind in {lp, rp, op, field, const, kw}."""
    tokens, pos = [], 0
    while pos < len(text):
        if text[pos:].strip() == "":
            break
        m = TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"bad token at {text[pos:]!r}")
        pos = m.end()
        lp, rp, op, field, const, word = m.groups()
        if lp:
            tokens.append(("lp", "("))
        elif rp:
            tokens.append(("rp", ")"))
        elif op:
            tokens.append(("op", op))
        elif field is not None:
            tokens.append(("field", field))
        elif const is not None:
            tokens.append(("const", const))
        else:
            tokens.append(("kw", word.upper()))
    return tokens


class Parser:
    """Recursive descent over the token list -> AST tuples:
    ("or", a, b) | ("and", a, b) | ("cmp", op, lhs, rhs) | ("bool", name);  operand = ("field", n) | ("const", v)
    """

    def __init__(self, tokens: list[tuple[str, str]]) -> None:
        self.toks, self.i = tokens, 0

    def peek(self) -> tuple[str, str] | None:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def take(self, kind: str) -> str:
        tok = self.peek()
        if tok is None or tok[0] != kind:
            raise ValueError(f"expected {kind}, got {tok}")
        self.i += 1
        return tok[1]

    def expr(self):  # or-level
        node = self.and_expr()
        while self.peek() == ("kw", "OR"):
            self.i += 1
            node = ("or", node, self.and_expr())
        return node

    def and_expr(self):  # AND binds tighter than OR
        node = self.primary()
        while self.peek() == ("kw", "AND"):
            self.i += 1
            node = ("and", node, self.primary())
        return node

    def primary(self):
        tok = self.peek()
        if tok is None:
            raise ValueError("unexpected end of rule")
        if tok == ("lp", "("):
            self.i += 1
            node = self.expr()
            self.take("rp")
            return node
        lhs = self.operand()
        if self.peek() and self.peek()[0] == "op":
            op = self.take("op")
            return ("cmp", op, lhs, self.operand())
        if lhs[0] != "field":
            raise ValueError("a constant cannot stand alone")
        return ("bool", lhs[1])  # bare field = boolean attribute

    def operand(self):
        tok = self.peek()
        if tok and tok[0] in ("field", "const"):
            self.i += 1
            return tok
        raise ValueError(f"expected operand, got {tok}")


def compile_rule(rule: str) -> tuple[bool, tuple]:
    """-> (accept_action, ast). Raises ValueError on a malformed rule."""
    tokens = tokenize(rule)
    if len(tokens) < 3 or tokens[0][0] != "kw" or tokens[0][1] not in ("ACCEPT", "BLOCK") or tokens[1] != ("kw", "IF"):
        raise ValueError(f"rule must start with ACCEPT/BLOCK if: {rule!r}")
    p = Parser(tokens[2:])
    ast = p.expr()
    if p.peek() is not None:
        raise ValueError(f"trailing tokens in {rule!r}")
    return tokens[0][1] == "ACCEPT", ast


def evaluate(node, txn: dict[str, str]) -> bool:
    kind = node[0]
    if kind == "or":
        return evaluate(node[1], txn) or evaluate(node[2], txn)
    if kind == "and":
        return evaluate(node[1], txn) and evaluate(node[2], txn)
    if kind == "bool":
        return txn.get(node[1], "").lower() == "true"  # missing -> False
    _, op, lhs, rhs = node
    l = txn.get(lhs[1]) if lhs[0] == "field" else lhs[1]
    r = txn.get(rhs[1]) if rhs[0] == "field" else rhs[1]
    if l is None or r is None:
        return False  # missing field: comparison is False even for !=
    return (l == r) if op == "=" else (l != r)


_COMPILED: dict[str, tuple[bool, tuple]] = {}  # rule text -> compiled, so 10^5 txns don't re-parse


def evaluate_rule(rule: str, txn: dict[str, str]) -> tuple[bool, bool]:
    """-> (matched, accept_action)."""
    if rule not in _COMPILED:
        _COMPILED[rule] = compile_rule(rule)
    accept, ast = _COMPILED[rule]
    return evaluate(ast, txn), accept


def should_accept_transaction(transaction: dict[str, str], rules: list[str]) -> bool:
    for rule in rules:  # first matching rule wins
        matched, accept = evaluate_rule(rule, transaction)
        if matched:
            return accept
    return True  # no rule matched -> accept


# ------------------------------------------------------------------ drivers


def run(lines: list[str], part: int) -> list[str]:
    ledger, rules, out = Ledger(), [], []
    for raw in lines:
        cmd = split_command(raw.strip())
        if cmd is None:
            continue
        prefix, rest = cmd
        if prefix == "API":
            fields = parse_query(rest)
            if part == 2 and any(simple_rule_matches(r, fields) for r in rules):
                continue  # blocked: balance untouched
            ledger.apply(fields)
        elif prefix == "BAL":
            out.append(str(ledger.balance(parse_query(rest))))
        elif prefix == "RULE" and part >= 2:
            if part == 2:
                rules.append(rest)
            else:
                try:
                    evaluate_rule(rest, {})  # validate syntax once; malformed rules are skipped
                    rules.append(rest)
                except ValueError:
                    pass
        elif prefix == "TXN" and part == 3:
            out.append("ACCEPT" if should_accept_transaction(parse_query(rest), rules) else "BLOCK")
    return out


def part1(lines: list[str]) -> list[str]:
    return run(lines, 1)


def part2(lines: list[str]) -> list[str]:
    return run(lines, 2)


def part3(lines: list[str]) -> list[str]:
    return run(lines, 3)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
