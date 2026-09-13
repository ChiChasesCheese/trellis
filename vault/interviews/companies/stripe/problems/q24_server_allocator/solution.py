"""q24 Server Allocator — reference solution.

Part 1: set membership walk from 1 (O(n)).  Parts 2-4: Tracker with, per host type, a
high-water counter and a min-heap of freed numbers, plus a set of live hostnames so a double
deallocate cannot push the same number twice.  Every operation is O(log n).
"""
from __future__ import annotations

import heapq
import sys


def next_server_number(allocated) -> int:
    """Smallest positive integer absent from `allocated`; 1.5-style floats never equal an int
    and are simply ignored by the `in` check (2 == 2.0 would count, as it should)."""
    taken = set(allocated)
    n = 1
    while n in taken:
        n += 1
    return n


def split_hostname(hostname: str) -> tuple[str, int] | None:
    """Split at the trailing digit run: 'apibox12' -> ('apibox', 12).
    None for no digits, empty type, number 0, or leading zeros ('apibox01' is not a name we issue)."""
    i = len(hostname)
    while i > 0 and hostname[i - 1].isdigit():
        i -= 1
    host_type, digits = hostname[:i], hostname[i:]
    if not host_type or not digits or digits[0] == "0":
        return None
    return host_type, int(digits)


class Tracker:
    def __init__(self, strict: bool = False) -> None:
        self.strict = strict
        self.next: dict[str, int] = {}          # type -> next never-issued number (high-water mark)
        self.free: dict[str, list[int]] = {}    # type -> min-heap of freed numbers
        self.live: set[str] = set()             # currently allocated hostnames

    def allocate(self, host_type: str) -> str:
        if not host_type or host_type[-1].isdigit():
            raise ValueError(f"invalid host type '{host_type}'")  # would make names ambiguous
        heap = self.free.get(host_type)
        if heap:
            n = heapq.heappop(heap)             # smallest freed number is reused first
        else:
            n = self.next.get(host_type, 1)
            self.next[host_type] = n + 1
        name = f"{host_type}{n}"
        self.live.add(name)
        return name

    def deallocate(self, hostname: str) -> bool:
        parts = split_hostname(hostname)
        if parts is None or hostname not in self.live:  # unknown / already freed / malformed
            if self.strict:
                raise KeyError(hostname)
            return False
        self.live.remove(hostname)
        host_type, n = parts
        heapq.heappush(self.free.setdefault(host_type, []), n)
        return True


def run_commands(lines) -> list[str]:
    """`lines` may be any iterable of raw lines (main streams stdin to keep 10^6 lines cheap)."""
    tracker = Tracker()
    out = []
    for ln in lines:
        f = ln.split()
        if not f:
            continue
        if f[0] == "ALLOCATE":
            out.append(tracker.allocate(f[1]))
        elif f[0] == "DEALLOCATE":
            tracker.deallocate(f[1])
        else:
            raise ValueError(f"unknown command: {ln}")
    return out


def _parse_numbers(line: str):
    line = line.strip().strip("[]")
    return [float(t) if "." in t else int(t) for t in line.replace(",", " ").split()]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    header = stdin.readline().strip()
    if not header:
        return
    part = int(header.split()[1])
    if part == 1:
        out = [str(next_server_number(_parse_numbers(ln))) for ln in stdin.read().splitlines()]
    else:
        out = run_commands(stdin)  # streamed: one line at a time
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
