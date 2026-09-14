"""qA14 LC 150 Evaluate Reverse Polish Notation — reference solution.

Part 1 is the LC signature (assume-valid input). Part 2 reuses the same arithmetic but returns a
step-by-step trace. Part 3 reuses the same arithmetic again but never raises, returning a
diagnostic 'ERROR <code>' string for any of five distinct malformed-input reasons instead.
"""
from __future__ import annotations

import re
import sys

OPERATORS = frozenset({"+", "-", "*", "/"})
_OPERAND_RE = re.compile(r"^-?[0-9]+$")


def _truncate_divide(a: int, b: int) -> int:
    """a / b, truncated toward zero (not floor -- Python's // floors toward -inf)."""
    quotient = abs(a) // abs(b)
    return -quotient if (a < 0) != (b < 0) else quotient


def _apply(a: int, b: int, op: str) -> int:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return _truncate_divide(a, b)


def evaluate_rpn(tokens: list[str]) -> int:
    """Part 1: standard LC 150. Assume tokens is a valid RPN expression (LC constraints)."""
    stack: list[int] = []
    for token in tokens:
        if token in OPERATORS:
            b = stack.pop()
            a = stack.pop()
            stack.append(_apply(a, b, token))
        else:
            stack.append(int(token))
    return stack[-1]


def evaluate_rpn_trace(tokens: list[str]) -> list[str]:
    """Part 2: same evaluation, assume-valid input. One '<a> <op> <b> = <result>' line per
    operator applied (in order), then a final 'RESULT <value>' line."""
    stack: list[int] = []
    lines: list[str] = []
    for token in tokens:
        if token in OPERATORS:
            b = stack.pop()
            a = stack.pop()
            result = _apply(a, b, token)
            lines.append(f"{a} {token} {b} = {result}")
            stack.append(result)
        else:
            stack.append(int(token))
    lines.append(f"RESULT {stack[-1]}")
    return lines


def evaluate_rpn_safe(tokens: list[str]) -> str:
    """Part 3: input NOT assumed valid; never raise. Returns str(result) on success, or
    'ERROR <code>' -- first applicable failure while scanning left to right wins:
    empty_input > unknown_token > insufficient_operands > division_by_zero > trailing_operands.
    """
    if not tokens:
        return "ERROR empty_input"

    stack: list[int] = []
    for token in tokens:
        if token in OPERATORS:
            if len(stack) < 2:
                return "ERROR insufficient_operands"
            b = stack.pop()
            a = stack.pop()
            if token == "/" and b == 0:
                return "ERROR division_by_zero"
            stack.append(_apply(a, b, token))
        elif _OPERAND_RE.fullmatch(token):
            stack.append(int(token))
        else:
            return "ERROR unknown_token"

    if len(stack) != 1:
        return "ERROR trailing_operands"
    return str(stack[0])


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines or not lines[0].strip():
        return
    part = int(lines[0].split()[1])
    tokens = lines[1].split() if len(lines) > 1 else []
    if part == 1:
        out = [str(evaluate_rpn(tokens))]
    elif part == 2:
        out = evaluate_rpn_trace(tokens)
    else:
        out = [evaluate_rpn_safe(tokens)]
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
