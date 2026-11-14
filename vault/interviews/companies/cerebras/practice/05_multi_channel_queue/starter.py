"""Multi-channel message queue: channels as bits, fan-out by intersection, union-find over shared channels,
and the fewest channels for a set of producer -> consumer patterns.

    uv run --project <repo root> python starter.py      # a short demo
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Iterable

# ---------------------------------------------------------------- Part 1: the queue


@dataclass(frozen=True)
class Message:
    id: int
    producer: str
    channels: frozenset[str]
    payload: Any


def bits_to_names(mask: int, names: list[str]) -> set[str]:
    raise NotImplementedError


class MessageQueue:
    """Each channel is one bit; a participant's channels are an int used as a bit set, so "which channels do
    these two share" is one AND (C/64 machine words for C channels) instead of a set intersection.

    Delivery is push: enqueue looks up the subscribers of each tagged channel, takes the union (a consumer on two of
    the tags still gets the message once) and appends to each recipient's inbox. Consumers only get messages
    enqueued while they are subscribed."""

    def __init__(self, channels: Iterable[str] = ()):
        raise NotImplementedError

    # channels
    def add_channel(self, name: str) -> int:
        raise NotImplementedError

    def channel_mask(self, names: Iterable[str]) -> int:
        raise NotImplementedError

    # subscriptions
    def subscribe(self, consumer: str, channel: str) -> None:
        raise NotImplementedError

    def unsubscribe(self, consumer: str, channel: str) -> None:
        raise NotImplementedError

    def subscriptions(self, consumer: str) -> set[str]:
        raise NotImplementedError

    # messages
    def enqueue(self, producer: str, channels: Iterable[str], payload: Any) -> int:
        raise NotImplementedError

    def consume(self, consumer: str, max_n: int | None = None) -> list[Message]:
        raise NotImplementedError

    def pending(self, consumer: str) -> int:
        raise NotImplementedError

    def shared_channels(self, a: str, b: str) -> set[str]:
        raise NotImplementedError

    def _mask_of(self, who: str) -> int:
        raise NotImplementedError

    # Part 2 on live state
    def share_groups(self) -> list[list[str]]:
        raise NotImplementedError


# ---------------------------------------------------------------- Part 2: union-find


class UnionFind:
    """Disjoint sets with path halving + union by size: each operation is O(alpha(n)), effectively constant."""

    def __init__(self):
        raise NotImplementedError

    def add(self, x) -> None:
        raise NotImplementedError

    def find(self, x):
        raise NotImplementedError

    def union(self, a, b) -> bool:
        raise NotImplementedError


def groups(memberships: dict[str, Iterable[str]]) -> list[list[str]]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 3: fewest channels, isolation rule


def plan_channels(pairs: Iterable[tuple[str, str]]) -> dict[str, str]:
    raise NotImplementedError


def min_channels(pairs: Iterable[tuple[str, str]]) -> int:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 4 (stretch): exact delivery


def min_channels_exact(pairs: Iterable[tuple[str, str]], limit: int = 14) -> list[tuple[frozenset, frozenset]]:
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
