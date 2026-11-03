"""餐厅候位（Restaurant Waitlist）——起始模板。公开的类名、签名和异常与 `solution.py` 一致。"""

from __future__ import annotations

from collections.abc import Callable, Sequence
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


class Restaurant:
    def __init__(self, table_sizes: Sequence[int], clock: Callable[[], datetime],
                 dining_time: timedelta = timedelta(minutes=60), max_overtakes: int | None = None) -> None:
        """table_sizes[i] 是 i 号桌的容量。桌子为空或有容量小于 1 的桌子抛 ValueError。

        clock 和 dining_time 第 2 关才用到；max_overtakes 第 3 关才用到（None 表示不限）。
        """
        raise NotImplementedError

    def join(self, party_id: str, size: int) -> int | None:
        """来了一桌客人。能立刻入座就返回桌号，否则排到队尾返回 None。

        入座规则：在容量够的空闲桌里选最小的，容量相同取编号小的。
        size < 1 抛 InvalidPartyError；size 超过最大的桌子抛 PartyTooLargeError；
        party_id 已在排队或用餐抛 DuplicatePartyError。失败时不改变任何状态。
        """
        raise NotImplementedError

    def leave(self, party_id: str) -> None:
        """排队的客人走了。不在排队（包括已入座）抛 UnknownPartyError。走了之后同一个 id 可以再 join。"""
        raise NotImplementedError

    def finish(self, party_id: str) -> list[tuple[str, int]]:
        """用餐结束，桌子空出来；返回因此新入座的 (party_id, 桌号)，按入座先后。

        规则：从队首往后，第一个坐得下的人入座（前面坐不下的人留在队里，保持相对顺序）。
        不在用餐抛 UnknownPartyError。
        """
        raise NotImplementedError

    def queue(self) -> list[str]:
        """排队中的 party_id，从队首到队尾，返回新列表。"""
        raise NotImplementedError

    def table_of(self, party_id: str) -> int | None:
        """已入座返回桌号，否则 None。"""
        raise NotImplementedError

    def estimate_wait(self, party_id: str) -> timedelta:
        """第 2 关：排队中的客人预计还要等多久。已入座返回 timedelta(0)；不认识抛 UnknownPartyError。

        推演：每桌的空出时刻 = 入座时间 + dining_time（已超时的算现在就空），桌子空出时用和实际
        完全相同的入座规则安排队伍。
        """
        raise NotImplementedError

    def quote(self, size: int) -> timedelta:
        """第 2 关：此刻来一桌 size 人（排到队尾）预计要等多久；不改变任何状态。size 不合法同 join。"""
        raise NotImplementedError

    # 第 3 关：max_overtakes 不为 None 时，一个人被排在后面的人插队 max_overtakes 次之后，
    # 就挡在所有后面的人前面：他没坐下之前，后面的人即使有空桌也不能坐。0 表示严格先来先坐。
    # 被挡住的人在挡路者入座或离开之后，会在同一次调用里被安排。估计也要遵守同样的规则。

    def change_size(self, party_id: str, size: int) -> list[tuple[str, int]]:
        """第 4 关：排队中的客人改人数，位置和被插队次数不变；返回因此新入座的 (party_id, 桌号)。

        不在排队抛 UnknownPartyError；新人数不合法同 join，且失败时保持原样。
        """
        raise NotImplementedError
