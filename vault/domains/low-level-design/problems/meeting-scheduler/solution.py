"""会议室预订（Meeting Scheduler）——半开区间冲突检测、多人找空档、周期会议与时区的参考实现。

核心思路：一次占用是半开区间 `[start, end)`，`10:00–11:00` 和 `11:00–12:00` 因此天然相邻而不
重叠，判重叠只剩一行比较。房间的忙闲状态只长在 `RoomCalendar` 身上，一间房一把锁；"给几个人找
空档"是把这组人各自的忙碌区间合并（区间合并算法），再在查询窗口里找出比会议时长还宽的空档，最后
挑能坐下这组人的最小房间。周期会议存的是一条重复规则加一张按天记的例外表，只在被查询的窗口里
展开成具体场次，从不把整条规则物化成日历；"这一场"和"这一场及以后"是两种不同粒度的编辑，后者
把老规则在某天前封顶、开一条新规则接上。规则本身存的是本地墙钟时间加时区，而不是一个固定的 UTC
偏移量——同一个偏移量跨夏令时（DST）切换会让本地钟点整体错位，这正是本设计要避开的坑。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, replace
from datetime import date, datetime, time, timedelta
from enum import Enum
from zoneinfo import ZoneInfo


# --------------------------------------------------------------------------
# 失败路径：一个小的异常家族。

class SchedulerError(Exception):
    """本设计里所有失败路径的公共基类。"""

class InvalidIntervalError(SchedulerError):
    """区间本身不合法：结束时刻不晚于开始时刻。"""

class RoomNotFoundError(SchedulerError):
    """目录里没有这间会议室。"""

class RoomUnavailableError(SchedulerError):
    """这间房在请求的时间段（或周期系列覆盖的核验窗口）里已经被占用。"""

class MeetingNotFoundError(SchedulerError):
    """会议号或周期系列号不存在。"""


# --------------------------------------------------------------------------
# 房间与区间：全部不可变的数据。

class Equipment(Enum):
    """会议室的设备。字符串枚举，便于按名字匹配需求。"""

    PROJECTOR = "projector"
    VIDEO_CONF = "video_conf"
    WHITEBOARD = "whiteboard"
    PHONE = "phone"


@dataclass(frozen=True, slots=True)
class Room:
    """一间物理会议室：容量与设备固定，不带任何"这段时间被谁占着"的状态——
    占用是每个时刻都在变的库存事实，属于 `RoomCalendar`，不属于房间本身。
    """

    id: str
    name: str
    capacity: int
    equipment: frozenset[Equipment] = frozenset()

    def fits(self, attendees: int, required: frozenset[Equipment]) -> bool:
        """这间房坐得下这么多人、配得齐这些设备。"""
        return self.capacity >= attendees and required <= self.equipment


@dataclass(frozen=True, slots=True)
class Interval:
    """半开区间 `[start, end)`：两端都是带时区的具体时刻。

    半开是这道题最省事的约定：`10:00–11:00` 的会散场、`11:00–12:00` 的会开始，判重叠不需要
    任何 `-1` 或特判就能得出"不冲突"，见题解「关键设计决策」。
    """

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise InvalidIntervalError(f"end {self.end} must be after start {self.start}")

    def overlaps(self, other: "Interval") -> bool:
        """两个区间是否有公共时刻。"""
        return self.start < other.end and other.start < self.end

    @property
    def duration(self) -> timedelta:
        """这段区间有多长。"""
        return self.end - self.start


def merge_intervals(intervals: Sequence[Interval]) -> tuple[Interval, ...]:
    """把一组可能重叠、可能相邻的区间合并成互不重叠的最少区间数。

    按起点排序（O(n log n)）后做一次线性扫描（O(n)）：当前区间和结果里最后一个区间"挨得上或
    重叠"就合并，否则单独成一段。这是找空档之前必须做的预处理——不先合并，同一段忙碌时间被
    两个人各占一部分时会被误判成中间有一道缝。
    """
    if not intervals:
        return ()
    ordered = sorted(intervals, key=lambda iv: iv.start)
    merged = [ordered[0]]
    for iv in ordered[1:]:
        last = merged[-1]
        if iv.start <= last.end:  # 半开区间：端点相等也算挨上，必须合并，否则会留一条零宽假缝
            merged[-1] = Interval(last.start, max(last.end, iv.end))
        else:
            merged.append(iv)
    return tuple(merged)


def free_gaps(busy: Sequence[Interval], window: Interval, min_duration: timedelta) -> tuple[Interval, ...]:
    """在 `window` 内、`busy`（会先合并）之外，找出所有不短于 `min_duration` 的空档，按时间顺序。"""
    gaps: list[Interval] = []
    cursor = window.start
    for iv in merge_intervals(busy):
        start, end = max(iv.start, window.start), min(iv.end, window.end)
        if start >= end:
            continue
        if start - cursor >= min_duration:
            gaps.append(Interval(cursor, start))
        cursor = max(cursor, end)
    if window.end - cursor >= min_duration:
        gaps.append(Interval(cursor, window.end))
    return tuple(gaps)


# --------------------------------------------------------------------------
# 一次性会议。

@dataclass(slots=True)
class Meeting:
    """一次性会议：房间、时间、发起人与与会者。没有生命周期状态——存在即已确认，取消即删除。"""

    id: str
    room_id: str
    interval: Interval
    organizer: str
    attendees: tuple[str, ...]


# --------------------------------------------------------------------------
# 周期会议：重复规则 + 按天记的例外。

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

    weekdays: frozenset[int]  # 0=周一 … 6=周日，同 date.weekday()
    interval_weeks: int = 1
    until: date | None = None

    def dates_in(self, start: date, end: date, series_start: date) -> Iterator[date]:
        """这条规则在 `[start, end)` 里落在哪些具体日期上——只在被查询的窗口内展开，
        绝不把整条规则物化成一张无限长的日期表。
        """
        first_monday = series_start - timedelta(days=series_start.weekday())
        day = max(start, series_start)
        while day < end:
            if (self.until is None or day <= self.until) and day.weekday() in self.weekdays:
                monday = day - timedelta(days=day.weekday())
                if (monday - first_monday).days // 7 % self.interval_weeks == 0:
                    yield day
            day += timedelta(days=1)


class RecurringSeries:
    """一条周期会议规则：房间、参与者、重复模式，以及按天记的例外表和它自己的锁。

    本地墙钟时间（`local_start`）+ 时区（`zone`）才是这条规则的权威表示——同一个固定 UTC 偏移量
    跨夏令时切换会让本地钟点整体错位，见题解「关键设计决策」。这个类只管"这一天单独改不改"；
    "这一天及以后整体改"是更大粒度的编辑，由 `freeze_after` 配合
    `MeetingSchedulerService.split_series` 完成，不在这个类的职责里。
    """

    def __init__(self, series_id: str, room_id: str, organizer: str, attendees: Sequence[str],
                 local_start: time, duration: timedelta, zone: ZoneInfo, rule: RecurrenceRule,
                 series_start: date) -> None:
        self.id = series_id
        self.room_id = room_id
        self.organizer = organizer
        self.attendees = tuple(attendees)
        self.local_start = local_start
        self.duration = duration
        self.zone = zone
        self.rule = rule
        self.series_start = series_start
        self._exceptions: dict[date, OccurrenceException] = {}
        self._lock = threading.Lock()

    @property
    def participants(self) -> frozenset[str]:
        """发起人和与会者合在一起的集合——找空档时按这份名单判断谁在忙。"""
        return frozenset({self.organizer, *self.attendees})

    @property
    def exception_count(self) -> int:
        """当前记着多少条例外——用来验证 `freeze_after` 真的清掉了查不到的那些。"""
        with self._lock:
            return len(self._exceptions)

    def cancel_occurrence(self, day: date) -> None:
        """只取消这一天这一场，规则本身和其它日期不受影响。"""
        with self._lock:
            self._exceptions[day] = OccurrenceException(ExceptionKind.CANCELLED)

    def reschedule_occurrence(self, day: date, local_start: time | None = None,
                              duration: timedelta | None = None) -> None:
        """只改这一天这一场的时间或时长，规则本身和其它日期不受影响。"""
        with self._lock:
            self._exceptions[day] = OccurrenceException(ExceptionKind.RESCHEDULED, local_start, duration)

    def freeze_after(self, cutoff: date) -> None:
        """把规则的生效范围封在 `cutoff` 前一天，供"这一场及以后"的编辑使用；同时清掉再也
        查不到的未来例外——不这样做，`_exceptions` 就是一张只涨不跌的表。
        """
        with self._lock:
            self.rule = replace(self.rule, until=cutoff - timedelta(days=1))
            stale = [day for day in self._exceptions if day >= cutoff]
            for day in stale:
                del self._exceptions[day]

    def occurrence_on(self, day: date) -> Interval | None:
        """这一天这场会议的具体区间（已按例外调整），被取消则是 `None`。

        本地时间在这里才换算成带时区的具体时刻，逐天单独换算——`zoneinfo` 会按那一天的日期
        查出当天正确的 UTC 偏移，天然吃到夏令时切换，不需要任何"手动补一小时"的特判。
        """
        with self._lock:
            exc = self._exceptions.get(day)
        if exc is not None and exc.kind is ExceptionKind.CANCELLED:
            return None
        local_start = exc.local_start if exc and exc.local_start is not None else self.local_start
        duration = exc.duration if exc and exc.duration is not None else self.duration
        start = datetime.combine(day, local_start, tzinfo=self.zone)
        return Interval(start, start + duration)

    def occurrences_in(self, window: Interval) -> tuple[Interval, ...]:
        """展开这条规则在 `window` 里落地的所有场次——只算查询的这一段。"""
        start_date = window.start.astimezone(self.zone).date()
        end_date = window.end.astimezone(self.zone).date() + timedelta(days=1)
        days = self.rule.dates_in(start_date, end_date, self.series_start)
        occurrences = (self.occurrence_on(day) for day in days)
        return tuple(iv for iv in occurrences if iv is not None and iv.overlaps(window))


# --------------------------------------------------------------------------
# RoomCalendar：一间房自己的日程，本设计里唯一持有"忙闲"这份状态的对象。

class RoomCalendar:
    """一间会议室自己的日程：一次性会议 + 挂在这间房的周期系列，一把私有锁守住"查完再写"。

    竞争边界和数据边界在这里重合：两个组织者抢的是同一间房，锁就该长在房间这一层，不同房间
    之间零共享，天然不互相阻塞。读方法一律返回快照（一份新元组），从不交出内部字典本身。
    """

    def __init__(self, room: Room) -> None:
        self.room = room
        self._meetings: dict[str, Meeting] = {}
        self._series: dict[str, RecurringSeries] = {}
        self._lock = threading.Lock()

    def _collect_locked(self, window: Interval) -> list[tuple[frozenset[str], Interval]]:
        """`window` 内每一段忙碌区间，连同"谁在忙"。调用方必须已经持有 `self._lock`。"""
        out: list[tuple[frozenset[str], Interval]] = []
        for meeting in self._meetings.values():
            if meeting.interval.overlaps(window):
                out.append((frozenset({meeting.organizer, *meeting.attendees}), meeting.interval))
        for series in self._series.values():
            out.extend((series.participants, iv) for iv in series.occurrences_in(window))
        return out

    def busy_with(self, window: Interval) -> tuple[tuple[frozenset[str], Interval], ...]:
        """`window` 内每一段忙碌区间的只读快照，供上层按参与者筛选。"""
        with self._lock:
            return tuple(self._collect_locked(window))

    def is_free(self, interval: Interval) -> bool:
        """这段时间这间房完全没人占。"""
        with self._lock:
            return not self._collect_locked(interval)

    def reserve(self, meeting: Meeting) -> None:
        """把一次性会议钉进这间房：检查与写入在同一把锁里完成，不留"查完到写完"之间的缝——
        两个组织者同时抢同一间房的重叠时段，只可能有一个在这把锁里看到"空"。
        """
        with self._lock:
            if self._collect_locked(meeting.interval):
                raise RoomUnavailableError(f"room {self.room.id} is busy during {meeting.interval}")
            self._meetings[meeting.id] = meeting

    def cancel(self, meeting_id: str) -> bool:
        """取消一次性会议，把房间还回去。幂等：不存在就返回 `False`，不抛异常。"""
        with self._lock:
            return self._meetings.pop(meeting_id, None) is not None

    def add_series(self, series: RecurringSeries, horizon: Interval) -> None:
        """挂一条周期系列：只在 `horizon` 这段可核验的窗口内查冲突——规则本身可以不封顶，
        但没有任何算法能对"无穷"这件事下结论，核验必须划一条有限的边界。
        """
        with self._lock:
            existing = self._collect_locked(horizon)
            for occurrence in series.occurrences_in(horizon):
                if any(occurrence.overlaps(busy) for _, busy in existing):
                    raise RoomUnavailableError(
                        f"room {self.room.id} conflicts with the new series on {occurrence}")
            self._series[series.id] = series

    @property
    def meeting_count(self) -> int:
        """这间房眼下挂着几笔一次性会议。"""
        with self._lock:
            return len(self._meetings)

    @property
    def series_count(self) -> int:
        """这间房眼下挂着几条周期系列。"""
        with self._lock:
            return len(self._series)


# --------------------------------------------------------------------------
# MeetingSchedulerService：门面。房间目录、找空档配房、周期会议编辑，自己不存任何忙闲状态。

class MeetingSchedulerService:
    """会议室预订服务：注册房间、订一次性会议、给一组人找空档配房、管理周期会议。"""

    def __init__(self, default_horizon: timedelta = timedelta(days=90)) -> None:
        self._rooms: dict[str, Room] = {}
        self._calendars: dict[str, RoomCalendar] = {}
        self._meeting_room: dict[str, str] = {}  # 会议号 → 所在房间号，取消时不用扫全部房间
        self._series: dict[str, RecurringSeries] = {}
        self._default_horizon = default_horizon
        self._lock = threading.Lock()
        self._meeting_ids = (f"M{n}" for n in itertools.count(1))
        self._series_ids = (f"S{n}" for n in itertools.count(1))

    # ---- 房间目录 ----------------------------------------------------------

    def register_room(self, room: Room) -> None:
        """把一间会议室加进目录。"""
        with self._lock:
            self._rooms[room.id] = room
            self._calendars[room.id] = RoomCalendar(room)

    def room(self, room_id: str) -> Room:
        """按 id 取房间；不存在就抛 `RoomNotFoundError`。"""
        with self._lock:
            found = self._rooms.get(room_id)
        if found is None:
            raise RoomNotFoundError(f"unknown room {room_id!r}")
        return found

    @property
    def room_count(self) -> int:
        """目录里有几间房。"""
        with self._lock:
            return len(self._rooms)

    def _calendar(self, room_id: str) -> RoomCalendar:
        with self._lock:
            calendar = self._calendars.get(room_id)
        if calendar is None:
            raise RoomNotFoundError(f"unknown room {room_id!r}")
        return calendar

    def meeting_count(self, room_id: str) -> int:
        """这间房眼下挂着几笔一次性会议——验证取消真的把房间还回去了。"""
        return self._calendar(room_id).meeting_count

    def series_count(self, room_id: str) -> int:
        """这间房眼下挂着几条周期系列。"""
        return self._calendar(room_id).series_count

    def occupied_intervals(self, room_id: str, window: Interval) -> tuple[Interval, ...]:
        """这间房在 `window` 内每一段忙碌区间的只读快照，按开始时间排序。"""
        entries = self._calendar(room_id).busy_with(window)
        return tuple(sorted((iv for _, iv in entries), key=lambda iv: iv.start))

    # ---- 一次性会议 ---------------------------------------------------------

    def book_meeting(self, room_id: str, organizer: str, attendees: Sequence[str],
                     interval: Interval) -> Meeting:
        """订一间房、一个时间段。房间忙着就抛异常，不排队、不重试。"""
        calendar = self._calendar(room_id)
        with self._lock:
            meeting_id = next(self._meeting_ids)
        meeting = Meeting(meeting_id, room_id, interval, organizer, tuple(attendees))
        calendar.reserve(meeting)
        with self._lock:
            self._meeting_room[meeting_id] = room_id
        return meeting

    def cancel_meeting(self, meeting_id: str) -> None:
        """取消一次性会议，把房间还回去。"""
        with self._lock:
            room_id = self._meeting_room.pop(meeting_id, None)
        if room_id is None:
            raise MeetingNotFoundError(f"unknown meeting {meeting_id!r}")
        self._calendar(room_id).cancel(meeting_id)

    # ---- 找空档 + 配房 -------------------------------------------------------

    def _busy_for(self, attendees: Sequence[str], window: Interval) -> tuple[Interval, ...]:
        """把这组人各自的忙碌区间收集到一起——只要有一个人忙，这段时间对整组就是忙的。"""
        who = set(attendees)
        with self._lock:
            calendars = list(self._calendars.values())
        busy: list[Interval] = []
        for calendar in calendars:
            for participants, interval in calendar.busy_with(window):
                if who & participants:
                    busy.append(interval)
        return tuple(busy)

    def find_slot(self, attendees: Sequence[str], duration: timedelta, window: Interval,
                  equipment: frozenset[Equipment] = frozenset()) -> tuple[Interval, Room] | None:
        """给这组人找最早的、时长够、能配到房的空档；房间挑坐得下这组人的最小那间。

        `window` 里的每个空档来自区间合并算法：O(n log n) 排序 + O(n) 扫描（`merge_intervals`），
        n 是这组人全部忙碌区间之和。搜索结果不是强一致的承诺——真正的裁决发生在 `book_meeting`
        那一次原子的 `reserve` 里，这里给出的只是"建议"。
        """
        busy = self._busy_for(attendees, window)
        for gap in free_gaps(busy, window, duration):
            candidate = Interval(gap.start, gap.start + duration)
            room = self._smallest_fit(len(attendees), equipment, candidate)
            if room is not None:
                return candidate, room
        return None

    def _smallest_fit(self, attendee_count: int, equipment: frozenset[Equipment],
                      interval: Interval) -> Room | None:
        with self._lock:
            candidates = sorted(self._rooms.values(), key=lambda r: r.capacity)
        for room in candidates:
            if room.fits(attendee_count, equipment) and self._calendar(room.id).is_free(interval):
                return room
        return None

    # ---- 周期会议 ------------------------------------------------------------

    def schedule_series(self, room_id: str, organizer: str, attendees: Sequence[str],
                        local_start: time, duration: timedelta, zone: ZoneInfo,
                        rule: RecurrenceRule, series_start: date,
                        horizon: timedelta | None = None) -> RecurringSeries:
        """挂一条周期会议。只在 `horizon`（默认 90 天）内核验冲突——规则本身可以不封顶。"""
        calendar = self._calendar(room_id)
        with self._lock:
            series_id = next(self._series_ids)
        series = RecurringSeries(series_id, room_id, organizer, attendees, local_start, duration,
                                 zone, rule, series_start)
        span = horizon or self._default_horizon
        window_start = datetime.combine(series_start, time.min, tzinfo=zone)
        calendar.add_series(series, Interval(window_start, window_start + span))
        with self._lock:
            self._series[series_id] = series
        return series

    def series(self, series_id: str) -> RecurringSeries:
        """按 id 取周期系列；不存在就抛 `MeetingNotFoundError`。"""
        with self._lock:
            found = self._series.get(series_id)
        if found is None:
            raise MeetingNotFoundError(f"unknown series {series_id!r}")
        return found

    def split_series(self, series_id: str, from_day: date, local_start: time | None = None,
                     duration: timedelta | None = None, room_id: str | None = None) -> RecurringSeries:
        """"这一场及以后"的编辑：老规则在 `from_day` 前一天封顶，从 `from_day` 起开一条新系列
        接上，参与者不变，时间/时长/房间可以在新系列上改。
        """
        old = self.series(series_id)
        old.freeze_after(from_day)
        new_room = room_id or old.room_id
        calendar = self._calendar(new_room)
        with self._lock:
            new_id = next(self._series_ids)
        new_series = RecurringSeries(new_id, new_room, old.organizer, old.attendees,
                                     local_start or old.local_start, duration or old.duration,
                                     old.zone, replace(old.rule, until=None), from_day)
        window_start = datetime.combine(from_day, time.min, tzinfo=old.zone)
        calendar.add_series(new_series, Interval(window_start, window_start + self._default_horizon))
        with self._lock:
            self._series[new_id] = new_series
        return new_series


if __name__ == "__main__":
    ny = ZoneInfo("America/New_York")
    small = Room("R1", "壁橱间", capacity=4, equipment=frozenset({Equipment.VIDEO_CONF}))
    big = Room("R2", "大会议室", capacity=12,
              equipment=frozenset({Equipment.PROJECTOR, Equipment.VIDEO_CONF, Equipment.WHITEBOARD}))
    service = MeetingSchedulerService()
    service.register_room(small)
    service.register_room(big)

    # 一次性会议：占掉小会议室 09:00–10:00（本地时间，用 UTC 固定偏移简化演示）。
    utc = ZoneInfo("UTC")
    day = date(2026, 2, 2)
    busy = Interval(datetime(2026, 2, 2, 14, 0, tzinfo=utc), datetime(2026, 2, 2, 15, 0, tzinfo=utc))
    service.book_meeting("R1", organizer="alice", attendees=["bob"], interval=busy)

    window = Interval(datetime(2026, 2, 2, 13, 0, tzinfo=utc), datetime(2026, 2, 2, 18, 0, tzinfo=utc))
    slot = service.find_slot(["alice", "carol"], timedelta(hours=1), window)
    print(f"free slot for alice+carol: {slot[0].start:%H:%M}-{slot[0].end:%H:%M} in {slot[1].name}")

    # 周期会议：每周一 09:00（纽约时间）站会，横跨 2026-03-08 的夏令时切换。
    rule = RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series("R2", organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=ny, rule=rule, series_start=date(2026, 3, 2))
    before, after = series.occurrence_on(date(2026, 3, 2)), series.occurrence_on(date(2026, 3, 9))
    print(f"DST 前 UTC 偏移 {before.start.utcoffset()}，DST 后 UTC 偏移 {after.start.utcoffset()}，"
          f"本地钟点都还是 09:00")

    service.series(series.id).cancel_occurrence(date(2026, 3, 16))
    print(f"3/16 取消后还有场次：{series.occurrence_on(date(2026, 3, 16))}")

    split = service.split_series(series.id, date(2026, 3, 23), local_start=time(10, 0))
    print(f"3/23 起改到 10:00：老系列还剩 {series.rule.until}，新系列从 {split.series_start} 开始")
