"""pc13 Service Startup / Dependency Ordering -- reference solution.

`deps` is a list of `(service, dependency)` pairs: `service` requires `dependency` to already be
up before `service` can start. Kahn's algorithm processes services whose every dependency has
already started; Part1's tie-break when several services are simultaneously ready is the smallest
service name (lexicographic), which makes the returned order fully deterministic.

A cycle means some services can never start. Rather than a generic "there is a cycle somewhere"
error, `CycleError.cycle` names one actual cycle (a minimal loop of mutually-dependent services),
found by an iterative (stack-based, no Python recursion) DFS with 3-colour marking restricted to
the services Kahn could not resolve -- some of those services are merely stuck WAITING on a cycle
without being part of it themselves, so a plain "everything left over" report would be misleading.

Part2 (reconstructed) groups services into startup WAVES: wave i is exactly the services that
become ready once every wave < i has fully started -- the standard level-order/BFS view of Kahn's
algorithm. Each wave is sorted ascending for a deterministic report (services in the same wave
start in parallel, so their relative order carries no meaning, but the printed order must still be
reproducible).

Part3 (reconstructed) adds a per-service duration and asks for each service's earliest possible
start time plus the time at which every service is up: `start[s] = max(finish[dependency] for
dependency in deps(s), default 0)`, `finish[s] = start[s] + duration[s]`. This is exactly the
"parallel courses" critical-path recurrence (pc09) applied to a dependency graph instead of a
course graph.
"""

from __future__ import annotations

import heapq
import sys


class CycleError(ValueError):
    """Raised when `deps` contains a cycle. `.cycle` lists the services around one such cycle,
    in dependency order (cycle[i] requires cycle[i + 1], and cycle[-1] requires cycle[0])."""

    def __init__(self, cycle: list[str]) -> None:
        self.cycle = cycle
        super().__init__(f"dependency cycle detected: {' -> '.join(cycle)} -> {cycle[0]}")


def _validate(services: list[str], deps: list[tuple[str, str]]) -> None:
    if len(set(services)) != len(services):
        raise ValueError("services must not contain duplicates")
    known = set(services)
    for s, d in deps:
        if s not in known or d not in known:
            raise ValueError(f"dependency {(s, d)!r} references an unknown service")
        if s == d:
            raise ValueError(f"a service cannot depend on itself: {s!r}")


def _build(services: list[str], deps: list[tuple[str, str]]):
    """requires[s] = set of services s directly depends on; enables[d] = services unlocked once d is up."""
    requires: dict[str, set[str]] = {s: set() for s in services}
    enables: dict[str, list[str]] = {s: [] for s in services}
    for s, d in deps:
        requires[s].add(d)
        enables[d].append(s)
    return requires, enables


def _find_one_cycle(services: list[str], requires: dict[str, set[str]], stuck: set[str]) -> list[str]:
    """Iterative DFS (explicit stack, 3-colour marking) restricted to `stuck` services, returning
    one real cycle -- not just the whole stuck set, some of which may only be waiting on a cycle."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {s: WHITE for s in stuck}
    for start in sorted(stuck):
        if color[start] != WHITE:
            continue
        path: list[str] = []
        frame_stack = [(start, iter(sorted(requires[start] & stuck)))]
        color[start] = GRAY
        path.append(start)
        while frame_stack:
            node, it = frame_stack[-1]
            advanced = False
            for nxt in it:
                if color[nxt] == GRAY:
                    idx = path.index(nxt)
                    return path[idx:]
                if color[nxt] == WHITE:
                    color[nxt] = GRAY
                    path.append(nxt)
                    frame_stack.append((nxt, iter(sorted(requires[nxt] & stuck))))
                    advanced = True
                    break
            if not advanced:
                color[node] = BLACK
                path.pop()
                frame_stack.pop()
    raise AssertionError("stuck services must contain a cycle")  # pragma: no cover -- defensive


# --------------------------------------------------------------------------- Part 1
def startup_order(services: list[str], deps: list[tuple[str, str]]) -> list[str]:
    _validate(services, deps)
    requires, enables = _build(services, deps)
    indeg = {s: len(requires[s]) for s in services}
    heap = sorted(s for s in services if indeg[s] == 0)
    heapq.heapify(heap)
    order: list[str] = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in enables[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(order) != len(services):
        stuck = set(services) - set(order)
        raise CycleError(_find_one_cycle(services, requires, stuck))
    return order


# --------------------------------------------------------------------------- Part 2
def startup_waves(services: list[str], deps: list[tuple[str, str]]) -> list[list[str]]:
    _validate(services, deps)
    requires, enables = _build(services, deps)
    indeg = {s: len(requires[s]) for s in services}
    remaining = set(services)
    waves: list[list[str]] = []
    frontier = sorted(s for s in services if indeg[s] == 0)
    while frontier:
        waves.append(frontier)
        remaining -= set(frontier)
        nxt_frontier: set[str] = set()
        for node in frontier:
            for succ in enables[node]:
                indeg[succ] -= 1
                if indeg[succ] == 0:
                    nxt_frontier.add(succ)
        frontier = sorted(nxt_frontier)
    if remaining:
        raise CycleError(_find_one_cycle(services, requires, remaining))
    return waves


# --------------------------------------------------------------------------- Part 3
def startup_times(
    services: list[str], deps: list[tuple[str, str]], duration: dict[str, int]
) -> tuple[dict[str, int], int]:
    _validate(services, deps)
    if set(duration) != set(services):
        raise ValueError("duration must have exactly one entry per service")
    if any(d < 0 for d in duration.values()):
        raise ValueError("duration must be >= 0")
    requires, enables = _build(services, deps)
    indeg = {s: len(requires[s]) for s in services}
    start: dict[str, int] = {}
    finish: dict[str, int] = {}
    heap = sorted(s for s in services if indeg[s] == 0)
    heapq.heapify(heap)
    processed = 0
    while heap:
        node = heapq.heappop(heap)
        processed += 1
        start[node] = max((finish[d] for d in requires[node]), default=0)
        finish[node] = start[node] + duration[node]
        for nxt in enables[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if processed != len(services):
        stuck = set(services) - set(start)
        raise CycleError(_find_one_cycle(services, requires, stuck))
    overall = max(finish.values(), default=0)
    return start, overall


# --------------------------------------------------------------------------- line-driven wrappers
def _read(lines: list[str], idx: int) -> tuple[list[str], list[tuple[str, str]], int]:
    tag, n = lines[idx].split()
    if tag != "S":
        raise ValueError(f"expected 'S <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    services = lines[idx : idx + n]
    idx += n
    tag, m = lines[idx].split()
    if tag != "D":
        raise ValueError(f"expected 'D <m>', got {lines[idx]!r}")
    idx += 1
    m = int(m)
    deps = [tuple(lines[idx + t].split()) for t in range(m)]
    idx += m
    return services, deps, idx


def part1(lines: list[str]) -> list[str]:
    """'S n' / n service names / 'D m' / m 'service dependency' lines -> the startup order, or
    'CYCLE <c1> <c2> ...' if `deps` contains a cycle."""
    services, deps, _ = _read(lines, 0)
    try:
        order = startup_order(services, deps)
    except CycleError as e:
        return ["CYCLE " + " ".join(e.cycle)]
    return order


def part2(lines: list[str]) -> list[str]:
    """Same input -> one line per wave: space-separated service names (ascending); or CYCLE line."""
    services, deps, _ = _read(lines, 0)
    try:
        waves = startup_waves(services, deps)
    except CycleError as e:
        return ["CYCLE " + " ".join(e.cycle)]
    return [" ".join(wave) for wave in waves]


def part3(lines: list[str]) -> list[str]:
    """Same input plus 'T n' / n 'service duration' lines -> 'earliest_all_up' then one 'service
    start' line per service (ascending by name); or CYCLE line."""
    services, deps, idx = _read(lines, 0)
    tag, n = lines[idx].split()
    if tag != "T":
        raise ValueError(f"expected 'T <n>', got {lines[idx]!r}")
    idx += 1
    n = int(n)
    duration: dict[str, int] = {}
    for t in range(n):
        name, d = lines[idx + t].split()
        duration[name] = int(d)
    try:
        start, overall = startup_times(services, deps, duration)
    except CycleError as e:
        return ["CYCLE " + " ".join(e.cycle)]
    out = [str(overall)]
    out.extend(f"{s} {start[s]}" for s in sorted(services))
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
