"""pc25 Grep With Context Lines -- reference solution.

grep(lines, search_target, lines_around) mimics `grep -C N`: return every line that contains
search_target as a substring, plus up to `lines_around` lines immediately before and after each
match, with overlapping windows merged into one contiguous run, lines kept in their original
order, and no duplicate lines even where windows overlap.

Part2 (reconstructed): mimic GNU grep more closely -- separate non-adjacent runs with a literal
"--" line (only when there's a gap, never a leading/trailing one), and support asymmetric
-B (before) / -A (after) counts instead of one symmetric `lines_around`.

Part3 (reconstructed): a streaming version that works over an ITERATOR of lines (never seen
twice, never seekable) using O(lines_around) auxiliary memory: a bounded ring buffer holds the
pending "before" context, and we don't know a line is worth keeping until we've seen up to
`lines_around` lines after it, at which point it's yielded.
"""

from __future__ import annotations

import sys
from collections import deque
from typing import Iterable, Iterator

# --------------------------------------------------------------------------- Part 1
def grep(lines: list[str], search_target: str, lines_around: int) -> list[str]:
    """Matching lines plus up to `lines_around` lines before/after, overlapping windows merged,
    original order preserved, no duplicates. `lines_around < 0` -> ValueError."""
    if lines_around < 0:
        raise ValueError(f"lines_around must be >= 0, got {lines_around!r}")
    n = len(lines)
    keep = [False] * n
    for i, line in enumerate(lines):
        if search_target in line:
            lo, hi = max(0, i - lines_around), min(n - 1, i + lines_around)
            for j in range(lo, hi + 1):
                keep[j] = True
    return [line for i, line in enumerate(lines) if keep[i]]


# --------------------------------------------------------------------------- Part 2
def grep_grouped(
    lines: list[str], search_target: str, before: int, after: int
) -> list[str]:
    """Like Part1 but with asymmetric -B/-A counts, and non-adjacent kept runs separated by a
    literal "--" line (GNU grep style): never before the first run, never after the last, and
    exactly one "--" between two runs that don't touch/overlap."""
    if before < 0 or after < 0:
        raise ValueError(f"before/after must be >= 0, got before={before!r} after={after!r}")
    n = len(lines)
    keep = [False] * n
    for i, line in enumerate(lines):
        if search_target in line:
            lo, hi = max(0, i - before), min(n - 1, i + after)
            for j in range(lo, hi + 1):
                keep[j] = True

    out: list[str] = []
    prev_kept_idx: int | None = None
    for i, line in enumerate(lines):
        if not keep[i]:
            continue
        if prev_kept_idx is not None and i != prev_kept_idx + 1:
            out.append("--")
        out.append(line)
        prev_kept_idx = i
    return out


# --------------------------------------------------------------------------- Part 3
def grep_stream(lines: Iterable[str], search_target: str, lines_around: int) -> Iterator[str]:
    """Streaming version: `lines` is a one-pass iterator (no len(), no indexing, no re-reading).
    O(lines_around) auxiliary memory: a ring buffer of the last `lines_around` lines (pending
    "before" context) plus a small counter of how many more lines to force-emit as trailing
    "after" context for the most recent match. Yields kept lines in order, no duplicates, no
    "--" separators (that's Part 2's concern; combine both if a caller wants both, not required
    here)."""
    if lines_around < 0:
        raise ValueError(f"lines_around must be >= 0, got {lines_around!r}")
    after_remaining = 0
    # A ring buffer of at most `lines_around + 1` pending [line, keep] pairs. A line only becomes
    # safe to emit once we know whether a match up to `lines_around` lines later will pull it in
    # as trailing context -- so we hold it that long, then flush. Bounded size -> O(lines_around)
    # auxiliary memory regardless of how many lines the iterator produces.
    window: deque[list] = deque()  # each item: [line, keep_bool]
    cap = lines_around + 1

    def _flush_one():
        line, keep = window.popleft()
        return line if keep else None

    for line in lines:
        is_match = search_target in line
        window.append([line, False])
        if is_match:
            lo = max(0, len(window) - 1 - lines_around)
            for k in range(lo, len(window)):
                window[k][1] = True
            after_remaining = lines_around
        elif after_remaining > 0:
            window[-1][1] = True
            after_remaining -= 1
        while len(window) > cap:
            out = _flush_one()
            if out is not None:
                yield out
    while window:
        out = _flush_one()
        if out is not None:
            yield out


# --------------------------------------------------------------------------- line-driven wrappers
def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def part1(lines: list[str]) -> list[str]:
    """'N n' / n text lines / 'Q target around' -> matched lines with context."""
    body, idx = _read_n_lines(lines, 0)
    tag, target, around = lines[idx].split()
    if tag != "Q":
        raise ValueError(f"expected 'Q <target> <around>', got {lines[idx]!r}")
    return grep(body, target, int(around))


def part2(lines: list[str]) -> list[str]:
    """'N n' / n text lines / 'Q target before after' -> grouped output with '--' separators."""
    body, idx = _read_n_lines(lines, 0)
    tag, target, before, after = lines[idx].split()
    if tag != "Q":
        raise ValueError(f"expected 'Q <target> <before> <after>', got {lines[idx]!r}")
    return grep_grouped(body, target, int(before), int(after))


def part3(lines: list[str]) -> list[str]:
    """'N n' / n text lines / 'Q target around' -> matched lines with context, via the streaming
    generator (fed the same lines as a one-pass iterator)."""
    body, idx = _read_n_lines(lines, 0)
    tag, target, around = lines[idx].split()
    if tag != "Q":
        raise ValueError(f"expected 'Q <target> <around>', got {lines[idx]!r}")
    return list(grep_stream(iter(body), target, int(around)))


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    # Body text lines are assumed non-empty (see problem.md's boundary list): like every other
    # problem in this kit, main()'s line transport drops blank lines, so grep inputs containing a
    # genuinely blank line are out of scope for the stdin/stdout format (call grep()/grep_stream()
    # directly with such data instead of going through main()).
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
