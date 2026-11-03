"""餐厅候位（Restaurant Waitlist）：排队、按桌型入座、预计等待时间。

核心思路：所有"谁坐哪张桌"的决定都集中在一个纯函数 `_drain` 里——给它排队列表、空闲桌子和
规则，它按队伍顺序把能坐的人都安排上并返回结果。真实的 `join` / `finish` 用它改真状态；
等位估计 `_simulate` 把状态复制一份，在复制品上用同一个 `_drain` 往前推演时间。
策略只写一遍，"预测"和"实际"就不会各说各话。
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta


class RestaurantError(Exception):
    """所有失败路径的公共基类。"""


class InvalidPartyError(RestaurantError, ValueError):
    """人数不合法（小于 1）。"""


class PartyTooLargeError(InvalidPartyError):
    """人数超过最大的桌子，永远排不上。"""


class DuplicatePartyError(RestaurantError):
    """这个 party_id 正在排队或正在用餐。"""


class UnknownPartyError(RestaurantError):
    """这个 party_id 不在该操作要求的状态里（比如 leave 一个已入座的）。"""


@dataclass(slots=True)
class _Waiting:
    id: str
    size: int
    skipped: int = 0  # 第 3 关：已经被排在后面的人插队多少次


def _best_fit(size: int, free: set[int], sizes: Sequence[int]) -> int | None:
    """能坐下的空闲桌里选最小的（大桌留给大团），容量相同取编号小的。"""
    fit = min(((sizes[t], t) for t in free if sizes[t] >= size), default=None)
    return None if fit is None else fit[1]


def _drain(queue: list[_Waiting], free: set[int], sizes: Sequence[int],
           max_overtakes: int | None) -> list[tuple[_Waiting, int]]:
    """按队伍顺序把现在能安排的都安排上。就地修改 queue 和 free，返回 (人, 桌号) 列表。

    第 1 关的规则：从队首往后找，第一个有桌可坐的人入座，然后重新从头找，直到没人能坐。
    第 3 关的规则：某人被插队次数达到 max_overtakes，就挡在所有后面的人前面。
    """
    seated: list[tuple[_Waiting, int]] = []
    while True:
        for i, w in enumerate(queue):
            table = _best_fit(w.size, free, sizes)
            if table is not None:
                for earlier in queue[:i]:
                    earlier.skipped += 1
                del queue[i]
                free.remove(table)
                seated.append((w, table))
                break
            if max_overtakes is not None and w.skipped >= max_overtakes:
                return seated  # 他自己坐不了，又不许后面的人再越过他
        else:
            return seated


class Restaurant:
    def __init__(self, table_sizes: Sequence[int], clock: Callable[[], datetime],
                 dining_time: timedelta = timedelta(minutes=60), max_overtakes: int | None = None) -> None:
        if not table_sizes or any(n < 1 for n in table_sizes):
            raise ValueError("need at least one table, every table seats 1 or more")
        self._sizes = list(table_sizes)
        self._clock, self._dining, self._max_overtakes = clock, dining_time, max_overtakes
        self._free = set(range(len(self._sizes)))
        self._queue: list[_Waiting] = []
        self._seated: dict[str, tuple[int, datetime]] = {}  # party -> (桌号, 入座时间)

    # ---------------------------------------------------------------- 第 1 关

    def join(self, party_id: str, size: int) -> int | None:
        """来了一桌客人。能立刻入座就返回桌号，否则排到队尾返回 None。"""
        self._check_size(size)
        if party_id in self._seated or any(w.id == party_id for w in self._queue):
            raise DuplicatePartyError(party_id)
        self._queue.append(_Waiting(party_id, size))
        self._seat_everyone_possible()
        return self.table_of(party_id)

    def leave(self, party_id: str) -> None:
        """排队的客人走了。"""
        for i, w in enumerate(self._queue):
            if w.id == party_id:
                del self._queue[i]
                self._seat_everyone_possible()  # 第 3 关：挡路的人走了，后面的人可能能坐了
                return
        raise UnknownPartyError(party_id)

    def finish(self, party_id: str) -> list[tuple[str, int]]:
        """用餐结束，桌子空出来；返回因此新入座的 (party_id, 桌号)，按入座先后。"""
        if party_id not in self._seated:
            raise UnknownPartyError(party_id)
        table, _ = self._seated.pop(party_id)
        self._free.add(table)
        return self._seat_everyone_possible()

    def queue(self) -> list[str]:
        return [w.id for w in self._queue]

    def table_of(self, party_id: str) -> int | None:
        entry = self._seated.get(party_id)
        return entry[0] if entry else None

    def _check_size(self, size: int) -> None:
        if size < 1:
            raise InvalidPartyError(f"party size must be at least 1, got {size}")
        if size > max(self._sizes):
            raise PartyTooLargeError(f"no table seats {size}")

    def _seat_everyone_possible(self) -> list[tuple[str, int]]:
        now = self._clock()
        placed = _drain(self._queue, self._free, self._sizes, self._max_overtakes)
        for w, table in placed:
            self._seated[w.id] = (table, now)
        return [(w.id, table) for w, table in placed]

    # ---------------------------------------------------------------- 第 2 关：等位估计

    def estimate_wait(self, party_id: str) -> timedelta:
        """一个排队中的客人预计还要等多久；已入座返回 0；不认识抛 UnknownPartyError。"""
        if party_id in self._seated:
            return timedelta(0)
        if not any(w.id == party_id for w in self._queue):
            raise UnknownPartyError(party_id)
        return self._simulate([_Waiting(w.id, w.size, w.skipped) for w in self._queue], party_id)

    def quote(self, size: int) -> timedelta:
        """现在来一桌 size 人，预计要等多久；不会改变任何状态。"""
        self._check_size(size)
        probe = "\0quote"
        queue = [_Waiting(w.id, w.size, w.skipped) for w in self._queue] + [_Waiting(probe, size)]
        return self._simulate(queue, probe)

    def _simulate(self, queue: list[_Waiting], target: str) -> timedelta:
        """在复制品上往前推演：每张忙桌的空出时刻 = 入座时间 + 用餐时长（超时的算现在就空）。"""
        now = self._clock()
        free = set(self._free)
        busy = {table: max(now, at + self._dining) for table, at in self._seated.values()}
        t = now
        while True:
            for w, table in _drain(queue, free, self._sizes, self._max_overtakes):
                if w.id == target:
                    return t - now
                busy[table] = t + self._dining
            t = min(busy.values())  # 下一个桌子空出来的时刻
            for table in [tb for tb, ft in busy.items() if ft <= t]:
                del busy[table]
                free.add(table)

    # ---------------------------------------------------------------- 第 4 关

    def change_size(self, party_id: str, size: int) -> list[tuple[str, int]]:
        """排队中的客人改人数：位置和被插队次数不变；返回因此新入座的 (party_id, 桌号)。"""
        waiting = next((w for w in self._queue if w.id == party_id), None)
        if waiting is None:
            raise UnknownPartyError(party_id)
        self._check_size(size)
        waiting.size = size
        return self._seat_everyone_possible()
