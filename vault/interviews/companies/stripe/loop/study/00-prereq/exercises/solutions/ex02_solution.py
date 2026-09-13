"""ex02 参考答案。"""
from __future__ import annotations

import sys
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Event:
    ts: int
    kind: str
    amount: int


def parse_events(lines: list[str]) -> list[Event]:
    out: list[Event] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        ts, kind, amount = line.split(",")
        out.append(Event(int(ts), kind, int(amount)))
    return out


class Counter2:
    def __init__(self) -> None:
        self.counts: dict[str, int] = defaultdict(int)

    def add(self, kind: str) -> None:
        self.counts[kind] += 1

    def top(self) -> str | None:
        if not self.counts:
            return None
        # 次数降序、名字升序 → 取第一个。min 配 key 元组一步到位。
        return min(self.counts, key=lambda k: (-self.counts[k], k))


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    events = parse_events(stdin.read().splitlines())
    total: dict[str, int] = defaultdict(int)
    for e in events:
        total[e.kind] += e.amount
    for kind in sorted(total):
        stdout.write(f"{kind},{total[kind]}\n")


if __name__ == "__main__":
    main()
