"""od07 Throne Inheritance without an initial king -- reference solution.

Source (MED, fastprep "Snowflake Throne Inheritance without initial king", phone screen,
"Source Match: 86% (adapted from original problem)"): a paraphrase of LC 1600 "Throne
Inheritance" with one Snowflake-specific twist -- the family starts EMPTY (no king supplied at
construction); whoever is named as the *parent* in the very first birth() call becomes the
founder and never changes, even after their own death. Everything more specific than the API
shape and that one twist is reconstructed and stated in problem.md.

Part1: birth(parent, child) grows a tree rooted at the founder; death(name) is idempotent and
never removes anyone, it only hides them from get_inheritance_order(); get_inheritance_order()
is a pre-order DFS, children visited in birth order, dead names skipped from the OUTPUT (their
living descendants still appear -- dead branches stay structurally intact).
Part2: get_inheritance_order() must not use Python recursion -- a single-child chain of length
10**5 would blow the default recursion limit -- so the DFS uses an explicit stack, O(living +
dead) time and space, no recursion at all.
Part3: succession_after(name) walks the SAME full pre-order (dead names included, so you can
still ask "who succeeds a king right after he dies") and returns the first LIVING name strictly
after name's position, or "" if name was never born or nobody living follows.
"""

from __future__ import annotations

import sys


class ThroneInheritance:
    def __init__(self) -> None:
        self._founder: str | None = None
        self._children: dict[str, list[str]] = {}  # name -> children, birth order
        self._dead: set[str] = set()

    def birth(self, parent_name: str, child_name: str) -> None:
        if parent_name == child_name:
            raise ValueError(f"cannot be your own parent: {child_name!r}")
        if child_name in self._children:
            raise ValueError(f"duplicate child name: {child_name!r}")
        if self._founder is None:
            # first call ever: no king was supplied at construction, so the parent named here
            # becomes the founder and is planted as the tree's root.
            self._founder = parent_name
            self._children[parent_name] = []
        elif parent_name not in self._children:
            raise ValueError(f"unknown parent: {parent_name!r}")
        self._children[parent_name].append(child_name)
        self._children[child_name] = []

    def death(self, name: str) -> None:
        """Idempotent: safe to call on the living, the already-dead, or a name never born --
        never raises, never mutates the tree shape, only marks name as dead."""
        self._dead.add(name)

    def get_inheritance_order(self) -> list[str]:
        return [name for name in self._full_order() if name not in self._dead]

    def succession_after(self, name: str) -> str:
        order = self._full_order()
        try:
            i = order.index(name)
        except ValueError:
            return ""  # name was never born
        for nxt in order[i + 1 :]:
            if nxt not in self._dead:
                return nxt
        return ""  # no living heir follows

    # ------------------------------------------------------------------ internals
    def _full_order(self) -> list[str]:
        """Iterative pre-order DFS over every name ever born (dead included), founder first,
        each node's children visited in birth order. O(n) time/space, no recursion -- this is
        what makes Part2's 10**5-deep chain safe."""
        if self._founder is None:
            return []
        order: list[str] = []
        stack = [self._founder]
        while stack:
            node = stack.pop()
            order.append(node)
            for child in reversed(self._children.get(node, ())):
                stack.append(child)
        return order


# --------------------------------------------------------------------------- command stream
def run_commands(lines: list[str]) -> list[str]:
    """BIRTH <parent> <child> | DEATH <name> | ORDER | SUCCESSOR <name>.
    BIRTH: silent on success; 'ERROR' on self-parent / duplicate child / unknown parent.
    DEATH: always silent (idempotent, even for a name never born).
    ORDER: space-joined inheritance order, or '-' if empty.
    SUCCESSOR <name>: next living heir strictly after <name>, or '-' if none/unknown."""
    tree = ThroneInheritance()
    out: list[str] = []
    for line in lines:
        parts = line.split()
        cmd = parts[0]
        if cmd == "BIRTH":
            try:
                tree.birth(parts[1], parts[2])
            except ValueError:
                out.append("ERROR")
        elif cmd == "DEATH":
            tree.death(parts[1])
        elif cmd == "ORDER":
            order = tree.get_inheritance_order()
            out.append(" ".join(order) if order else "-")
        elif cmd == "SUCCESSOR":
            out.append(tree.succession_after(parts[1]) or "-")
        else:
            raise ValueError(f"unknown command {line!r}")
    return out


def part1(lines: list[str]) -> list[str]:
    """BIRTH / DEATH / ORDER."""
    return run_commands(lines)


def part2(lines: list[str]) -> list[str]:
    """Same commands as part1; this is the part exercised against a 10**5-deep chain."""
    return run_commands(lines)


def part3(lines: list[str]) -> list[str]:
    """Adds SUCCESSOR."""
    return run_commands(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
