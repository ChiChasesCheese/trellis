"""pc10 Distributed Tree Count -- reference solution.

A rooted tree of nodes that only talk by messages. One global FIFO channel delivers messages
exactly once, in send order. Each delivery is logged as `from->to:MESSAGE`.

Protocol (Part1):
  * start: the root sends GET_COUNT to each child in increasing id order;
  * a node receiving GET_COUNT: if it is a leaf it sends `REPORT <1>` to its parent, otherwise it
    sends GET_COUNT to each child in increasing id order and waits;
  * a node receiving REPORT from a child adds the value; once every child has reported it sends
    `REPORT <1 + sum>` to its parent -- or, if it is the root, the run ends with `ROOT_COUNT:<n>`.
A single-node tree logs only `ROOT_COUNT:1`.

Part2 (reconstructed) adds unreliable links. Every send gets a global send id (0, 1, 2, ... in
send order, retries included). If a send id is in `drops`, that delivery is lost: it is logged as
`from->to:MESSAGE LOST` at its turn and the sender re-sends it once (a new send id, appended to the
channel). If the retry is lost too, the link is declared dead: logged `from->to:MESSAGE GIVEUP`,
and -- because link failure is detected at both ends -- the parent on that link treats the child's
whole subtree as missing (contributes 0) and counts it as reported. The run ends with
`ROOT_COUNT:<n>` or `ROOT_COUNT:<n> PARTIAL` if any subtree went missing.
"""

from __future__ import annotations

import sys
from collections import deque


def _children(parent: list[int]) -> tuple[int, list[list[int]]]:
    n = len(parent)
    if n == 0:
        raise ValueError("empty tree")
    roots = [i for i, p in enumerate(parent) if p == -1]
    if len(roots) != 1:
        raise ValueError(f"need exactly one root (-1), found {len(roots)}")
    kids: list[list[int]] = [[] for _ in range(n)]
    for i, p in enumerate(parent):
        if p == -1:
            continue
        if not 0 <= p < n or p == i:
            raise ValueError(f"bad parent {p} for node {i}")
        kids[p].append(i)
    root = roots[0]
    seen, stack = 0, [root]
    while stack:  # every node must hang off the root (no cycles, no forest)
        node = stack.pop()
        seen += 1
        stack.extend(kids[node])
    if seen != n:
        raise ValueError("parent array contains a cycle")
    return root, kids  # kids are already in increasing id order


def simulate_tree_count(parent: list[int], drops: set[int] | None = None) -> list[str]:
    """Part1 when drops is None/empty; Part2 otherwise."""
    drops = drops or set()
    root, kids = _children(parent)
    log: list[str] = []
    if not kids[root]:
        return ["ROOT_COUNT:1"]

    channel: deque[tuple[int, int, str, int, bool]] = deque()  # (frm, to, msg, send_id, is_retry)
    next_id = 0
    pending = [len(k) for k in kids]
    total = [1] * len(parent)
    partial = False

    def send(frm: int, to: int, msg: str, is_retry: bool = False) -> None:
        nonlocal next_id
        channel.append((frm, to, msg, next_id, is_retry))
        next_id += 1

    def child_done(node: int, value: int) -> str | None:
        """Account one finished child of `node`; returns the final line if the root finished."""
        total[node] += value
        pending[node] -= 1
        if pending[node] == 0:
            if node == root:
                return f"ROOT_COUNT:{total[node]}" + (" PARTIAL" if partial else "")
            send(node, parent[node], f"REPORT {total[node]}")
        return None

    for c in kids[root]:
        send(root, c, "GET_COUNT")

    while channel:
        frm, to, msg, send_id, is_retry = channel.popleft()
        if send_id in drops:
            if not is_retry:
                log.append(f"{frm}->{to}:{msg} LOST")
                send(frm, to, msg, is_retry=True)
                continue
            log.append(f"{frm}->{to}:{msg} GIVEUP")
            partial = True
            upper = frm if msg == "GET_COUNT" else to  # the parent on this link
            end = child_done(upper, 0)
            if end:
                log.append(end)
                return log
            continue

        log.append(f"{frm}->{to}:{msg}")
        if msg == "GET_COUNT":
            if not kids[to]:
                send(to, frm, "REPORT 1")
            else:
                for c in kids[to]:
                    send(to, c, "GET_COUNT")
        else:  # REPORT <v>
            end = child_done(to, int(msg.split()[1]))
            if end:
                log.append(end)
                return log
    raise AssertionError("channel drained without the root finishing")  # pragma: no cover


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """one line: space-separated parent array (root is -1)."""
    return simulate_tree_count([int(x) for x in lines[0].split()])


def part2(lines: list[str]) -> list[str]:
    """line 1: parent array; line 2: 'DROPS' followed by space-separated send ids (may be empty)."""
    parent = [int(x) for x in lines[0].split()]
    tokens = lines[1].split() if len(lines) > 1 else ["DROPS"]
    if tokens[0] != "DROPS":
        raise ValueError(f"expected 'DROPS ...', got {lines[1]!r}")
    return simulate_tree_count(parent, {int(x) for x in tokens[1:]})


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
