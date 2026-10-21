"""办公室人数追踪：任意时刻有多少人、某时刻的人数、某个区间内的最大人数。

运行：`python3 -I occupancy_tracker.py`（assert 全过打印 OK）。讲解见上一级 `occupancy_tracker.md`。

核心想法：**不存"人数"，存"进出事件"**。每个事件是 (时间, +1 或 -1)；某时刻的人数 = 该时刻及之前所有事件的前缀和。
事件按时间追加，所以前缀和数组 `counts[i]` 也是追加的；"某时刻人数"是一次二分查找，
"区间最大人数"是对 `counts` 的区间最大值查询——用一棵可追加的线段树做到 O(log n)。
同样的模型可以直接写成 SQL（窗口函数前缀和），测试里用标准库 sqlite3 验证两者答案一致。
"""

from __future__ import annotations

import bisect
import sqlite3
from dataclasses import dataclass


class OccupancyError(Exception):
    pass


class AlreadyInside(OccupancyError):
    pass


class NotInside(OccupancyError):
    pass


class OutOfOrder(OccupancyError):
    pass


class _MaxTree:
    """可追加的区间最大值线段树（迭代式，容量翻倍）。append 摊还 O(1)，query O(log n)。"""

    _NEG = -(10 ** 18)

    def __init__(self) -> None:
        self._cap = 1
        self._n = 0
        self._t = [self._NEG, self._NEG]

    def append(self, value: int) -> None:
        if self._n == self._cap:
            old = self._t[self._cap:self._cap + self._n]
            self._cap *= 2
            self._t = [self._NEG] * (2 * self._cap)
            self._t[self._cap:self._cap + len(old)] = old
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
        if lo > hi:
            return self._NEG
        res = self._NEG
        lo += self._cap
        hi += self._cap + 1
        while lo < hi:
            if lo & 1:
                res = max(res, self._t[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                res = max(res, self._t[hi])
            lo //= 2
            hi //= 2
        return res


@dataclass(frozen=True)
class Event:
    ts: int            # Unix 秒，由调用方给（不读系统时钟）
    person: str
    delta: int         # +1 进入，-1 离开


class OccupancyTracker:
    """时间非递减地追加事件。相同时间戳的多个事件按到达顺序处理（"同一秒内先出后进"由调用方的到达顺序决定）。"""

    def __init__(self) -> None:
        self._times: list[int] = []        # 事件时间，非递减
        self._counts: list[int] = []       # counts[i] = 处理完第 i 个事件之后的人数
        self._inside: set[str] = set()
        self._tree = _MaxTree()
        self.events: list[Event] = []

    # ── 写 ──
    def enter(self, person: str, ts: int) -> None:
        if person in self._inside:
            raise AlreadyInside(person)
        self._append(Event(ts, person, +1))
        self._inside.add(person)

    def leave(self, person: str, ts: int) -> None:
        if person not in self._inside:
            raise NotInside(person)
        self._append(Event(ts, person, -1))
        self._inside.remove(person)

    def _append(self, ev: Event) -> None:
        if self._times and ev.ts < self._times[-1]:
            raise OutOfOrder(f"{ev.ts} < {self._times[-1]}")
        prev = self._counts[-1] if self._counts else 0
        self._times.append(ev.ts)
        self._counts.append(prev + ev.delta)
        self._tree.append(prev + ev.delta)
        self.events.append(ev)

    # ── 读 ──
    def current(self) -> int:
        return len(self._inside)

    def count_at(self, ts: int) -> int:
        """时刻 ts（含）的人数：最后一个 ≤ ts 的事件之后的前缀和。O(log n)。"""
        i = bisect.bisect_right(self._times, ts) - 1
        return self._counts[i] if i >= 0 else 0

    def max_in(self, start: int, end: int) -> int:
        """闭区间 [start, end] 内出现过的最大人数 = max(区间开始时的人数, 区间内每个事件之后的人数)。"""
        if start > end:
            raise ValueError("start > end")
        best = self.count_at(start)
        lo = bisect.bisect_left(self._times, start)
        hi = bisect.bisect_right(self._times, end) - 1
        return max(best, self._tree.query(lo, hi))

    def who_is_inside_at(self, ts: int) -> set[str]:
        """时刻 ts 在办公室的人：回放事件（O(n)）。需要频繁查询时应维护每人的访问区间，见讲解文档。"""
        inside: set[str] = set()
        for ev in self.events:
            if ev.ts > ts:
                break
            (inside.add if ev.delta > 0 else inside.discard)(ev.person)
        return inside


# ───────────────────────────── 同一个模型的 SQL 版本 ─────────────────────────────

SQL_COUNT_AT = "SELECT COALESCE(SUM(delta), 0) FROM presence_events WHERE ts <= :t"
SQL_MAX_IN = """
WITH running AS (
  SELECT ts, SUM(delta) OVER (ORDER BY ts, seq) AS cnt FROM presence_events
)
SELECT MAX(cnt) FROM (
  SELECT cnt FROM running WHERE ts BETWEEN :a AND :b
  UNION ALL
  SELECT COALESCE((SELECT SUM(delta) FROM presence_events WHERE ts <= :a), 0)
)
"""


def _sql_db(events: list[Event]) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE presence_events (seq INTEGER PRIMARY KEY, ts INTEGER NOT NULL, person TEXT NOT NULL, delta INTEGER NOT NULL)")
    db.execute("CREATE INDEX idx_ts ON presence_events(ts)")
    db.executemany("INSERT INTO presence_events(ts, person, delta) VALUES (?, ?, ?)", [(e.ts, e.person, e.delta) for e in events])
    return db


# ───────────────────────────── 测试 ─────────────────────────────

def _run_tests() -> None:
    t = OccupancyTracker()
    assert t.current() == 0 and t.count_at(100) == 0 and t.max_in(0, 100) == 0     # 空：全是 0
    t.enter("a", 10)
    t.enter("b", 20)
    t.enter("c", 30)
    t.leave("a", 40)
    t.enter("d", 40)            # 同一秒：先出后进（到达顺序），人数在 40 这一秒结束时仍是 3
    t.leave("b", 50)
    t.leave("c", 60)
    assert t.current() == 1

    # count_at：事件之前 0，事件时刻含，之后保持
    assert [t.count_at(x) for x in (5, 10, 15, 20, 29, 30, 39, 40, 45, 50, 59, 60, 1000)] == [0, 1, 1, 2, 2, 3, 3, 3, 3, 2, 2, 1, 1]
    # max_in：区间开始时就已有的人数也要算；区间内峰值；闭区间端点
    assert t.max_in(0, 5) == 0
    assert t.max_in(10, 10) == 1
    assert t.max_in(0, 1000) == 3
    assert t.max_in(35, 39) == 3        # 区间内无事件：取开始时的人数
    assert t.max_in(41, 100) == 3       # 40 秒的最终人数 3 是区间开始时的状态
    assert t.max_in(50, 100) == 2
    assert t.max_in(61, 100) == 1
    assert t.who_is_inside_at(45) == {"b", "c", "d"} and t.who_is_inside_at(1000) == {"d"}

    # 非法序列
    for fn, exc in ((lambda: t.enter("d", 70), AlreadyInside), (lambda: t.leave("zz", 70), NotInside),
                    (lambda: t.enter("e", 55), OutOfOrder)):
        try:
            fn()
        except exc:
            pass
        else:
            raise AssertionError(exc.__name__)
    assert t.current() == 1                         # 失败的调用不改变状态

    # 线段树：随机对拍（暴力 vs 线段树 vs SQL），覆盖扩容
    import random
    rng = random.Random(7)
    big = OccupancyTracker()
    now = 0
    people_in: list[str] = []
    for i in range(400):
        now += rng.choice([0, 0, 1, 2, 5])
        if people_in and rng.random() < 0.45:
            p = people_in.pop(rng.randrange(len(people_in)))
            big.leave(p, now)
        else:
            p = f"p{i}"
            big.enter(p, now)
            people_in.append(p)
    db = _sql_db(big.events)

    def brute_count(ts: int) -> int:
        return sum(e.delta for e in big.events if e.ts <= ts)

    def brute_max(a: int, b: int) -> int:
        best = brute_count(a)
        cur = 0
        for e in big.events:
            cur += e.delta
            if a <= e.ts <= b:
                best = max(best, cur)
        return best

    for _ in range(200):
        a = rng.randrange(-3, now + 3)
        b = a + rng.randrange(0, 60)
        assert big.count_at(a) == brute_count(a) == db.execute(SQL_COUNT_AT, {"t": a}).fetchone()[0]
        assert big.max_in(a, b) == brute_max(a, b) == db.execute(SQL_MAX_IN, {"a": a, "b": b}).fetchone()[0]


if __name__ == "__main__":
    _run_tests()
    print("OK occupancy_tracker")
