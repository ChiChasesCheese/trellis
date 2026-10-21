"""办公室人数追踪（练习骨架）：补全每个方法体，使测试通过。

要点：存进出事件而不是人数；人数是前缀和；用二分回答「t 时刻多少人」；区间最大值要把
「区间开始时已在楼里的人」算进去；按 zone 分楼层；重复重试被忽略，时间倒流被拒绝；SQL 版同一模型。
"""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass

ALL = None  # 查询时 zone=ALL 表示整个办公室


class OccupancyError(Exception):
    """人数追踪的错误基类。"""


class AlreadyInside(OccupancyError):
    """这个人已经在楼里，又收到一次不同的进入事件。"""


class NotInside(OccupancyError):
    """这个人不在楼里（或不在这个 zone），却收到离开事件。"""


class OutOfOrder(OccupancyError):
    """事件时间比已入账的最后一个事件更早。"""


@dataclass(frozen=True)
class Event:
    ts: int
    person: str
    zone: str
    delta: int


class Timeline:
    """一条只追加的人数时间线（时间数组 + 前缀和数组 + 区间最大值结构）。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def append(self, ts: int, delta: int) -> None:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    def count_at(self, ts: int) -> int:
        """ts 这一秒结束时的人数。"""
        raise NotImplementedError

    def max_in(self, start: int, end: int) -> int:
        """闭区间 [start, end] 内出现过的最大人数。"""
        raise NotImplementedError


class OccupancyTracker:
    def __init__(self) -> None:
        raise NotImplementedError

    def enter(self, person: str, ts: int, zone: str = "main") -> bool:
        """新事件 True；与该人上一个事件完全相同的重试 False；非法序列抛对应异常且不改变状态。"""
        raise NotImplementedError

    def leave(self, person: str, ts: int, zone: str = "main") -> bool:
        raise NotImplementedError

    def current(self, zone: str | None = ALL) -> int:
        raise NotImplementedError

    def count_at(self, ts: int, zone: str | None = ALL) -> int:
        raise NotImplementedError

    def max_in(self, start: int, end: int, zone: str | None = ALL) -> int:
        raise NotImplementedError

    def who_is_inside_at(self, ts: int) -> frozenset[str]:
        raise NotImplementedError

    @property
    def events(self) -> tuple[Event, ...]:
        raise NotImplementedError


SQL_SCHEMA = """
CREATE TABLE presence_events (
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  ts INTEGER NOT NULL, person TEXT NOT NULL, zone TEXT NOT NULL, delta INTEGER NOT NULL);
CREATE INDEX idx_presence_ts ON presence_events(ts)
"""
SQL_COUNT_AT = "SELECT 0"  # 练习：参数 :t、:zone（NULL 表示全部）
SQL_MAX_IN = "SELECT 0"  # 练习：参数 :a、:b、:zone；窗口函数前缀和


def load_sqlite(events: Iterable[Event]) -> sqlite3.Connection:
    raise NotImplementedError
