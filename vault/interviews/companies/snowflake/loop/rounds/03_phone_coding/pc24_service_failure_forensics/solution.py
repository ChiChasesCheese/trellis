"""pc24 Service Failure Forensics -- reference solution.

Three stages, glued around one incident:
Part1: binary search a sorted log for the first ERROR at/after a given timestamp.
Part2: given "A depends on B" edges (B fails -> A fails), BFS/DFS every service that will
       eventually fail starting from one initially-failed service.
Part3: the longest failure-propagation chain in that failure DAG (longest path), with an
       explicit, defined behaviour for cycles (a genuine dependency cycle is itself reported as
       an error condition: services rarely have circular hard dependencies, and "longest path"
       is undefined -- infinite -- on a cycle).

Log line format (defined here, not given verbatim in the source preview):
    "<ts> <service> <LEVEL> <message>"
where <ts> is a zero-padded, lexicographically-sortable ISO-ish string (e.g.
"2026-09-01T00:03:12"), <service> has no spaces, LEVEL in {INFO, WARN, ERROR}, and <message> is
the rest of the line (may itself contain spaces). Logs are given already sorted by <ts> ascending
(stable: a tie in <ts> keeps input order), which is what makes Part 1 a binary search rather than
a linear scan.
"""

from __future__ import annotations

import bisect
import heapq
import sys

# --------------------------------------------------------------------------- Part 1
def _parse_line(line: str) -> tuple[str, str, str, str]:
    parts = line.split(" ", 3)
    if len(parts) < 3:
        raise ValueError(f"log line must be '<ts> <service> <LEVEL> [msg]', got {line!r}")
    ts, service, level = parts[0], parts[1], parts[2]
    msg = parts[3] if len(parts) == 4 else ""
    if level not in ("INFO", "WARN", "ERROR"):
        raise ValueError(f"unknown level {level!r} in line {line!r}")
    return ts, service, level, msg


def first_error_at_or_after(logs: list[str], ts: str) -> int:
    """Index of the first ERROR-level line with timestamp >= ts, or -1 if none. `logs` is sorted
    by timestamp ascending. Binary search (`bisect_left`) finds the first line at/after `ts` in
    O(log n) comparisons, then a forward scan finds the first ERROR from there -- see problem.md
    for why the scan's amortised cost stays small even though it isn't itself a binary search."""
    timestamps = [_parse_line(line)[0] for line in logs]
    start = bisect.bisect_left(timestamps, ts)
    for i in range(start, len(logs)):
        if _parse_line(logs[i])[2] == "ERROR":
            return i
    return -1


# --------------------------------------------------------------------------- Part 2
def _parse_edges(edges: list[str]) -> dict[str, list[str]]:
    """edges: 'A B' meaning A depends on B (B fails -> A fails). Returns adjacency B -> [A, ...]
    (the failure-propagation direction), preserving input order for determinism."""
    graph: dict[str, list[str]] = {}
    for e in edges:
        parts = e.split()
        if len(parts) != 2:
            raise ValueError(f"edge must be 'A B' (A depends on B), got {e!r}")
        a, b = parts
        graph.setdefault(b, [])
        if a not in graph[b]:
            graph[b].append(a)
        graph.setdefault(a, [])
    return graph


def services_that_will_fail(edges: list[str], initial_failure: str) -> list[str]:
    """BFS/DFS forward through the failure graph (B fails -> everything depending on B fails).
    Returns every service that fails, INCLUDING `initial_failure` itself, in the order first
    discovered by a BFS from `initial_failure` (breadth-first, edges visited in the order given).
    Unknown `initial_failure` (never appears in any edge) -> ValueError."""
    graph = _parse_edges(edges)
    if initial_failure not in graph:
        raise ValueError(f"unknown service {initial_failure!r}")
    seen = [initial_failure]
    seen_set = {initial_failure}
    i = 0
    while i < len(seen):
        cur = seen[i]
        i += 1
        for nxt in graph.get(cur, []):
            if nxt not in seen_set:
                seen_set.add(nxt)
                seen.append(nxt)
    return seen


# --------------------------------------------------------------------------- Part 3
def longest_failure_chain(edges: list[str]) -> list[str]:
    """Longest path in the failure DAG (B -> A meaning "B failing causes A to fail"), i.e. the
    longest sequence of services s0, s1, ..., sk where each s_{i+1} depends on s_i. Ties broken by
    lexicographically-smallest sequence of service names. A genuine cycle (a service transitively
    depending on itself) makes "longest path" undefined (infinite) -- we detect it and raise
    ValueError naming one service on the cycle, rather than silently looping forever or picking an
    arbitrary cutoff."""
    graph = _parse_edges(edges)
    nodes = sorted(graph)
    if not nodes:
        raise ValueError("no services (empty edge list)")

    # Kahn's algorithm to both detect a cycle and get a topological order in one pass.
    indeg = {n: 0 for n in nodes}
    for b in nodes:
        for a in graph[b]:
            indeg[a] += 1
    order: list[str] = []
    heap = sorted(n for n in nodes if indeg[n] == 0)
    heapq.heapify(heap)
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for nxt in graph[n]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(order) != len(nodes):
        remaining = sorted(n for n in nodes if n not in order)
        raise ValueError(f"failure graph has a cycle involving {remaining[0]!r} (not a DAG)")

    # longest path ending at each node, processed in topological order so predecessors are
    # already finalised. We keep the full chain (not just a back-pointer) because the tie-break
    # is lexicographic over the whole sequence, not just the last step.
    best_len = {n: 1 for n in nodes}
    best_chain: dict[str, list[str]] = {n: [n] for n in nodes}
    for b in order:
        for a in graph[b]:
            cand_len = best_len[b] + 1
            cand_chain = best_chain[b] + [a]
            if cand_len > best_len[a] or (cand_len == best_len[a] and cand_chain < best_chain[a]):
                best_len[a] = cand_len
                best_chain[a] = cand_chain

    winner = min(nodes, key=lambda n: (-best_len[n], best_chain[n]))
    return best_chain[winner]


# --------------------------------------------------------------------------- line-driven wrappers
def _read_n_lines(lines: list[str], idx: int) -> tuple[list[str], int]:
    tag, n = lines[idx].split()
    if tag != "N":
        raise ValueError(f"expected 'N <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    return lines[idx : idx + n], idx + n


def part1(lines: list[str]) -> list[str]:
    """'N n' / n log lines / 'Q ts' -> one line: the 0-based index, or -1."""
    logs, idx = _read_n_lines(lines, 0)
    tag, ts = lines[idx].split(maxsplit=1)
    if tag != "Q":
        raise ValueError(f"expected 'Q <ts>', got {lines[idx]!r}")
    return [str(first_error_at_or_after(logs, ts))]


def part2(lines: list[str]) -> list[str]:
    """'N n' / n edge lines / 'S service' -> one line: space-joined failed services in BFS order."""
    edges, idx = _read_n_lines(lines, 0)
    tag, service = lines[idx].split()
    if tag != "S":
        raise ValueError(f"expected 'S <service>', got {lines[idx]!r}")
    return [" ".join(services_that_will_fail(edges, service))]


def part3(lines: list[str]) -> list[str]:
    """'N n' / n edge lines -> one line: space-joined services on the longest failure chain, or
    'CYCLE <service>' if the graph isn't a DAG."""
    edges, _ = _read_n_lines(lines, 0)
    try:
        chain = longest_failure_chain(edges)
    except ValueError as exc:
        # extract the service name the exception names, for a stable one-line report
        msg = str(exc)
        service = msg.split("involving ")[1].split(" (")[0].strip("'")
        return [f"CYCLE {service}"]
    return [" ".join(chain)]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
