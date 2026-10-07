"""Check a parsed rule against the field table, then evaluate it. No ``eval``, no attribute access."""
from __future__ import annotations

import operator
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any as AnyType

from rulelang.rules import parser
from rulelang.rules.fields import BOOL, FIELDS, LOOP_ITEMS, NUM, STR, STRINGS, Scope
from rulelang.rules.parser import RuleSyntaxError

_ORDER = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge}


def _fields_in(node: parser.Node) -> Iterator[parser.Field]:
    if isinstance(node, parser.Field):
        yield node
    elif isinstance(node, (parser.Not, parser.Any)):
        yield from _fields_in(node.operand)
    elif isinstance(node, (parser.BoolOp, parser.Compare)):
        yield from _fields_in(node.left)
        yield from _fields_in(node.right)


@dataclass(frozen=True)
class CompiledRule:
    name: str
    source: str
    root: parser.Node

    def matches(self, scope: Scope) -> bool:
        return bool(_eval(self.root, scope))


def compile_rule(name: str, source: str) -> CompiledRule:
    """Parse and type-check ``source``; raises ``RuleSyntaxError`` naming the rule and the position."""
    try:
        root = parser.parse(source)
        if _check(root, None) != BOOL:
            raise RuleSyntaxError("a rule must be a true/false condition")
    except RuleSyntaxError as exc:
        raise RuleSyntaxError(exc.reason, exc.line, exc.column, rule=name) from None
    return CompiledRule(name, source, root)


def _check(node: parser.Node, loop: str | None) -> str:
    """Return the node's type, raising on unknown fields and mismatched operands."""
    if isinstance(node, parser.Literal):
        return BOOL if isinstance(node.value, bool) else NUM if isinstance(node.value, float) else STR
    if isinstance(node, parser.Field):
        spec = FIELDS.get(node.path)
        if spec is None:
            raise RuleSyntaxError(f"unknown field {node.path!r}", node.line, node.col)
        if spec.loop and spec.loop != loop:
            raise RuleSyntaxError(f"{node.path!r} can only be used inside any(...)", node.line, node.col)
        return spec.type
    if isinstance(node, parser.Not):
        return _need(_check(node.operand, loop), BOOL, node.operand)
    if isinstance(node, parser.BoolOp):
        _need(_check(node.left, loop), BOOL, node.left)
        return _need(_check(node.right, loop), BOOL, node.right)
    if isinstance(node, parser.Any):
        loops = {f.path.split(".")[0] for f in _fields_in(node.operand) if FIELDS.get(f.path) and FIELDS[f.path].loop}
        if len(loops) != 1:
            raise RuleSyntaxError("any(...) must use exactly one of link.* or recipient.*", node.line, node.col)
        return _need(_check(node.operand, loops.pop()), BOOL, node.operand)
    left, right = _check(node.left, loop), _check(node.right, loop)
    if node.op == "in":
        if left != STR or right not in (STRINGS, STR):
            raise RuleSyntaxError("'in' needs a string on the left and a list or string on the right", node.line, node.col)
    elif node.op in _ORDER:
        if left != NUM or right != NUM:
            raise RuleSyntaxError(f"{node.op!r} compares numbers", node.line, node.col)
    elif left != right:
        raise RuleSyntaxError(f"cannot compare {left} with {right}", node.line, node.col)
    return BOOL


def _need(actual: str, wanted: str, node: parser.Node) -> str:
    if actual != wanted:
        line, col = getattr(node, "line", 1), getattr(node, "col", 1)
        raise RuleSyntaxError(f"expected a true/false condition, found a {actual}", line, col)
    return wanted


def _eval(node: parser.Node, scope: Scope) -> AnyType:
    if isinstance(node, parser.Literal):
        return node.value
    if isinstance(node, parser.Field):
        return FIELDS[node.path].get(scope)
    if isinstance(node, parser.Not):
        return not _eval(node.operand, scope)
    if isinstance(node, parser.BoolOp):
        left = _eval(node.left, scope)
        if node.op == "and":
            return bool(left) and bool(_eval(node.right, scope))
        return bool(left) or bool(_eval(node.right, scope))
    if isinstance(node, parser.Any):
        var = next(f.path.split(".")[0] for f in _fields_in(node.operand) if FIELDS[f.path].loop)
        return any(_eval(node.operand, scope.bind(var, item)) for item in LOOP_ITEMS[var](scope.event))
    left, right = _eval(node.left, scope), _eval(node.right, scope)
    if left is None or right is None:  # unknown data never matches, whatever the operator
        return False
    if node.op == "in":
        return left in right
    if node.op == "==":
        return left == right
    if node.op == "!=":
        return left != right
    return _ORDER[node.op](left, right)
