"""od09 Queue -> Service -- reference solution.

SimpleQueue is a thin wrapper around collections.deque (Part1). MessageQueue (Part2/3) adds a
ready deque of not-currently-delivered message ids, a payload dict, and an in-flight dict mapping
message_id -> (visible_at, delivery_seq). `dequeue` first sweeps in-flight entries whose
visibility deadline has passed back onto the *back* of the ready queue (ascending deadline order
-- the ones that timed out earliest re-enter the line first), mimicking a passive
visibility-timeout redelivery. `requeue_all_in_flight` (Part3's crash simulation) instead moves
every in-flight entry onto the *front* of the ready queue ordered by original delivery sequence
(earliest-delivered first), modelling "the service restarted and no longer trusts any
outstanding lease" -- oldest unfinished work gets reprocessed first, ahead of anything that was
never delivered yet.
"""

from __future__ import annotations

import sys
from collections import deque


class SimpleQueue:
    def __init__(self) -> None:
        self._dq: deque = deque()

    def enqueue(self, item: object) -> None:
        self._dq.append(item)

    def dequeue(self) -> object:
        return self._dq.popleft()

    def peek(self) -> object:
        return self._dq[0]

    def __len__(self) -> int:
        return len(self._dq)


class MessageQueue:
    def __init__(self) -> None:
        self._ready: deque[str] = deque()
        self._payloads: dict[str, object] = {}
        self._in_flight: dict[str, tuple[int, int]] = {}  # id -> (visible_at, delivery_seq)
        self._enqueue_seq = 0
        self._delivery_seq = 0

    def enqueue(self, payload: object) -> str:
        self._enqueue_seq += 1
        message_id = f"m{self._enqueue_seq}"
        self._payloads[message_id] = payload
        self._ready.append(message_id)
        return message_id

    def _requeue_expired(self, now: int) -> None:
        expired = sorted(
            (visible_at, seq, mid)
            for mid, (visible_at, seq) in self._in_flight.items()
            if visible_at <= now
        )
        for _visible_at, _seq, mid in expired:
            del self._in_flight[mid]
            self._ready.append(mid)

    def dequeue(self, now: int, visibility_timeout: int) -> "tuple[str, object] | None":
        self._requeue_expired(now)
        if not self._ready:
            return None
        message_id = self._ready.popleft()
        self._delivery_seq += 1
        self._in_flight[message_id] = (now + visibility_timeout, self._delivery_seq)
        return message_id, self._payloads[message_id]

    def ack(self, message_id: str) -> bool:
        if message_id not in self._in_flight:
            return False
        del self._in_flight[message_id]
        self._payloads.pop(message_id, None)
        return True

    def requeue_all_in_flight(self) -> int:
        items = sorted(
            (seq, mid) for mid, (_visible_at, seq) in self._in_flight.items()
        )  # ascending delivery seq: earliest-delivered first
        for _seq, mid in reversed(items):  # appendleft in reverse -> earliest ends up frontmost
            self._ready.appendleft(mid)
            del self._in_flight[mid]
        return len(items)


# ---------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    q = SimpleQueue()
    out: list[str] = []
    for raw in lines:
        fields = raw.split(" ", 1)
        verb = fields[0]
        try:
            if verb == "ENQ":
                q.enqueue(fields[1])
            elif verb == "DEQ":
                out.append(str(q.dequeue()))
            elif verb == "PEEK":
                out.append(str(q.peek()))
            else:
                raise ValueError(f"bad line: {raw!r}")
        except IndexError:
            out.append("ERROR:IndexError")
    return out


def part2(lines: list[str]) -> list[str]:
    mq = MessageQueue()
    out: list[str] = []
    for raw in lines:
        fields = raw.split()
        verb = fields[0]
        if verb == "ENQ":
            out.append(mq.enqueue(fields[1]))
        elif verb == "DEQ":
            result = mq.dequeue(int(fields[1]), int(fields[2]))
            out.append("None" if result is None else f"{result[0]} {result[1]}")
        elif verb == "ACK":
            out.append(str(mq.ack(fields[1])))
        else:
            raise ValueError(f"bad line: {raw!r}")
    return out


def part3(lines: list[str]) -> list[str]:
    mq = MessageQueue()
    out: list[str] = []
    for raw in lines:
        fields = raw.split()
        verb = fields[0]
        if verb == "ENQ":
            out.append(mq.enqueue(fields[1]))
        elif verb == "DEQ":
            result = mq.dequeue(int(fields[1]), int(fields[2]))
            out.append("None" if result is None else f"{result[0]} {result[1]}")
        elif verb == "ACK":
            out.append(str(mq.ack(fields[1])))
        elif verb == "CRASH":
            out.append(str(mq.requeue_all_in_flight()))
        else:
            raise ValueError(f"bad line: {raw!r}")
    return out


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
