"""od03 Transactional In-Memory KV Store -- reference solution.

A shared global dict plus a per-thread stack of overlay frames (via threading.local(), so each
thread only ever touches its own stack -- no locking needed there). Each frame maps key ->
either its new value or the _DELETED sentinel, recording only *this* transaction's own writes.
Reads walk the calling thread's stack innermost-first, falling back to global state under a lock.
commit() merges the innermost frame into its parent (dict.update -- last write wins, which is
correct because the frame already holds the most recent value for each key it touched) or, if it
was the outermost frame, applies it to global state atomically under the same lock reads use.
rollback() simply discards the innermost frame -- no separate undo log is needed because the
frame itself only ever holds this transaction's own writes, which is exactly what first-touch
snapshotting protects against re-recording.
"""

from __future__ import annotations

import sys
import threading

_DELETED = object()


class TransactionalKVStore:
    def __init__(self) -> None:
        self._global: dict[str, int] = {}
        self._global_lock = threading.Lock()
        self._local = threading.local()

    def _stack(self) -> list[dict]:
        stack = getattr(self._local, "stack", None)
        if stack is None:
            stack = []
            self._local.stack = stack
        return stack

    def get(self, key: str) -> int | None:
        for frame in reversed(self._stack()):
            if key in frame:
                value = frame[key]
                return None if value is _DELETED else value
        with self._global_lock:
            return self._global.get(key)

    def put(self, key: str, value: int) -> None:
        stack = self._stack()
        if stack:
            stack[-1][key] = value
        else:
            with self._global_lock:
                self._global[key] = value

    def delete(self, key: str) -> None:
        stack = self._stack()
        if stack:
            stack[-1][key] = _DELETED
        else:
            with self._global_lock:
                self._global.pop(key, None)

    def begin(self) -> None:
        self._stack().append({})

    def commit(self) -> bool:
        stack = self._stack()
        if not stack:
            return False
        frame = stack.pop()
        if stack:
            stack[-1].update(frame)
        else:
            with self._global_lock:
                for key, value in frame.items():
                    if value is _DELETED:
                        self._global.pop(key, None)
                    else:
                        self._global[key] = value
        return True

    def rollback(self) -> bool:
        stack = self._stack()
        if not stack:
            return False
        stack.pop()
        return True


# ---------------------------------------------------------------------- line-driven wrappers
def _process(store: TransactionalKVStore, line: str) -> str | None:
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
    store = TransactionalKVStore()
    out: list[str] = []
    for line in lines:
        result = _process(store, line)
        if result is not None:
            out.append(result)
    return out


def part2(lines: list[str]) -> list[str]:
    return part1(lines)


def part3(lines: list[str]) -> list[str]:
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
