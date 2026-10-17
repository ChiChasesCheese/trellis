"""办公室人数追踪：任意时刻楼里有多少人，某段时间里最多有多少人。

设计五行：
1. 不存「人数」，存进出事件 (时间, 人, +1/-1)；任一时刻的人数是该时刻之前所有事件的前缀和。
2. 事件按时间追加，所以前缀和数组也只追加；`Timeline` 用二分查找回答「t 时刻多少人」。
3. 区间最大值用一棵只追加的线段树（`_MaxTree`），查询 O(log n)。
4. 楼层／楼栋是 `zone`：每个 zone 一条 `Timeline`，再加一条全局的；重复的重试事件被忽略，倒流的事件被拒绝。
5. 同一个模型可以直接写成 SQL（`SQL_COUNT_AT`、`SQL_MAX_IN`），测试里与内存版对拍。
"""

from __future__ import annotations

import bisect
import sqlite3
import threading
from collections.abc import Iterable
from dataclasses import dataclass

ALL = None  # 查询时 zone=ALL 表示整个办公室


class OccupancyError(Exception):
    """人数追踪的错误基类。"""


class AlreadyInside(OccupancyError):
    """这个人已经在楼里，又收到一次不同的进入事件。"""


class NotInside(OccupancyError):
    """这个人不在楼里，却收到离开事件。"""


class OutOfOrder(OccupancyError):
    """事件时间比已入账的最后一个事件更早。"""


@dataclass(frozen=True)
class Event:
    ts: int  # Unix 秒，由调用方给出；追踪器从不读系统时钟
    person: str
    zone: str
    delta: int  # +1 进入，-1 离开


class _MaxTree:
    """只追加的区间最大值线段树。容量不够时翻倍重建，append 摊还 O(1)，query O(log n)。"""

    _NEG = -(10**18)

    def __init__(self) -> None:
        self._cap = 1
        self._n = 0
        self._t = [self._NEG, self._NEG]

    def append(self, value: int) -> None:
        if self._n == self._cap:
            old = self._t[self._cap : self._cap + self._n]
            self._cap *= 2
            self._t = [self._NEG] * (2 * self._cap)
            self._t[self._cap : self._cap + len(old)] = old
            for i in range(self._cap - 1, 0, -1):
                self._t[i] = max(self._t[2 * i], self._t[2 * i + 1])
        i = self._cap + self._n
        self._t[i] = value
        self._n += 1
        i //= 2
        while i:
            self._t[i] = max(self._t[2 * i], self._t[2 * i + 1])
            i //= 2

    def query(self, lo: int, hi: int) -> int:
        """闭区间 [lo, hi] 的最大值；空区间返回极小值。"""
        result = self._NEG
        lo += self._cap
        hi += self._cap + 1
        while lo < hi:
            if lo & 1:
                result = max(result, self._t[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                result = max(result, self._t[hi])
            lo //= 2
            hi //= 2
        return result


class Timeline:
    """一条只追加的人数时间线：times[i] 是第 i 个事件的时间，counts[i] 是处理完它之后的人数。"""

    def __init__(self) -> None:
        self._times: list[int] = []
        self._counts: list[int] = []
        self._tree = _MaxTree()

    def append(self, ts: int, delta: int) -> None:
        count = (self._counts[-1] if self._counts else 0) + delta
        self._times.append(ts)
        self._counts.append(count)
        self._tree.append(count)

    @property
    def size(self) -> int:
        return len(self._times)

    def count_at(self, ts: int) -> int:
        """ts 这一秒结束时的人数：最后一个 time <= ts 的事件之后的前缀和，没有则 0。"""
        i = bisect.bisect_right(self._times, ts) - 1
        return self._counts[i] if i >= 0 else 0

    def max_in(self, start: int, end: int) -> int:
        """闭区间 [start, end] 内出现过的最大人数：区间开始时的人数，与区间内每个事件之后的人数，取最大。"""
        lo = bisect.bisect_left(self._times, start)
        hi = bisect.bisect_right(self._times, end) - 1
        best = self.count_at(start)
        return max(best, self._tree.query(lo, hi)) if lo <= hi else best


class OccupancyTracker:
    """接收进出事件，回答人数查询。事件必须按时间不递减地到达。"""

    def __init__(self) -> None:
        self._all = Timeline()
        self._zones: dict[str, Timeline] = {}
        self._last: dict[str, Event] = {}  # 每个人最近一次事件，用来判断重复与合法性
        self._events: list[Event] = []
        self._last_ts: int | None = None
        self._lock = threading.Lock()

    # ---- 写 ----
    def enter(self, person: str, ts: int, zone: str = "main") -> bool:
        """记录进入。新事件返回 True；与上一个事件完全相同的重试返回 False。"""
        return self._record(Event(ts, person, zone, +1))

    def leave(self, person: str, ts: int, zone: str = "main") -> bool:
        return self._record(Event(ts, person, zone, -1))

    def _record(self, ev: Event) -> bool:
        with self._lock:
            last = self._last.get(ev.person)
            if last == ev:
                return False  # 同一事件重投：忽略，不是错误
            inside = last is not None and last.delta == +1
            if ev.delta == +1 and inside:
                raise AlreadyInside(ev.person)
            if ev.delta == -1 and (not inside or last.zone != ev.zone):  # type: ignore[union-attr]
                raise NotInside(ev.person)
            if self._last_ts is not None and ev.ts < self._last_ts:
                raise OutOfOrder(f"{ev.ts} < {self._last_ts}")
            self._all.append(ev.ts, ev.delta)
            self._zones.setdefault(ev.zone, Timeline()).append(ev.ts, ev.delta)
            self._last[ev.person] = ev
            self._events.append(ev)
            self._last_ts = ev.ts
            return True

    # ---- 读 ----
    def _timeline(self, zone: str | None) -> Timeline | None:
        return self._all if zone is ALL else self._zones.get(zone)

    def current(self, zone: str | None = ALL) -> int:
        with self._lock:
            t = self._timeline(zone)
            return t.count_at(self._last_ts) if t is not None and self._last_ts is not None else 0

    def count_at(self, ts: int, zone: str | None = ALL) -> int:
        with self._lock:
            t = self._timeline(zone)
            return t.count_at(ts) if t is not None else 0

    def max_in(self, start: int, end: int, zone: str | None = ALL) -> int:
        if start > end:
            raise ValueError("start 不能大于 end")
        with self._lock:
            t = self._timeline(zone)
            return t.max_in(start, end) if t is not None else 0

    def who_is_inside_at(self, ts: int) -> frozenset[str]:
        """ts 时在楼里的人：回放事件，O(n)。"""
        with self._lock:
            inside: set[str] = set()
            for ev in self._events:
                if ev.ts > ts:
                    break
                (inside.add if ev.delta > 0 else inside.discard)(ev.person)
            return frozenset(inside)

    @property
    def events(self) -> tuple[Event, ...]:
        with self._lock:
            return tuple(self._events)


# ---- 同一个模型的 SQL 版本 ----
SQL_SCHEMA = """
CREATE TABLE presence_events (
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL, person TEXT NOT NULL, zone TEXT NOT NULL, delta INTEGER NOT NULL);
CREATE INDEX idx_presence_ts ON presence_events(ts)
"""
SQL_COUNT_AT = """
SELECT COALESCE(SUM(delta), 0) FROM presence_events
WHERE ts <= :t AND (:zone IS NULL OR zone = :zone)
"""
SQL_MAX_IN = """
WITH scoped AS (SELECT seq, ts, delta FROM presence_events WHERE (:zone IS NULL OR zone = :zone)),
running AS (SELECT ts, SUM(delta) OVER (ORDER BY ts, seq) AS cnt FROM scoped)
SELECT MAX(cnt) FROM (
  SELECT cnt FROM running WHERE ts BETWEEN :a AND :b
  UNION ALL
  SELECT COALESCE((SELECT SUM(delta) FROM scoped WHERE ts <= :a), 0)
)
"""


def load_sqlite(events: Iterable[Event]) -> sqlite3.Connection:
    """把事件灌进内存 SQLite；`seq` 在同一秒内给事件定序，窗口函数才有确定的顺序。"""
    db = sqlite3.connect(":memory:")
    db.executescript(SQL_SCHEMA)
    db.executemany(
        "INSERT INTO presence_events(ts, person, zone, delta) VALUES (?, ?, ?, ?)",
        [(e.ts, e.person, e.zone, e.delta) for e in events],
    )
    return db


if __name__ == "__main__":
    t = OccupancyTracker()
    for person, ts in (("a", 10), ("b", 20), ("c", 30)):
        t.enter(person, ts)
    t.leave("a", 40)
    t.enter("d", 40)
    print(t.count_at(25), t.count_at(45), t.max_in(41, 100))
