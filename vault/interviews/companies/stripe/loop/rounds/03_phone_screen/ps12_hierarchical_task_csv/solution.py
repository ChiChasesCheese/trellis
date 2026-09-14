"""ps12 Hierarchical Task CSV — reference solution.

Pipeline shared by every part: `_parse_rows` (RFC4180-aware CSV parse into `Row` records) ->
`_build_tree` (adjacency list `children[task_id] -> [child_id, ...]` in input order, plus a
`name` lookup) -> a per-part render step. Parts 1-4 mirror the real interview's unlock order
(root-only -> naive uniform connector -> fixed last-child connector -> arbitrary depth), but
`_render_forest` (Part 3/4's renderer) is a single general tree walk: a Part 3 implementation
written this way already *is* Part 4, since the connector rule never changes with depth.

The renderer is an explicit-stack (iterative) DFS, not recursion -- nesting depth can reach
len(lines) (a single root with a 10**5-long chain of nested singleton subtasks), which would blow
Python's default recursion limit if implemented as naive recursion.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from typing import NamedTuple

NON_FINAL = "├─ "  # connector for a child that has a later sibling
FINAL = "└─ "  # connector for the last child in its parent's list
NON_FINAL_ANCESTOR = "│  "  # continuation bar carried past a non-final ancestor level
FINAL_ANCESTOR = "   "  # (three spaces) continuation carried past a final ancestor level


class Row(NamedTuple):
    kind: str  # "task" (root) or "subtask" (child)
    task_id: str
    name: str
    parent_id: str | None  # None for a root
    order: int  # input line index (timestamp is NOT the sort key -- see problem.md)


# ------------------------------------------------------------------ parsing
def _parse_rows(lines: list[str]) -> list[Row]:
    """CSV-parse (via the `csv` module, so quoted commas/escaped quotes in task_name work) each
    non-blank line into a Row. A 4-field row is a root ('task'); a 5-field row is a child
    ('subtask'). `timestamp` (fields[0]) is read and discarded -- it is never a sort key."""
    out: list[Row] = []
    for i, raw in enumerate(lines):
        if not raw.strip():
            continue
        fields = next(csv.reader([raw]))
        kind = fields[1]
        if kind == "task":
            _timestamp, _kind, task_id, name = fields
            out.append(Row(kind, task_id, name, None, i))
        elif kind == "subtask":
            _timestamp, _kind, parent_id, task_id, name = fields
            out.append(Row(kind, task_id, name, parent_id, i))
        else:
            raise ValueError(f"unknown row kind: {kind!r}")
    return out


def _build_tree(rows: list[Row]) -> tuple[list[str], dict[str, list[str]], dict[str, str]]:
    """roots (task_ids of 'task' rows, input order), children (adjacency list, input order per
    parent), name (task_id -> task_name, every row contributes one entry)."""
    roots = [r.task_id for r in rows if r.kind == "task"]
    name = {r.task_id: r.name for r in rows}
    children: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        if r.kind == "subtask":
            children[r.parent_id].append(r.task_id)
    return roots, children, name


# ------------------------------------------------------------------ rendering
def _render_forest(roots: list[str], children: dict[str, list[str]], name: dict[str, str]) -> list[str]:
    """Part 3/4's rule: correct '├─ '/'└─ ' connector at every level, with the matching
    continuation prefix ('│  ' vs three spaces) carried to every descendant. Iterative
    (explicit-stack) DFS so nesting depth is not bounded by Python's recursion limit."""
    out: list[str] = []
    for root in roots:
        out.append(f"{root} {name[root]}")
        stack: list[tuple[str, str, bool]] = []  # (task_id, ancestor_prefix, is_last_child)
        kids = children.get(root, [])
        for i in range(len(kids) - 1, -1, -1):  # push in reverse -> pop in input order
            stack.append((kids[i], "", i == len(kids) - 1))
        while stack:
            task_id, ancestor_prefix, is_last = stack.pop()
            connector = FINAL if is_last else NON_FINAL
            out.append(f"{ancestor_prefix}{connector}{task_id} {name[task_id]}")
            next_prefix = ancestor_prefix + (FINAL_ANCESTOR if is_last else NON_FINAL_ANCESTOR)
            grandchildren = children.get(task_id, [])
            for i in range(len(grandchildren) - 1, -1, -1):
                stack.append((grandchildren[i], next_prefix, i == len(grandchildren) - 1))
    return out


# ------------------------------------------------------------------ parts
def part1(lines: list[str]) -> list[str]:
    """Root-only input: 'task_id task_name' per 'task' row, in input order."""
    return [f"{r.task_id} {r.name}" for r in _parse_rows(lines) if r.kind == "task"]


def part2(lines: list[str]) -> list[str]:
    """Roots + direct subtasks only. Every subtask gets '├─ ', including the list's last one --
    intentionally not yet fixed (that's part3)."""
    roots, children, name = _build_tree(_parse_rows(lines))
    out: list[str] = []
    for root in roots:
        out.append(f"{root} {name[root]}")
        for child_id in children.get(root, []):
            out.append(f"{NON_FINAL}{child_id} {name[child_id]}")
    return out


def part3(lines: list[str]) -> list[str]:
    """Same input shape as part2; the last subtask in each list now gets '└─ '."""
    roots, children, name = _build_tree(_parse_rows(lines))
    return _render_forest(roots, children, name)


def part4(lines: list[str]) -> list[str]:
    """Arbitrary nesting depth. Identical rule/renderer to part3 -- a correctly generalized part3
    already handles this; the split exists because that's how the interview unlocked it."""
    roots, children, name = _build_tree(_parse_rows(lines))
    return _render_forest(roots, children, name)


# ------------------------------------------------------------------ I/O
PARTS = {"PART 1": part1, "PART 2": part2, "PART 3": part3, "PART 4": part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    if header not in PARTS:
        raise ValueError(f"unknown header: {header!r}")
    out = PARTS[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
