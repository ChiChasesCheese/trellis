"""od03 Transactional In-Memory KV Store -- YOUR implementation. Run pytest against this file
with IMPL=starter.

See problem.md for the full contract: nested begin/commit/rollback merge semantics, and the
per-thread transaction stack / linearizable-read requirement for Part3.
"""

from __future__ import annotations

import sys


class TransactionalKVStore:
    def __init__(self) -> None:
        pass  # TODO: a shared global dict + a per-thread stack of transaction overlays

    def get(self, key: str) -> int | None:
        """Read from the calling thread's own transaction stack (innermost frame that has
        touched `key` wins), falling back to global state. None if never set / deleted."""
        raise NotImplementedError  # TODO

    def put(self, key: str, value: int) -> None:
        """Write to the innermost active transaction of the calling thread, or straight to
        global state if no transaction is active."""
        raise NotImplementedError  # TODO

    def delete(self, key: str) -> None:
        """Same scoping as put(), but records 'this key is deleted here' rather than a value."""
        raise NotImplementedError  # TODO

    def begin(self) -> None:
        """Push a new (possibly nested) transaction frame onto the calling thread's stack."""
        raise NotImplementedError  # TODO

    def commit(self) -> bool:
        """Merge the innermost frame into its parent (or into global state if it was the
        outermost frame). False if no active transaction."""
        raise NotImplementedError  # TODO

    def rollback(self) -> bool:
        """Discard the innermost frame's writes entirely. False if no active transaction."""
        raise NotImplementedError  # TODO


def _process(store: "TransactionalKVStore", line: str) -> str | None:
    fields = line.split()
    verb = fields[0]
    if verb == "GET":
        return str(store.get(fields[1]))
    if verb == "PUT":
        store.put(fields[1], int(fields[2]))
        return None
    if verb == "DELETE":
        store.delete(fields[1])
        return None
    if verb == "BEGIN":
        store.begin()
        return None
    if verb == "COMMIT":
        return str(store.commit())
    if verb == "ROLLBACK":
        return str(store.rollback())
    raise ValueError(f"bad line: {line!r}")


def part1(lines: list[str]) -> list[str]:
    """Drive a fresh TransactionalKVStore from GET/PUT/DELETE/BEGIN/COMMIT/ROLLBACK lines."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Same driver as part1 -- nesting is a property of the class, exercised here with multiple
    BEGIN calls before a matching COMMIT/ROLLBACK."""
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
    """Same driver as part1, single-threaded (the linearizable-reads guarantee is exercised
    directly against TransactionalKVStore with real threads in test_od03.py)."""
    return part1(lines)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    body = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[n](body)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
