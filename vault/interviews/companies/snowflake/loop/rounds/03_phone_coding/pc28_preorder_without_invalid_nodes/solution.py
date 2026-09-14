"""pc28 Preorder Traversal Without Invalid Nodes -- reference solution.

n nodes numbered 0..n-1, edges = [parent, child] given in the order children should be visited,
a root, and a list of invalid nodes. Preorder-traverse the tree skipping invalid nodes.

The source preview names the shape (nodes/edges/root/invalid, preorder skipping invalid nodes)
but not what happens to an invalid node's SUBTREE -- that ambiguity is called out and both
readings are implemented and tested (reconstructed):

Part1: an invalid node is itself omitted from the output, but its children are still visited
       (skip-and-splice: the invalid node's children take its place in the preorder).
Part2: an invalid node prunes its entire subtree (skip-and-cut: nothing under an invalid node is
       ever visited, valid or not).

Both must be ITERATIVE (explicit stack), since depth can reach 1e5 and Python's recursion limit
(and C stack) would blow up on a recursive preorder over a path-shaped tree of that depth.
"""

from __future__ import annotations

import sys

# --------------------------------------------------------------------------- shared
def _build_children(edges: list[tuple[int, int]], n: int) -> list[list[int]]:
    """children[p] lists p's children IN THE ORDER edges gave them (preorder must respect this,
    not renumber/sort children)."""
    children: list[list[int]] = [[] for _ in range(n)]
    for parent, child in edges:
        children[parent].append(child)
    return children


# --------------------------------------------------------------------------- Part 1
def preorder_skip_invalid_splice(
    n: int, edges: list[tuple[int, int]], root: int, invalid: list[int]
) -> list[int]:
    """Part1 (reconstructed reading #1): an invalid node is omitted from the output, but its
    children are still traversed (as if the invalid node were transparent). Iterative, explicit
    stack -- safe for depth up to 1e5."""
    children = _build_children(edges, n)
    bad = set(invalid)
    out: list[int] = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node not in bad:
            out.append(node)
        # push children in reverse so they pop in original left-to-right order
        stack.extend(reversed(children[node]))
    return out


# --------------------------------------------------------------------------- Part 2
def preorder_skip_invalid_prune(
    n: int, edges: list[tuple[int, int]], root: int, invalid: list[int]
) -> list[int]:
    """Part2 (reconstructed reading #2): an invalid node prunes its WHOLE subtree -- nothing
    under an invalid node is ever visited. Iterative, explicit stack."""
    children = _build_children(edges, n)
    bad = set(invalid)
    out: list[int] = []
    if root in bad:
        return out
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node)
        stack.extend(c for c in reversed(children[node]) if c not in bad)
    return out


# --------------------------------------------------------------------------- line-driven wrappers
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
    n, edges, root, invalid = _parse_common(lines)
    order = preorder_skip_invalid_splice(n, edges, root, invalid)
    return [" ".join(map(str, order))] if order else ["-"]


def part2(lines: list[str]) -> list[str]:
    n, edges, root, invalid = _parse_common(lines)
    order = preorder_skip_invalid_prune(n, edges, root, invalid)
    return [" ".join(map(str, order))] if order else ["-"]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
