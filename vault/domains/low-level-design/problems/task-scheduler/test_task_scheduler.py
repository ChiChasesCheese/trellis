"""任务调度器的测试。分两类：绝大多数用 `run_pending` + 注入的假时钟，完全不涉及真实线程或
真实 sleep；少数标了"并发"的用例才启动 `Scheduler.start()`，用真实线程和 `threading.Barrier`
/`threading.Event` 断言并发与关闭语义——从不用 `time.sleep` 加断言去赌一个时间点。
"""

import importlib
import os
import threading
from datetime import UTC, datetime, timedelta

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))

T0 = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def make_clock(start: datetime = T0):
    box = [start]

    def clock() -> datetime:
        return box[0]

    def advance(delta: timedelta) -> datetime:
        box[0] += delta
        return box[0]

    return clock, advance


# --------------------------------------------------------------------------
# 第 1 关：一次性任务、延时/定点调度、取消、"不早于"。


def test_schedule_after_runs_at_due_time_not_before() -> None:
    clock, advance = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    ran = []
    scheduler.schedule_after(lambda: ran.append("x"), timedelta(seconds=10))

    advance(timedelta(seconds=9))
    assert scheduler.run_pending(clock()) == ()
    assert ran == []

    advance(timedelta(seconds=1))  # 现在恰好到期
    executed = scheduler.run_pending(clock())
    assert len(executed) == 1
    assert ran == ["x"]


def test_one_shot_task_does_not_run_twice_and_pending_count_drops() -> None:
    clock, advance = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    scheduler.schedule_after(lambda: None, timedelta(seconds=5))
    assert scheduler.pending_count == 1

    advance(timedelta(seconds=5))
    assert len(scheduler.run_pending(clock())) == 1
    assert scheduler.pending_count == 0

    advance(timedelta(seconds=100))
    assert scheduler.run_pending(clock()) == ()  # 早就跑完了，不会重跑


def test_schedule_at_specific_datetime() -> None:
    clock, advance = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    target = T0 + timedelta(minutes=3)
    ran = []
    scheduler.schedule_at(lambda: ran.append(1), target)

    advance(timedelta(minutes=3))
    scheduler.run_pending(clock())
    assert ran == [1]


def test_negative_delay_and_nonpositive_period_are_rejected() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    with pytest.raises(impl.InvalidScheduleError):
        scheduler.schedule_after(lambda: None, timedelta(seconds=-1))
    with pytest.raises(impl.InvalidScheduleError):
        scheduler.schedule_periodic(lambda: None, timedelta(0))
    with pytest.raises(impl.InvalidScheduleError):
        scheduler.schedule_periodic(lambda: None, timedelta(seconds=-5))


def test_cancel_before_due_prevents_the_run() -> None:
    clock, advance = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    ran = []
    task_id = scheduler.schedule_after(lambda: ran.append(1), timedelta(seconds=5))

    assert scheduler.cancel(task_id) is True
    assert scheduler.pending_count == 0

    advance(timedelta(seconds=5))
    assert scheduler.run_pending(clock()) == ()
    assert ran == []


def test_cancel_is_false_for_unknown_or_already_cancelled_task() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    assert scheduler.cancel(999) is False

    task_id = scheduler.schedule_after(lambda: None, timedelta(seconds=1))
    assert scheduler.cancel(task_id) is True
    assert scheduler.cancel(task_id) is False  # 第二次取消同一个 id 是安全的，但没有效果


def test_scheduling_after_shutdown_raises() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    scheduler.shutdown()
    with pytest.raises(impl.SchedulerClosedError):
        scheduler.schedule_after(lambda: None, timedelta(seconds=1))
    with pytest.raises(impl.SchedulerClosedError):
        scheduler.schedule_periodic(lambda: None, timedelta(seconds=1))


# --------------------------------------------------------------------------
# 第 2 关：固定速率 vs 固定延迟、优先级、堆的收缩。


def test_fixed_rate_catches_up_when_a_run_falls_behind() -> None:
    """固定速率的下一次到期在**取出时**就按 `due + period` 算好，与实际跑多久无关。
    一次性跳过一个多周期之后才第一次去看它，会在同一次 `run_pending` 调用里连续追赶。
    """
    clock, advance = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    count = []
    scheduler.schedule_periodic(lambda: count.append(1), timedelta(seconds=10),
                                mode=impl.RepeatMode.FIXED_RATE, first_due=T0)

    advance(timedelta(seconds=15))  # 进程忙到现在才回头看，due=T0 和 due=T0+10 都已经过期
    executed = scheduler.run_pending(clock())
    assert len(executed) == 2          # 追赶：两个到期时刻在同一次调用里连续被派发
    assert count == [1, 1]


def test_fixed_delay_never_catches_up() -> None:
    """固定延迟的下一次到期只在**完成之后**用完成时刻算，所以落后多少都只跑一次，
    并把整条未来时间线推后，而不是连续追赶。
    """
    clock, advance = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    count = []
    scheduler.schedule_periodic(lambda: count.append(1), timedelta(seconds=10),
                                mode=impl.RepeatMode.FIXED_DELAY, first_due=T0)

    advance(timedelta(seconds=25))
    executed = scheduler.run_pending(clock())
    assert len(executed) == 1
    assert count == [1]

    # 下一次到期 = 这次完成时刻（t=25）+ 10 = t=35，而不是 t=20；再跳到 t=35 才会再跑一次。
    advance(timedelta(seconds=9))
    assert scheduler.run_pending(clock()) == ()
    advance(timedelta(seconds=1))
    assert len(scheduler.run_pending(clock())) == 1
    assert count == [1, 1]


def test_priority_breaks_ties_among_tasks_due_at_the_same_instant() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    order = []
    scheduler.schedule_at(lambda: order.append("low"), T0, priority=5)
    scheduler.schedule_at(lambda: order.append("high"), T0, priority=1)
    scheduler.schedule_at(lambda: order.append("mid"), T0, priority=3)

    scheduler.run_pending(T0)
    assert order == ["high", "mid", "low"]  # 数字越小越先跑


def test_arrival_order_breaks_ties_when_priority_is_equal() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    order = []
    scheduler.schedule_at(lambda: order.append("a"), T0)
    scheduler.schedule_at(lambda: order.append("b"), T0)
    scheduler.schedule_at(lambda: order.append("c"), T0)

    scheduler.run_pending(T0)
    assert order == ["a", "b", "c"]


def test_explicit_compact_shrinks_heap_to_exactly_the_live_tasks() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    ids = [scheduler.schedule_at(lambda: None, T0 + timedelta(hours=i)) for i in range(2000)]
    for task_id in ids[:1990]:
        scheduler.cancel(task_id)

    assert scheduler.pending_count == 10
    scheduler.compact()
    assert scheduler.heap_size == 10  # 压缩之后，堆里不多不少正好是还活着的任务


def test_heap_does_not_grow_unbounded_even_without_calling_compact() -> None:
    """不手动调用 `compact`，光是取消操作本身触发的自动整理也必须生效——
    否则"取消一百万个一次性任务"会让堆一直攒着一百万个永远用不上的墓碑。
    """
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    ids = [scheduler.schedule_at(lambda: None, T0 + timedelta(hours=i)) for i in range(3000)]
    for task_id in ids[:2990]:
        scheduler.cancel(task_id)

    assert scheduler.pending_count == 10
    assert scheduler.heap_size < 3000       # 自动整理必须发生过至少一次
    assert scheduler.heap_size < 500         # 而且不是"刚好没触发阈值"那种侥幸


# --------------------------------------------------------------------------
# 第 3 关：异常不杀死循环或未来的调度、真实线程池的并发、drain vs abandon。


def test_a_raising_task_does_not_kill_future_runs_or_the_loop() -> None:
    clock, advance = make_clock()
    errors = []
    scheduler = impl.Scheduler(clock=clock, on_error=lambda task_id, exc: errors.append((task_id, exc)))
    count = []

    def flaky() -> None:
        count.append(1)
        if len(count) == 1:
            raise ValueError("boom")

    task_id = scheduler.schedule_periodic(flaky, timedelta(seconds=10),
                                          mode=impl.RepeatMode.FIXED_DELAY, first_due=T0)
    executed = scheduler.run_pending(T0)
    assert executed == (task_id,)          # run_pending 自己没有被异常打断
    assert len(errors) == 1 and isinstance(errors[0][1], ValueError)

    advance(timedelta(seconds=10))          # 固定延迟：完成时刻(t=0)+10，仍然会被调度
    assert scheduler.run_pending(clock()) == (task_id,)
    assert count == [1, 1]                  # 第二次正常跑完，没有再抛


def test_worker_pool_executes_due_tasks_concurrently() -> None:
    n = 4
    barrier = threading.Barrier(n + 1)
    scheduler = impl.Scheduler(clock=datetime.now, workers=n)
    for _ in range(n):
        scheduler.schedule_at(lambda: barrier.wait(timeout=5), datetime.now())

    scheduler.start()
    try:
        barrier.wait(timeout=5)  # 只有 n 个工作线程都同时到达了，这一句才不会超时
    finally:
        scheduler.shutdown(drain=True)


def test_shutdown_drains_a_running_task_by_default() -> None:
    started = threading.Event()
    finished = threading.Event()

    def slow() -> None:
        started.set()
        finished.set()

    scheduler = impl.Scheduler(clock=datetime.now, workers=1)
    scheduler.schedule_at(slow, datetime.now())
    scheduler.start()

    assert started.wait(timeout=5)
    scheduler.shutdown(drain=True)   # 默认 drain：返回时，已经派发的任务必须已经跑完
    assert finished.is_set()


def test_shutdown_abandons_not_yet_started_tasks_when_not_draining() -> None:
    release = threading.Event()
    blocker_started = threading.Event()
    late_ran = threading.Event()

    def blocker() -> None:
        blocker_started.set()
        release.wait(timeout=5)

    scheduler = impl.Scheduler(clock=datetime.now, workers=1)  # 只有一个工作线程
    scheduler.schedule_at(blocker, datetime.now())
    scheduler.schedule_at(lambda: late_ran.set(), datetime.now())  # 会排在线程池队列里
    scheduler.start()

    assert blocker_started.wait(timeout=5)
    scheduler.shutdown(drain=False)   # 不等待：排队中的第二个任务被直接丢弃
    release.set()                     # 放行卡住的第一个任务，避免线程泄漏
    assert not late_ran.wait(timeout=0.5)


# --------------------------------------------------------------------------
# 第 4 关（选做，见文章）：一口价式的扩展点在优先级测试里已经证明——加它没有改堆。


def test_run_pending_reports_the_ids_it_actually_executed() -> None:
    clock, _ = make_clock()
    scheduler = impl.Scheduler(clock=clock)
    a = scheduler.schedule_at(lambda: None, T0)
    b = scheduler.schedule_at(lambda: None, T0 + timedelta(seconds=100))

    executed = scheduler.run_pending(T0)
    assert executed == (a,)
    assert b not in executed
