"""qA14 LC 150 Evaluate Reverse Polish Notation — YOUR implementation.

RECONSTRUCTED TRAINING PROBLEM (title-only mirror entry; Part 1's algorithm is LeetCode's own
public problem, Parts 2-3's API/output shape is this repo's own) — see problem.md's warning
block.
"""
from __future__ import annotations

import sys

OPERATORS = frozenset({"+", "-", "*", "/"})


def _truncate_divide(a: int, b: int) -> int:
    """a / b, truncated toward zero (not floor -- Python's // floors toward -inf)."""
    # TODO
    return 0


def evaluate_rpn(tokens: list[str]) -> int:
    """Part 1: standard LC 150. Assume tokens is a valid RPN expression (LC constraints)."""
    # TODO
    return 0


def evaluate_rpn_trace(tokens: list[str]) -> list[str]:
    """Part 2: same evaluation, assume-valid input. One '<a> <op> <b> = <result>' line per
    operator applied (in order), then a final 'RESULT <value>' line."""
    # TODO
    return []


def evaluate_rpn_safe(tokens: list[str]) -> str:
    """Part 3: input NOT assumed valid; never raise. Returns str(result) on success, or
    'ERROR <code>' with code in {empty_input, unknown_token, insufficient_operands,
    division_by_zero, trailing_operands} -- first applicable failure while scanning left to
    right wins (see problem.md's priority order)."""
    # TODO
    return "ERROR empty_input"


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
