"""od09 Queue -> Service -- YOUR implementation. Run pytest against this file with IMPL=starter.

See problem.md for the full contract: Part1 raises IndexError like collections.deque, Part2's
visibility timeout is half-open and only affects un-acked in-flight messages, and Part3's
requeue_all_in_flight orders by original delivery sequence (earliest first), not by expiry time.
"""

from __future__ import annotations

import sys
from collections import deque


class SimpleQueue:
    def __init__(self) -> None:
        pass  # TODO: a deque

    def enqueue(self, item: object) -> None:
        raise NotImplementedError  # TODO

    def dequeue(self) -> object:
        """IndexError on empty (matches collections.deque.popleft())."""
        raise NotImplementedError  # TODO

    def peek(self) -> object:
        """IndexError on empty. Does not remove the item."""
        raise NotImplementedError  # TODO

    def __len__(self) -> int:
        raise NotImplementedError  # TODO


class MessageQueue:
    def __init__(self) -> None:
        pass  # TODO: ready queue, payloads, in-flight map (message_id -> (visible_at, seq))

    def enqueue(self, payload: object) -> str:
        """Returns a fresh message_id; the message is appended to the ready queue."""
        raise NotImplementedError  # TODO

    def dequeue(self, now: int, visibility_timeout: int) -> "tuple[str, object] | None":
        """First move any in-flight message whose visibility deadline is <= now back to the
        BACK of the ready queue (ascending deadline order), then pop the ready queue's front and
        mark it in-flight until now + visibility_timeout (half-open: expires exactly at that
        instant). None if nothing is ready after the requeue step."""
        raise NotImplementedError  # TODO

    def ack(self, message_id: str) -> bool:
        """True and permanently removes the message iff it is currently in-flight. False for an
        unknown id, an already-acked id, or one that has since timed out back to the ready
        queue (a late ack must not affect its next delivery)."""
        raise NotImplementedError  # TODO

    def requeue_all_in_flight(self) -> int:
        """(reconstructed, Part3) Immediately move every currently in-flight message back to the
        FRONT of the ready queue, ordered by original delivery sequence (earliest-delivered
        ends up frontmost) -- NOT by expiry time, unlike the timeout path in dequeue(). Returns
        how many messages were moved. Acked messages are already gone and unaffected."""
        raise NotImplementedError  # TODO


def part1(lines: list[str]) -> list[str]:
    """Drive a fresh SimpleQueue from ENQ/DEQ/PEEK lines."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """Drive a fresh MessageQueue from ENQ/DEQ/ACK lines."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """Same driver as part2, plus a CRASH line -> requeue_all_in_flight()."""
    # TODO
    return []


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
