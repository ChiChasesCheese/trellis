"""会议室预订（Meeting Scheduler）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/meeting-scheduler -q
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum
from zoneinfo import ZoneInfo


class SchedulerError(Exception):
    """本设计里所有失败路径的公共基类。"""

class InvalidIntervalError(SchedulerError):
    """区间本身不合法：结束时刻不晚于开始时刻。"""

class RoomNotFoundError(SchedulerError):
    """目录里没有这间会议室。"""

class RoomUnavailableError(SchedulerError):
    """这间房在请求的时间段里已经被占用。"""

class MeetingNotFoundError(SchedulerError):
    """会议号或周期系列号不存在。"""


class Equipment(Enum):
    """会议室的设备。"""

    PROJECTOR = "projector"
    VIDEO_CONF = "video_conf"
    WHITEBOARD = "whiteboard"
    PHONE = "phone"


@dataclass(frozen=True, slots=True)
class Room:
    """一间物理会议室：容量与设备固定，不带任何占用状态。"""

    id: str
    name: str
    capacity: int
    equipment: frozenset[Equipment] = frozenset()

    def fits(self, attendees: int, required: frozenset[Equipment]) -> bool:
        """这间房坐得下这么多人、配得齐这些设备。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Interval:
    """半开区间 `[start, end)`：两端都是带时区的具体时刻。"""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        raise NotImplementedError

    def overlaps(self, other: "Interval") -> bool:
        """两个区间是否有公共时刻。"""
        raise NotImplementedError

    @property
    def duration(self) -> timedelta:
        """这段区间有多长。"""
        raise NotImplementedError


def merge_intervals(intervals: Sequence[Interval]) -> tuple[Interval, ...]:
    """把一组可能重叠、可能相邻的区间合并成互不重叠的最少区间数。"""
    raise NotImplementedError


def free_gaps(busy: Sequence[Interval], window: Interval, min_duration: timedelta) -> tuple[Interval, ...]:
    """在 `window` 内、`busy` 之外，找出所有不短于 `min_duration` 的空档。"""
    raise NotImplementedError


@dataclass(slots=True)
class Meeting:
    """一次性会议：房间、时间、发起人与与会者。"""

    id: str
    room_id: str
    interval: Interval
    organizer: str
    attendees: tuple[str, ...]


class ExceptionKind(Enum):
    """一次例外是整场取消，还是只改了这一天的时间或时长。"""

    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


@dataclass(frozen=True, slots=True)
class OccurrenceException:
    """周期会议里，单独某一天相对规则的差异。"""

    kind: ExceptionKind
    local_start: time | None = None
    duration: timedelta | None = None


@dataclass(frozen=True, slots=True)
class RecurrenceRule:
    """按周几重复，可以隔周；`until` 是最后一次生效的日期（含），`None` 表示不封顶。"""

    weekdays: frozenset[int]
    interval_weeks: int = 1
    until: date | None = None

    def dates_in(self, start: date, end: date, series_start: date) -> Iterator[date]:
        """这条规则在 `[start, end)` 里落在哪些具体日期上。"""
        raise NotImplementedError


class RecurringSeries:
    """一条周期会议规则：房间、参与者、重复模式，以及按天记的例外表和它自己的锁。"""

    def __init__(self, series_id: str, room_id: str, organizer: str, attendees: Sequence[str],
                 local_start: time, duration: timedelta, zone: ZoneInfo, rule: RecurrenceRule,
                 series_start: date) -> None:
        raise NotImplementedError

    @property
    def participants(self) -> frozenset[str]:
        """发起人和与会者合在一起的集合。"""
        raise NotImplementedError

    @property
    def exception_count(self) -> int:
        """当前记着多少条例外。"""
        raise NotImplementedError

    def cancel_occurrence(self, day: date) -> None:
        """只取消这一天这一场。"""
        raise NotImplementedError

    def reschedule_occurrence(self, day: date, local_start: time | None = None,
                              duration: timedelta | None = None) -> None:
        """只改这一天这一场的时间或时长。"""
        raise NotImplementedError

    def freeze_after(self, cutoff: date) -> None:
        """把规则的生效范围封在 `cutoff` 前一天，并清掉再也查不到的未来例外。"""
        raise NotImplementedError

    def occurrence_on(self, day: date) -> Interval | None:
        """这一天这场会议的具体区间（已按例外调整），被取消则是 `None`。"""
        raise NotImplementedError

    def occurrences_in(self, window: Interval) -> tuple[Interval, ...]:
        """展开这条规则在 `window` 里落地的所有场次。"""
        raise NotImplementedError


class RoomCalendar:
    """一间会议室自己的日程：一次性会议 + 挂在这间房的周期系列，一把私有锁守住"查完再写"。"""

    def __init__(self, room: Room) -> None:
        raise NotImplementedError

    def busy_with(self, window: Interval) -> tuple[tuple[frozenset[str], Interval], ...]:
        """`window` 内每一段忙碌区间的只读快照，连同"谁在忙"。"""
        raise NotImplementedError

    def is_free(self, interval: Interval) -> bool:
        """这段时间这间房完全没人占。"""
        raise NotImplementedError

    def reserve(self, meeting: Meeting) -> None:
        """把一次性会议钉进这间房：检查与写入在同一把锁里完成。"""
        raise NotImplementedError

    def cancel(self, meeting_id: str) -> bool:
        """取消一次性会议，把房间还回去。幂等。"""
        raise NotImplementedError

    def add_series(self, series: RecurringSeries, horizon: Interval) -> None:
        """挂一条周期系列：只在 `horizon` 这段可核验的窗口内查冲突。"""
        raise NotImplementedError

    @property
    def meeting_count(self) -> int:
        """这间房眼下挂着几笔一次性会议。"""
        raise NotImplementedError

    @property
    def series_count(self) -> int:
        """这间房眼下挂着几条周期系列。"""
        raise NotImplementedError


class MeetingSchedulerService:
    """会议室预订服务：注册房间、订一次性会议、给一组人找空档配房、管理周期会议。"""

    def __init__(self, default_horizon: timedelta = timedelta(days=90)) -> None:
        raise NotImplementedError

    def register_room(self, room: Room) -> None:
        """把一间会议室加进目录。"""
        raise NotImplementedError

    def room(self, room_id: str) -> Room:
        """按 id 取房间；不存在就抛 `RoomNotFoundError`。"""
        raise NotImplementedError

    @property
    def room_count(self) -> int:
        """目录里有几间房。"""
        raise NotImplementedError

    def meeting_count(self, room_id: str) -> int:
        """这间房眼下挂着几笔一次性会议。"""
        raise NotImplementedError

    def series_count(self, room_id: str) -> int:
        """这间房眼下挂着几条周期系列。"""
        raise NotImplementedError

    def occupied_intervals(self, room_id: str, window: Interval) -> tuple[Interval, ...]:
        """这间房在 `window` 内每一段忙碌区间的只读快照，按开始时间排序。"""
        raise NotImplementedError

    def book_meeting(self, room_id: str, organizer: str, attendees: Sequence[str],
                     interval: Interval) -> Meeting:
        """订一间房、一个时间段。房间忙着就抛异常。"""
        raise NotImplementedError

    def cancel_meeting(self, meeting_id: str) -> None:
        """取消一次性会议，把房间还回去。"""
        raise NotImplementedError

    def find_slot(self, attendees: Sequence[str], duration: timedelta, window: Interval,
                  equipment: frozenset[Equipment] = frozenset()) -> tuple[Interval, Room] | None:
        """给这组人找最早的、时长够、能配到房的空档；房间挑坐得下这组人的最小那间。"""
        raise NotImplementedError

    def schedule_series(self, room_id: str, organizer: str, attendees: Sequence[str],
                        local_start: time, duration: timedelta, zone: ZoneInfo,
                        rule: RecurrenceRule, series_start: date,
                        horizon: timedelta | None = None) -> RecurringSeries:
        """挂一条周期会议。只在 `horizon`（默认 90 天）内核验冲突。"""
        raise NotImplementedError

    def series(self, series_id: str) -> RecurringSeries:
        """按 id 取周期系列；不存在就抛 `MeetingNotFoundError`。"""
        raise NotImplementedError

    def split_series(self, series_id: str, from_day: date, local_start: time | None = None,
                     duration: timedelta | None = None, room_id: str | None = None) -> RecurringSeries:
        """"这一场及以后"的编辑：老规则在 `from_day` 前一天封顶，从 `from_day` 起开一条新系列接上。"""
        raise NotImplementedError
