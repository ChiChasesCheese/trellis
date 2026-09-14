"""q03 Tree Height Reduction -- reference solution.

Three parts drawn from three DIFFERENT sources with three DIFFERENT node-indexing / depth
conventions. Each part is kept faithful to its OWN source's convention -- they are not unified.
See problem.md for the full derivation of each part's algorithm.

Part 1 (FastPrep, "minimum n-ary tree deletions"): nodes 1..n, `parent` has length n-1 where
`parent[i]` (0-indexed i) is the parent of node i+2 (node 1 is the root, depth 1).
Part 2 (PracHub, "prune a multiway tree"): nodes 0-indexed, `parent[i]` is the parent index of
node i, `parent[root] == -1`, root depth 0.
Part 3 (FastPrep, "minimum height with re-root ops"): nodes 1-indexed, root = 1, height in
EDGES (root alone = height 0), tree given as explicit edge lists.
"""
from __future__ import annotations

import math
import sys
from collections import deque

sys.setrecursionlimit(20000)  # part3's fix() recurses one frame per tree level (chains up to ~2000)


# ---------------------------------------------------------------- Part 1
def part1(parent: list[int], k: int) -> list[int]:
    """parent[i] (0-indexed i) = parent of node i+2; node 1 is the root, root depth = 1.

    Derivation: depth is strictly increasing down any root-to-node path, so a node's depth > k
    if and only if it MUST be deleted -- no ancestor-only deletion can save it without also
    deleting valid shallower nodes, and it can always be deleted last (bottom-up, leaf order)
    once its own deeper descendants (which also all exceed k) are gone first. So the answer is
    exactly the sorted list of all node ids with depth > k. The root itself is never eligible
    (only non-root leaves may be deleted) -- excluded explicitly, though with the depth-1 root
    convention this only matters for the degenerate k == 0.
    """
    n = len(parent) + 1
    children: dict[int, list[int]] = {v: [] for v in range(1, n + 1)}
    for i, p in enumerate(parent):
        children[p].append(i + 2)

    depth = {1: 1}
    dq = deque([1])
    while dq:
        v = dq.popleft()
        for c in children[v]:
            depth[c] = depth[v] + 1
            dq.append(c)

    return sorted(v for v in range(1, n + 1) if v != 1 and depth[v] > k)


# ---------------------------------------------------------------- Part 2
def part2(parent: list[int], k: int) -> int:
    """parent[i] = parent index of node i (0-indexed), parent[root] == -1, root depth 0.

    Here each deletion removes a WHOLE subtree at once (cheaper than node-by-node), so the
    answer is the count of "topmost" violators: nodes with depth > k whose own parent has
    depth <= k. If the parent also violates, the parent's own subtree-deletion already covers
    this node, so it is not counted again.
    """
    n = len(parent)
    children: dict[int, list[int]] = {v: [] for v in range(n)}
    root = None
    for v, p in enumerate(parent):
        if p == -1:
            root = v
        else:
            children[p].append(v)
    assert root is not None, "parent array must contain exactly one root (parent[root] == -1)"

    depth = {root: 0}
    dq = deque([root])
    while dq:
        v = dq.popleft()
        for c in children[v]:
            depth[c] = depth[v] + 1
            dq.append(c)

    count = 0
    for v in range(n):
        if v == root:
            continue
        if depth[v] > k and depth[parent[v]] <= k:
            count += 1
    return count


# ---------------------------------------------------------------- Part 3
def _build_children(tree_nodes: int, tree_from: list[int], tree_to: list[int]) -> dict[int, list[int]]:
    children: dict[int, list[int]] = {v: [] for v in range(1, tree_nodes + 1)}
    for f, t in zip(tree_from, tree_to):
        children[f].append(t)
    return children


def _compute_height(children: dict[int, list[int]], root: int) -> dict[int, int]:
    """height[v] = max edges from v down to any leaf in v's ORIGINAL subtree. Iterative
    post-order (not recursive) so this doesn't hit Python's recursion limit on deep chains."""
    height: dict[int, int] = {}
    stack: list[tuple[int, bool]] = [(root, False)]
    while stack:
        v, processed = stack.pop()
        if processed:
            h = 0
            for c in children[v]:
                if height[c] + 1 > h:
                    h = height[c] + 1
            height[v] = h
        else:
            stack.append((v, True))
            for c in children[v]:
                stack.append((c, False))
    return height


def _total_ops(H: int, root: int, children: dict[int, list[int]], height: dict[int, int]) -> int:
    """Minimum re-root operations to make the whole tree fit within height H.

    fix(v, d): min ops for v's whole original subtree to respect H, given v currently sits at
    depth d (unless relocated, in which case v's new depth is 1).
      - if d + height(v) <= H: already fits, 0 ops.
      - if d > H: v itself already violates and MUST be relocated (its new depth is 1).
      - else: min(cut v now, or push the decision down to each child at depth d+1).
    Memoized per H call on (v, d) -- see REPORT.md for why this is still empirically
    super-linear on skewed (chain) trees despite each individual step being O(1) amortized.

    H == 0 special case (a bug in the naive pseudocode this is adapted from): relocating a node
    ALWAYS lands it at depth 1 (directly under the root), never at depth 0 -- only the root
    itself can ever be at depth 0. So if H == 0, relocating never actually fixes a violating
    node; every real (non-root) node is unconditionally infeasible, regardless of budget. The
    naive pseudocode's "if d > H: return 1 + fix_children_only(v, 1, H)" implicitly (and
    wrongly) assumes relocation always resolves v without checking 1 <= H. fix() is only ever
    called on non-root nodes (fix_children_only(root, 0, H) is the only entry point, and it
    calls fix on root's children), so when H == 0 every call to fix() must report "impossible".
    """
    if H == 0:
        # feasible only if the tree is just the root (no edges at all)
        return 0 if not children[root] else math.inf

    memo: dict[tuple[int, int], int] = {}

    def fix(v: int, d: int) -> int:
        key = (v, d)
        cached = memo.get(key)
        if cached is not None:
            return cached
        if d + height[v] <= H:
            memo[key] = 0
            return 0
        if d > H:
            res = 1 + _fix_children_only(v, 1)
            memo[key] = res
            return res
        cut_cost = 1 + _fix_children_only(v, 1)
        keep_cost = 0
        for c in children[v]:
            keep_cost += fix(c, d + 1)
        res = cut_cost if cut_cost < keep_cost else keep_cost
        memo[key] = res
        return res

    def _fix_children_only(v: int, newd: int) -> int:
        total = 0
        for c in children[v]:
            total += fix(c, newd + 1)
        return total

    return _fix_children_only(root, 0)


def part3(tree_nodes: int, tree_from: list[int], tree_to: list[int], max_operations: int) -> int:
    """Binary search the smallest height H in [0, original_height] with total_ops(H) <=
    max_operations. Root is always node 1 and can never be cut."""
    children = _build_children(tree_nodes, tree_from, tree_to)
    root = 1
    height = _compute_height(children, root)
    original_height = height[root]

    lo, hi = 0, original_height
    while lo < hi:
        mid = (lo + hi) // 2
        if _total_ops(mid, root, children, height) <= max_operations:
            hi = mid
        else:
            lo = mid + 1
    return lo


# ---------------------------------------------------------------- main / stdin-stdout
def _read_ints(line: str) -> list[int]:
    return [int(x) for x in line.split()] if line.strip() else []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    """stdin format (each part has ITS OWN layout, matching its own source convention):

    PART 1
    n
    parent[0] parent[1] ... parent[n-2]      (length n-1; blank/omitted line if n == 1)
    k

    PART 2
    n
    parent[0] parent[1] ... parent[n-1]      (length n; parent[root] == -1)
    k

    PART 3
    tree_nodes
    edge_count
    tree_from[0] ... tree_from[edge_count-1]  (blank/omitted line if edge_count == 0)
    tree_to[0] ... tree_to[edge_count-1]      (blank/omitted line if edge_count == 0)
    max_operations

    stdout:
    PART 1 -> one line, the deletion ids space-separated ascending (empty line if none)
    PART 2 -> one line, a single integer count
    PART 3 -> one line, a single integer height
    """
    lines = stdin.read().splitlines()
    idx = 0

    def next_scalar_line() -> str:
        """A line that must hold a single value (part/n/k/edge_count/...): skip past any
        purely-blank separator lines to find it."""
        nonlocal idx
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        line = lines[idx] if idx < len(lines) else ""
        idx += 1
        return line

    def next_array_line() -> str:
        """A line that holds a (possibly empty) space-separated array: consume exactly one
        line, which may legitimately be blank or missing."""
        nonlocal idx
        line = lines[idx] if idx < len(lines) else ""
        idx += 1
        return line

    part_line = next_scalar_line().strip()
    part_num = int(part_line.split()[1]) if len(part_line.split()) > 1 else 1

    if part_num == 1:
        n = int(next_scalar_line().strip())
        parent = _read_ints(next_array_line())
        k = int(next_scalar_line().strip())
        result = part1(parent, k)
        stdout.write(" ".join(map(str, result)) + "\n")
    elif part_num == 2:
        n = int(next_scalar_line().strip())
        parent = _read_ints(next_array_line())
        k = int(next_scalar_line().strip())
        stdout.write(f"{part2(parent, k)}\n")
    else:
        tree_nodes = int(next_scalar_line().strip())
        edge_count = int(next_scalar_line().strip())
        tree_from = _read_ints(next_array_line())
        tree_to = _read_ints(next_array_line())
        max_operations = int(next_scalar_line().strip())
        stdout.write(f"{part3(tree_nodes, tree_from, tree_to, max_operations)}\n")


if __name__ == "__main__":
    main()
