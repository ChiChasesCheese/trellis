"""ps12 Hierarchical Task CSV — YOUR implementation.

Input shape (see problem.md): stdin is `PART n`, then CSV lines — a root record
`timestamp,task,task_id,task_name` (4 fields) or a child record
`timestamp,subtask,parent_id,task_id,task_name` (5 fields). Parse with the `csv` module (task
names may be quoted and contain commas / escaped quotes) -- never hand-roll `line.split(",")`.
"""

from __future__ import annotations

import sys


def part1(lines: list[str]) -> list[str]:
    """Input contains only root ('task') records. Return 'task_id task_name' per record, in
    input order."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Roots plus their direct subtasks only (one level, no subtask-of-subtask yet). For each
    root (input order): print the root line, then each subtask in input order, ALL prefixed
    '├─ ' (uniform connector -- the last subtask does NOT yet get '└─ ', that's part3)."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Same input shape as part2. Now the LAST subtask in each root's list gets '└─ ' instead of
    '├─ '; earlier subtasks keep '├─ '."""
    # TODO
    return []


def part4(lines: list[str]) -> list[str]:
    """Subtasks may now have their own subtasks, to any depth. Same connector rule as part3,
    generalized: a non-final child's descendants get an extra '│  ' per such ancestor level; a
    final child's descendants get an extra '   ' (three spaces) per such ancestor level. Use an
    explicit stack, not naive recursion -- depth can reach len(lines)."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    raw = stdin.read().splitlines()
    if not raw:
        return
    header, body = raw[0].strip(), raw[1:]
    parts = {"PART 1": part1, "PART 2": part2, "PART 3": part3, "PART 4": part4}
    if header not in parts:
        raise ValueError(f"unknown header: {header!r}")
    out = parts[header](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
