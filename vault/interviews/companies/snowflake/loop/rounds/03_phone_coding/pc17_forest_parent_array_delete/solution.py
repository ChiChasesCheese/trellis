"""pc17 Forest Parent Array Delete Node -- reference solution.

A forest of n nodes is encoded as `parent: list[int]` of length n where `parent[i] == i` marks a
root. Deleting a node must (a) decide what happens to its children and (b) return a *valid*
parent array again, which for this representation means indices 0..n-2 with no gaps -- so every
remaining node needs to be renumbered (indices above the deleted one shift down by one) and every
surviving parent pointer needs to be rewritten in terms of the new numbering.

Part1's semantics ("what happens to the deleted node's children") is a reconstructed choice,
stated in problem.md: the direct children of the deleted node become roots themselves; deeper
descendants are untouched (their parent is still their real parent, just renumbered).
Part2 (reconstructed) deletes the whole subtree instead of just one node.
Part3 (reconstructed) is a *simultaneous* batch: each survivor's new parent is its nearest
still-alive ancestor in the ORIGINAL tree, skipping over every deleted ancestor -- not the result
of replaying Part1 one deletion at a time (those two give different answers whenever a deleted
node has an ancestor that is also deleted; see problem.md's worked example).
"""

from __future__ import annotations

import sys


def _check_index(parent: list[int], index: int) -> None:
    if not (0 <= index < len(parent)):
        raise ValueError(f"index {index} out of range for forest of size {len(parent)}")


def _renumber(remaining: list[int]) -> dict[int, int]:
    return {old: new for new, old in enumerate(remaining)}


# --------------------------------------------------------------------------- Part 1
def delete_node_children_become_roots(parent: list[int], delete_index: int) -> list[int]:
    """Remove `delete_index`; its direct children become roots. Returns a compacted parent
    array of length len(parent) - 1."""
    _check_index(parent, delete_index)
    n = len(parent)
    remaining = [i for i in range(n) if i != delete_index]
    old_to_new = _renumber(remaining)
    result = [0] * len(remaining)
    for old in remaining:
        new = old_to_new[old]
        p = parent[old]
        result[new] = new if p == delete_index else old_to_new[p]
    return result


# --------------------------------------------------------------------------- Part 2
def delete_subtree(parent: list[int], delete_index: int) -> list[int]:
    """Remove `delete_index` AND every descendant of it. Returns a compacted parent array."""
    _check_index(parent, delete_index)
    n = len(parent)
    children: dict[int, list[int]] = {}
    for i, p in enumerate(parent):
        if i != p:
            children.setdefault(p, []).append(i)

    to_remove = set()
    stack = [delete_index]
    while stack:
        node = stack.pop()
        if node in to_remove:
            continue
        to_remove.add(node)
        stack.extend(children.get(node, ()))

    remaining = [i for i in range(n) if i not in to_remove]
    old_to_new = _renumber(remaining)
    result = [0] * len(remaining)
    for old in remaining:
        new = old_to_new[old]
        p = parent[old]
        result[new] = new if (p == old or p in to_remove) else old_to_new[p]
    return result


# --------------------------------------------------------------------------- Part 3
def delete_nodes_batch(parent: list[int], delete_indices: list[int]) -> list[int]:
    """Delete every index in `delete_indices` simultaneously. Each surviving node's new parent
    is its nearest still-alive ancestor in the ORIGINAL tree (climbing past any number of
    deleted ancestors); if every ancestor up to and including the original root was deleted, the
    survivor becomes a root itself. Raises ValueError on an out-of-range or duplicated index."""
    n = len(parent)
    seen = set()
    for idx in delete_indices:
        _check_index(parent, idx)
        if idx in seen:
            raise ValueError(f"duplicate delete index {idx}")
        seen.add(idx)

    def nearest_live_ancestor(node: int):
        prev, cur = node, parent[node]
        while cur in seen and cur != prev:
            prev, cur = cur, parent[cur]
        if cur == prev:
            return None  # climbed to the (deleted-or-not) original root with nothing live above
        return cur

    remaining = [i for i in range(n) if i not in seen]
    old_to_new = _renumber(remaining)
    result = [0] * len(remaining)
    for old in remaining:
        new = old_to_new[old]
        anc = nearest_live_ancestor(old)
        result[new] = new if anc is None else old_to_new[anc]
    return result


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """each line: 'p0 p1 ... p(n-1) | delete_index' -> one line of the resulting parent array
    (space-separated, empty line for an empty forest)."""
    out = []
    for line in lines:
        left, right = line.split("|")
        parent = [int(x) for x in left.split()]
        delete_index = int(right.strip())
        out.append(" ".join(map(str, delete_node_children_become_roots(parent, delete_index))))
    return out


def part2(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        left, right = line.split("|")
        parent = [int(x) for x in left.split()]
        delete_index = int(right.strip())
        out.append(" ".join(map(str, delete_subtree(parent, delete_index))))
    return out


def part3(lines: list[str]) -> list[str]:
    """each line: 'p0 p1 ... p(n-1) | d0 d1 ...' (delete_indices space-separated, may be empty
    after the '|')."""
    out = []
    for line in lines:
        left, right = line.split("|")
        parent = [int(x) for x in left.split()]
        delete_indices = [int(x) for x in right.split()]
        out.append(" ".join(map(str, delete_nodes_batch(parent, delete_indices))))
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
