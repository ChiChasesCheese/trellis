"""会议室预订参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。"""

import importlib
import os
import threading
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

UTC = ZoneInfo("UTC")
NY = ZoneInfo("America/New_York")
DAY = date(2026, 2, 2)  # 星期一


def at(hour: int, minute: int = 0, day: date = DAY, zone: ZoneInfo = UTC) -> datetime:
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=zone)


def iv(h1: int, h2: int, day: date = DAY) -> "impl.Interval":
    return impl.Interval(at(h1, 0, day), at(h2, 0, day))


def build():
    service = impl.MeetingSchedulerService()
    small = impl.Room("R1", "壁橱间", capacity=4, equipment=frozenset({impl.Equipment.VIDEO_CONF}))
    big = impl.Room("R2", "大会议室", capacity=12,
                    equipment=frozenset({impl.Equipment.PROJECTOR, impl.Equipment.VIDEO_CONF,
                                        impl.Equipment.WHITEBOARD}))
    service.register_room(small)
    service.register_room(big)
    return service, small, big


# ---- 第 1 关：房间、半开区间、订会议 -----------------------------------------


def test_half_open_intervals_are_adjacent_not_overlapping():
    morning = iv(10, 11)
    afternoon = iv(11, 12)
    overlapping = impl.Interval(at(10, 30), at(11, 30))
    assert not morning.overlaps(afternoon)  # 挨着但不重叠——退房/散场当刻不占用
    assert not afternoon.overlaps(morning)
    assert morning.overlaps(overlapping)
    assert overlapping.overlaps(morning)


def test_interval_rejects_end_not_after_start():
    with pytest.raises(impl.InvalidIntervalError):
        impl.Interval(at(11, 0), at(10, 0))
    with pytest.raises(impl.InvalidIntervalError):
        impl.Interval(at(10, 0), at(10, 0))


def test_room_fits_checks_capacity_and_equipment():
    small = impl.Room("R1", "壁橱间", capacity=4, equipment=frozenset({impl.Equipment.VIDEO_CONF}))
    assert small.fits(4, frozenset({impl.Equipment.VIDEO_CONF}))
    assert not small.fits(5, frozenset())  # 人数超了
    assert not small.fits(2, frozenset({impl.Equipment.PROJECTOR}))  # 没有投影仪


def test_book_meeting_succeeds_and_room_becomes_busy():
    service, small, _ = build()
    meeting = service.book_meeting(small.id, organizer="alice", attendees=["bob"], interval=iv(9, 10))
    assert service.meeting_count(small.id) == 1
    assert service.occupied_intervals(small.id, iv(0, 23)) == (iv(9, 10),)
    assert meeting.organizer == "alice"


def test_book_meeting_rejects_overlap_but_allows_back_to_back():
    service, small, _ = build()
    service.book_meeting(small.id, organizer="alice", attendees=[], interval=iv(10, 11))
    # 挨着的下一段完全没问题——半开区间的直接好处。
    service.book_meeting(small.id, organizer="bob", attendees=[], interval=iv(11, 12))
    with pytest.raises(impl.RoomUnavailableError):
        service.book_meeting(small.id, organizer="carol", attendees=[],
                             interval=impl.Interval(at(10, 30), at(11, 30)))
    assert service.meeting_count(small.id) == 2


def test_cancel_meeting_frees_the_room():
    service, small, _ = build()
    meeting = service.book_meeting(small.id, organizer="alice", attendees=[], interval=iv(9, 10))
    service.cancel_meeting(meeting.id)
    assert service.meeting_count(small.id) == 0
    # 取消之后这段时间应该能重新订出去。
    service.book_meeting(small.id, organizer="bob", attendees=[], interval=iv(9, 10))
    with pytest.raises(impl.MeetingNotFoundError):
        service.cancel_meeting(meeting.id)  # 幂等边界：同一张会议号不能再取消一次


# ---- 第 2 关：区间合并、找空档、配最小的房 ------------------------------------


def test_merge_intervals_combines_overlapping_and_adjacent():
    # 9-10 和 10-11 挨着（半开区间下端点相等也算挨上），必须合并成 9-11；
    # 9:30-10:30 和 9-10 真正重叠，也合并；11:30-12 和前面隔着半小时的缝，独立成段。
    merged = impl.merge_intervals([iv(9, 10), iv(10, 11), impl.Interval(at(9, 30), at(10, 30)),
                                   impl.Interval(at(11, 30), at(12, 0)), iv(14, 15)])
    assert merged == (iv(9, 11), impl.Interval(at(11, 30), at(12, 0)), iv(14, 15))


def test_free_gaps_finds_slots_around_busy_intervals():
    window = iv(9, 17)
    gaps = impl.free_gaps([iv(10, 11), iv(13, 14)], window, timedelta(hours=1))
    assert gaps == (iv(9, 10), iv(11, 13), iv(14, 17))
    # 半小时的缝比要求的时长短，找 1.5 小时的会议时应该被跳过。
    tight_gaps = impl.free_gaps([iv(9, 10), impl.Interval(at(10, 30), at(17, 0))], window, timedelta(hours=1))
    assert tight_gaps == ()


def test_find_slot_intersects_every_attendees_busy_interval():
    service, small, big = build()
    service.book_meeting(small.id, organizer="alice", attendees=[], interval=iv(9, 10))
    service.book_meeting(big.id, organizer="carol", attendees=[], interval=iv(10, 11))
    window = iv(9, 12)
    slot = service.find_slot(["alice", "carol"], timedelta(hours=1), window)
    assert slot is not None
    candidate, room = slot
    # 两人各自忙的时段合并起来是 9-11，第一个够长的空档只能是 11-12。
    assert candidate == iv(11, 12)


def test_find_slot_picks_the_smallest_room_that_fits():
    service, small, big = build()
    slot = service.find_slot(["alice", "bob"], timedelta(hours=1), iv(9, 12))
    assert slot is not None
    _, room = slot
    assert room.id == small.id  # 两间房都空着，选坐得下这组人的最小那间
    service.book_meeting(small.id, organizer="dan", attendees=[], interval=iv(9, 12))
    slot2 = service.find_slot(["alice", "bob"], timedelta(hours=1), iv(9, 12))
    assert slot2[1].id == big.id  # 小房被占了，退而求其次选大房


def test_find_slot_returns_none_when_no_window_is_wide_enough():
    service, small, big = build()
    service.book_meeting(small.id, organizer="a", attendees=[], interval=iv(9, 17))
    service.book_meeting(big.id, organizer="b", attendees=[], interval=iv(9, 17))
    assert service.find_slot(["a"], timedelta(hours=1), iv(9, 17)) is None


# ---- 第 3 关：周期会议、按天例外、"这一场"与"这一场及以后" -----------------------


def test_recurring_series_expands_lazily_for_a_far_future_window():
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))  # 每周一，不封顶
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    far_window = impl.Interval(datetime(2030, 6, 1, tzinfo=UTC), datetime(2030, 6, 15, tzinfo=UTC))
    occurrences = series.occurrences_in(far_window)
    assert len(occurrences) == 2  # 那两周里恰好两个周一，规则从没被整段物化过
    assert all(o.start.astimezone(NY).weekday() == 0 for o in occurrences)


def test_cancel_this_occurrence_only_affects_that_day():
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    series.cancel_occurrence(date(2026, 3, 9))
    assert series.occurrence_on(date(2026, 3, 9)) is None
    assert series.occurrence_on(date(2026, 3, 2)) is not None
    assert series.occurrence_on(date(2026, 3, 16)) is not None
    assert series.exception_count == 1


def test_reschedule_this_occurrence_only_affects_that_day():
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    series.reschedule_occurrence(date(2026, 3, 9), local_start=time(14, 0))
    moved = series.occurrence_on(date(2026, 3, 9))
    assert moved.start.astimezone(NY).time() == time(14, 0)
    unaffected = series.occurrence_on(date(2026, 3, 16))
    assert unaffected.start.astimezone(NY).time() == time(9, 0)


def test_split_series_freezes_old_and_starts_a_new_one():
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    new_series = service.split_series(series.id, date(2026, 3, 23), local_start=time(10, 0))
    assert series.rule.until == date(2026, 3, 22)  # 老系列在切分点前一天封顶
    # `occurrence_on` 只管"这一天长什么样"，真正按规则筛出哪些日期存在要看 `occurrences_in`：
    # 老系列在切分点之后，规则展开出的日期列表里已经没有它了。
    horizon = impl.Interval(datetime(2026, 3, 20, tzinfo=NY), datetime(2026, 3, 30, tzinfo=NY))
    old_dates = [o.start.astimezone(NY).date() for o in series.occurrences_in(horizon)]
    assert date(2026, 3, 23) not in old_dates
    assert new_series.occurrence_on(date(2026, 3, 23)).start.astimezone(NY).time() == time(10, 0)
    assert new_series.room_id == big.id
    assert new_series.attendees == series.attendees  # 参与者原样带过去


def test_split_series_prunes_exceptions_on_or_after_the_cutoff():
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    series.cancel_occurrence(date(2026, 3, 9))    # 切分点之前，应该保留
    series.cancel_occurrence(date(2026, 3, 23))   # 切分点当天，应该被清掉（再也查不到）
    service.split_series(series.id, date(2026, 3, 23))
    assert series.exception_count == 1  # 2026-03-23 那条例外泄漏进了一张再也查不到的表会被发现


def test_add_series_rejects_conflict_with_an_existing_meeting_in_the_horizon():
    service, _, big = build()
    # 未来某个星期一 09:15，和站会规则打算占的 09:00-09:30 撞在一起。
    service.book_meeting(big.id, organizer="frank", attendees=[],
                         interval=impl.Interval(datetime(2026, 3, 9, 9, 15, tzinfo=NY),
                                                datetime(2026, 3, 9, 9, 45, tzinfo=NY)))
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    with pytest.raises(impl.RoomUnavailableError):
        service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                local_start=time(9, 0), duration=timedelta(minutes=30),
                                zone=NY, rule=rule, series_start=date(2026, 3, 2))


# ---- 第 4 关：时区与夏令时、取消后放开房间 -----------------------------------


def test_recurring_meeting_keeps_local_wall_clock_across_dst():
    # 美国 2026 年的夏令时切换是 3 月 8 日；3 月 2 日和 3 月 9 日都是周一站会。
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    before = series.occurrence_on(date(2026, 3, 2))
    after = series.occurrence_on(date(2026, 3, 9))
    # 本地墙钟时间都还是 09:00——这才是旅客/员工真正在乎的事实。
    assert before.start.astimezone(NY).time() == time(9, 0)
    assert after.start.astimezone(NY).time() == time(9, 0)
    # 但换算成 UTC 的具体时刻，两者的偏移量不同——跨过了那次夏令时切换。
    assert before.start.utcoffset() != after.start.utcoffset()


def test_a_fixed_utc_instant_would_have_drifted_the_local_hour():
    # 反证：如果把第一场先冻结成一个固定的 UTC 时刻，再原样加 7 天（而不是每次都重新按
    # 本地时区换算），跨过夏令时切换之后换回本地时间，钟点会从 09:00 漂移成 10:00——
    # 这正是本设计坚持存"本地时间 + 时区"而不是存单一 UTC 时刻的原因。
    first_as_a_frozen_utc_instant = datetime(2026, 3, 2, 9, 0, tzinfo=NY).astimezone(UTC)
    naive_next = first_as_a_frozen_utc_instant + timedelta(days=7)
    assert naive_next.astimezone(NY).time() != time(9, 0)
    assert naive_next.astimezone(NY).time() == time(10, 0)


def test_cancelling_an_occurrence_frees_the_room_for_a_one_off_meeting():
    service, _, big = build()
    rule = impl.RecurrenceRule(weekdays=frozenset({0}))
    series = service.schedule_series(big.id, organizer="dan", attendees=["erin"],
                                     local_start=time(9, 0), duration=timedelta(minutes=30),
                                     zone=NY, rule=rule, series_start=date(2026, 3, 2))
    same_slot = impl.Interval(datetime(2026, 3, 9, 9, 0, tzinfo=NY), datetime(2026, 3, 9, 9, 30, tzinfo=NY))
    with pytest.raises(impl.RoomUnavailableError):
        service.book_meeting(big.id, organizer="gwen", attendees=[], interval=same_slot)
    series.cancel_occurrence(date(2026, 3, 9))
    service.book_meeting(big.id, organizer="gwen", attendees=[], interval=same_slot)  # 现在能订了
    assert service.meeting_count(big.id) == 1


# ---- 并发：两个组织者抢同一间房的重叠时段 -------------------------------------


def test_concurrent_overlapping_bookings_only_one_wins():
    service, _, big = build()
    n_threads = 10
    barrier = threading.Barrier(n_threads)
    results = [False] * n_threads

    def worker(i: int) -> None:
        barrier.wait()
        try:
            service.book_meeting(big.id, organizer=f"organizer{i}", attendees=[], interval=iv(9, 10))
            results[i] = True
        except impl.RoomUnavailableError:
            results[i] = False

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sum(results) == 1  # 十个组织者抢同一间房的同一个小时，只可能有一个订上
    assert service.meeting_count(big.id) == 1
