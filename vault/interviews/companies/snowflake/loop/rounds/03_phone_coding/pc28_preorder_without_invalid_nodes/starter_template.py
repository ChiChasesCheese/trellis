"""pc28 Preorder Traversal Without Invalid Nodes -- YOUR implementation. Run the tests against
this file with IMPL=starter.

n nodes 0..n-1, edges = [(parent, child)] in child-visit order, a root, and invalid nodes.
Preorder-traverse skipping invalid nodes. MUST be iterative (explicit stack) -- depth up to 1e5.
"""

from __future__ import annotations

import sys


def preorder_skip_invalid_splice(
    n: int, edges: list[tuple[int, int]], root: int, invalid: list[int]
) -> list[int]:
    """Part1 (reconstructed reading #1): an invalid node is omitted, but its children are still
    traversed. Iterative."""
    # TODO
    return []


def preorder_skip_invalid_prune(
    n: int, edges: list[tuple[int, int]], root: int, invalid: list[int]
) -> list[int]:
    """Part2 (reconstructed reading #2): an invalid node prunes its whole subtree. Iterative."""
    # TODO
    return []


def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def _parse_common(lines: list[str]) -> tuple[int, list[tuple[int, int]], int, list[int]]:
    tag, n = lines[0].split()
    if tag != "NODES":
        raise ValueError(f"expected 'NODES <n>', got {lines[0]!r}")
    n = int(n)
    edge_lines, idx = _read_n_lines(lines, 1)
    edges = []
    for el in edge_lines:
        p, c = el.split()
        edges.append((int(p), int(c)))
    tag, root = lines[idx].split()
    if tag != "ROOT":
        raise ValueError(f"expected 'ROOT <root>', got {lines[idx]!r}")
    root = int(root)
    idx += 1
    invalid_line = lines[idx].split()
    if invalid_line[0] != "INVALID":
        raise ValueError(f"expected 'INVALID ...', got {lines[idx]!r}")
    invalid = [int(x) for x in invalid_line[1:]]
    return n, edges, root, invalid


def part1(lines: list[str]) -> list[str]:
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
