"""熔断器的测试：`-k part1` 选第 1 关，依此类推。时间用假时钟，线程用事件排顺序，不靠 sleep 估时间。"""

import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
State = impl.State

T = 5.0


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class Down(Exception):
    pass


def boom():
    raise Down("down")


def good():
    return "ok"


def make(clock=None, **kw):
    clock = clock or Clock()
    return impl.CircuitBreaker(clock=clock, **kw), clock


def fail(cb, n=1):
    for _ in range(n):
        with pytest.raises(Down):
            cb.call(boom)


def blocked_call(cb, gate, entered, result="ok", exc=None):
    """在线程里发起一次会阻塞到 gate 打开的调用；返回 (线程, 结果字典)。"""
    box = {}

    def fn():
        entered.set()
        assert gate.wait(T), "测试里的闸门没有被打开"
        if exc:
            raise exc
        return result

    def run():
        try:
            box["value"] = cb.call(fn)
        except BaseException as e:  # noqa: BLE001
            box["error"] = e

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return t, box


# ---- 第 1 关：三状态、阈值、冷却、降级、指标 -----------------------------------


def test_part1_closed_passes_results_and_counts_successes():
    cb, _ = make()
    assert cb.state is State.CLOSED
    assert cb.call(good) == "ok"
    assert cb.call(lambda: 42) == 42
    assert cb.metrics == impl.Metrics(success=2, failure=0, rejected=0)


def test_part1_consecutive_failures_trip_the_breaker_and_original_errors_propagate():
    cb, _ = make(failure_threshold=3)
    fail(cb, 2)
    assert cb.state is State.CLOSED
    fail(cb, 1)
    assert cb.state is State.OPEN
    assert cb.metrics.failure == 3


def test_part1_a_success_resets_the_consecutive_count():
    cb, _ = make(failure_threshold=3)
    fail(cb, 2)
    cb.call(good)
    fail(cb, 2)
    assert cb.state is State.CLOSED
    fail(cb, 1)
    assert cb.state is State.OPEN


def test_part1_open_rejects_without_calling_downstream():
    cb, _ = make(failure_threshold=1, open_timeout=10)
    fail(cb)
    calls = []
    for _ in range(3):
        with pytest.raises(impl.CircuitOpenError):
            cb.call(lambda: calls.append(1))
    assert calls == []
    assert cb.metrics == impl.Metrics(success=0, failure=1, rejected=3)


def test_part1_fallback_covers_rejection_and_failure_but_not_success():
    cb, _ = make(failure_threshold=2, open_timeout=10)
    assert cb.call(good, fallback=lambda: "cached") == "ok"
    assert cb.call(boom, fallback=lambda: "cached") == "cached"       # 失败：降级，计一次失败
    assert cb.call(boom, fallback=lambda: "cached") == "cached"
    assert cb.state is State.OPEN
    ran = []
    assert cb.call(lambda: ran.append(1), fallback=lambda: "cached") == "cached"   # 拒绝：降级，不碰下游
    assert ran == [] and cb.metrics == impl.Metrics(success=1, failure=2, rejected=1)


def test_part1_cooldown_boundary_then_probe_success_closes():
    cb, clock = make(failure_threshold=1, open_timeout=10)
    fail(cb)
    clock.advance(9.99)
    with pytest.raises(impl.CircuitOpenError):
        cb.call(good)
    clock.advance(0.01)                                               # 正好 10 秒：放行一个探测
    assert cb.call(good) == "ok"
    assert cb.state is State.CLOSED
    assert cb.call(good) == "ok"


def test_part1_failed_probe_reopens_with_a_fresh_timer():
    cb, clock = make(failure_threshold=1, open_timeout=10)
    fail(cb)
    clock.advance(10)
    fail(cb)                                                          # 探测失败
    assert cb.state is State.OPEN
    clock.advance(9)
    with pytest.raises(impl.CircuitOpenError):                        # 要从探测失败那一刻重新数满 10 秒
        cb.call(good)
    clock.advance(1)
    assert cb.call(good) == "ok" and cb.state is State.CLOSED


def test_part1_state_does_not_change_by_itself_over_time():
    cb, clock = make(failure_threshold=1, open_timeout=10)
    fail(cb)
    clock.advance(1000)
    assert cb.state is State.OPEN                                     # 没有调用就没有转换
    cb.call(good)
    assert cb.state is State.CLOSED


def test_part1_after_recovery_failures_count_from_zero():
    cb, clock = make(failure_threshold=2, open_timeout=1)
    fail(cb, 2)
    clock.advance(1)
    cb.call(good)
    fail(cb, 1)
    assert cb.state is State.CLOSED
    fail(cb, 1)
    assert cb.state is State.OPEN


def test_part1_metrics_is_an_immutable_snapshot():
    cb, _ = make()
    cb.call(good)
    snap = cb.metrics
    cb.call(good)
    assert snap.success == 1 and cb.metrics.success == 2
    with pytest.raises(AttributeError):
        snap.success = 99


@pytest.mark.parametrize("kw", [dict(failure_threshold=0), dict(open_timeout=-1)])
def test_part1_invalid_configuration_is_rejected(kw):
    with pytest.raises(ValueError):
        impl.CircuitBreaker(**kw)


def test_part1_keyboard_interrupt_is_not_a_downstream_failure():
    cb, _ = make(failure_threshold=1)

    def interrupted():
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        cb.call(interrupted)
    assert cb.state is State.CLOSED and cb.metrics == impl.Metrics(0, 0, 0)


# ---- 第 2 关：半开期名额、迟到的旧结果、不持锁调用 ------------------------------


def half_open(cb, clock, timeout=10):
    """failure_threshold=1 的熔断器：失败一次打开，再等冷却结束，下一次调用就是探测。"""
    fail(cb)
    clock.advance(timeout)


def test_part2_half_open_admits_only_the_configured_number_of_probes():
    cb, clock = make(failure_threshold=1, open_timeout=10, half_open_max_calls=2)
    half_open(cb, clock)
    gate, e1, e2 = threading.Event(), threading.Event(), threading.Event()
    t1, _ = blocked_call(cb, gate, e1)
    assert e1.wait(T)
    t2, _ = blocked_call(cb, gate, e2)
    assert e2.wait(T)
    assert cb.state is State.HALF_OPEN
    with pytest.raises(impl.CircuitOpenError):                        # 第三个：名额已满
        cb.call(good)
    gate.set()
    t1.join(T), t2.join(T)
    assert cb.state is State.CLOSED


@pytest.mark.parametrize("kw", [dict(half_open_max_calls=0), dict(success_threshold=0)])
def test_part2_invalid_half_open_configuration_is_rejected(kw):
    with pytest.raises(ValueError):
        impl.CircuitBreaker(**kw)


def test_part2_single_probe_slot_rejects_concurrent_callers():
    cb, clock = make(failure_threshold=1, open_timeout=10)
    half_open(cb, clock)
    gate, entered = threading.Event(), threading.Event()
    t, box = blocked_call(cb, gate, entered)
    assert entered.wait(T)
    with pytest.raises(impl.CircuitOpenError):
        cb.call(good)
    assert cb.metrics.rejected == 1
    gate.set()
    t.join(T)
    assert box["value"] == "ok" and cb.state is State.CLOSED
    assert cb.call(good) == "ok"


def test_part2_success_threshold_needs_several_good_probes():
    cb, clock = make(failure_threshold=1, open_timeout=10, success_threshold=3)
    half_open(cb, clock)
    cb.call(good)
    cb.call(good)
    assert cb.state is State.HALF_OPEN
    cb.call(good)
    assert cb.state is State.CLOSED


def test_part2_any_probe_failure_reopens_even_after_earlier_probe_successes():
    cb, clock = make(failure_threshold=1, open_timeout=10, success_threshold=3)
    half_open(cb, clock)
    cb.call(good)
    fail(cb)
    assert cb.state is State.OPEN
    with pytest.raises(impl.CircuitOpenError):
        cb.call(good)
    clock.advance(10)
    cb.call(good)
    cb.call(good)
    assert cb.state is State.HALF_OPEN                                # 成功计数从头开始，不继承上一轮的
    cb.call(good)
    assert cb.state is State.CLOSED


def test_part2_a_late_result_from_an_older_state_does_not_change_the_new_one():
    cb, clock = make(failure_threshold=1, open_timeout=10)
    gate, entered = threading.Event(), threading.Event()
    slow, box = blocked_call(cb, gate, entered, exc=Down("late"))     # 关闭状态时发出的慢请求
    assert entered.wait(T)
    fail(cb)                                                          # 另一个请求让熔断器打开
    clock.advance(10)
    assert cb.call(good) == "ok" and cb.state is State.CLOSED         # 探测成功，回到关闭
    gate.set()
    slow.join(T)                                                      # 慢请求现在才失败
    assert isinstance(box["error"], Down)
    assert cb.state is State.CLOSED                                   # 不能把旧失败当成新一轮的失败
    assert cb.metrics.failure == 2                                    # 但指标照实计数


def test_part2_a_late_probe_result_after_reopening_is_ignored():
    cb, clock = make(failure_threshold=1, open_timeout=10, half_open_max_calls=2)
    half_open(cb, clock)
    gate_a, gate_b, ea, eb = (threading.Event() for _ in range(4))
    ta, a = blocked_call(cb, gate_a, ea, exc=Down("a"))
    assert ea.wait(T)
    tb, b = blocked_call(cb, gate_b, eb)
    assert eb.wait(T)
    gate_a.set()
    ta.join(T)
    assert cb.state is State.OPEN                                     # 探测 A 失败，重新打开
    gate_b.set()
    tb.join(T)                                                        # 探测 B 此时才成功
    assert b["value"] == "ok" and cb.state is State.OPEN              # 属于上一轮，不能让它关闭熔断器


def test_part2_the_downstream_call_runs_outside_the_lock():
    cb, _ = make(failure_threshold=100)
    gate, entered = threading.Event(), threading.Event()
    t, _ = blocked_call(cb, gate, entered)
    assert entered.wait(T)
    box = {}
    th = threading.Thread(target=lambda: box.update(v=(cb.call(good), cb.state, cb.metrics)), daemon=True)
    th.start()
    th.join(T)
    assert not th.is_alive() and box["v"][0] == "ok"                  # 第一个调用还卡在下游时，别人照常通行
    gate.set()
    t.join(T)


def test_part2_concurrent_calls_keep_exact_counts():
    cb, _ = make(failure_threshold=10 ** 6)
    n_threads, per = 8, 25
    barrier = threading.Barrier(n_threads)

    def worker(i):
        barrier.wait(T)
        for j in range(per):
            try:
                cb.call(good if (i + j) % 2 else boom)
            except Down:
                pass

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    m = cb.metrics
    assert m.success + m.failure == n_threads * per == 200 and m.success == m.failure == 100 and m.rejected == 0


def test_part2_concurrent_rejections_are_counted_exactly():
    cb, _ = make(failure_threshold=1, open_timeout=10 ** 6)
    fail(cb)
    n_threads, per = 8, 25
    barrier = threading.Barrier(n_threads)

    def worker():
        barrier.wait(T)
        for _ in range(per):
            with pytest.raises(impl.CircuitOpenError):
                cb.call(good)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    [t.start() for t in threads]
    [t.join(T) for t in threads]
    assert cb.metrics.rejected == 200


# ---- 第 3 关：失败判定、滑动窗口、慢调用 ---------------------------------------


class ClientError(Exception):
    """下游的 4xx：说明下游是健康的。"""


def test_part3_is_failure_lets_client_errors_through_without_tripping():
    cb, _ = make(failure_threshold=1, is_failure=lambda e: not isinstance(e, ClientError))

    def bad_request():
        raise ClientError("400")

    for _ in range(3):
        with pytest.raises(ClientError):
            cb.call(bad_request, fallback=lambda: "cached")          # 不算失败的异常：原样抛出，降级不掩盖它
    assert cb.state is State.CLOSED
    assert cb.metrics == impl.Metrics(success=3, failure=0, rejected=0)
    fail(cb)                                                          # 真正的失败仍然会熔断
    assert cb.state is State.OPEN


def test_part3_failure_rate_window_trips_on_interleaved_failures():
    cb, _ = make(failure_threshold=2, window_size=10, min_calls=4, failure_rate=0.5)
    for step in (good, boom, good, boom):                             # 连续失败数永远到不了 2，但失败率是 50%
        try:
            cb.call(step)
        except Down:
            pass
    assert cb.state is State.OPEN


def test_part3_window_waits_for_min_calls():
    cb, _ = make(window_size=10, min_calls=4, failure_rate=0.5)
    fail(cb, 3)
    assert cb.state is State.CLOSED                                   # 3 次全是失败，但样本还不够
    fail(cb, 1)
    assert cb.state is State.OPEN


def test_part3_window_forgets_old_results():
    cb, _ = make(window_size=4, min_calls=4, failure_rate=0.75)
    for step in (boom, good, good, good, boom, boom):
        try:
            cb.call(step)
        except Down:
            pass
    assert cb.state is State.CLOSED                                   # 窗口 [good, good, boom, boom]：50%
    fail(cb)
    assert cb.state is State.OPEN                                     # 窗口 [good, boom, boom, boom]：75%


def test_part3_window_is_cleared_when_the_state_changes():
    cb, clock = make(open_timeout=1, window_size=4, min_calls=4, failure_rate=0.5)
    fail(cb, 4)
    clock.advance(1)
    cb.call(good)
    fail(cb, 3)
    assert cb.state is State.CLOSED                                   # 旧的失败不跟着带过来：窗口里只有 4 个新样本中的 3 个
    fail(cb, 1)
    assert cb.state is State.OPEN


def test_part3_slow_calls_count_as_failures_but_still_return_their_result():
    cb, clock = make(failure_threshold=2, slow_call_threshold=1.0)

    def slow():
        clock.advance(1.0)
        return "late"

    def quick():
        clock.advance(0.5)
        return "fine"

    assert cb.call(quick) == "fine" and cb.metrics.failure == 0
    assert cb.call(slow) == "late"                                    # 恰好达到阈值就算慢
    assert cb.call(slow) == "late"
    assert cb.state is State.OPEN and cb.metrics.failure == 2


@pytest.mark.parametrize("kw", [dict(window_size=5, min_calls=6), dict(window_size=5, min_calls=0),
                                dict(failure_rate=0), dict(failure_rate=1.5)])
def test_part3_invalid_window_configuration_is_rejected(kw):
    with pytest.raises(ValueError):
        impl.CircuitBreaker(**kw)


# ---- 第 4 关（选做）：退避冷却、状态变化通知 ------------------------------------


def test_part4_cooldown_backs_off_after_each_failed_probe_and_resets_on_recovery():
    cb, clock = make(failure_threshold=1, open_timeout=10, backoff_factor=2, max_open_timeout=25)
    fail(cb)
    clock.advance(10)
    fail(cb)                                                          # 第一次探测失败：冷却变 20
    clock.advance(19)
    with pytest.raises(impl.CircuitOpenError):
        cb.call(good)
    clock.advance(1)
    fail(cb)                                                          # 第二次探测失败：min(40, 25) = 25
    clock.advance(24)
    with pytest.raises(impl.CircuitOpenError):
        cb.call(good)
    clock.advance(1)
    assert cb.call(good) == "ok" and cb.state is State.CLOSED         # 恢复后复位
    fail(cb)
    clock.advance(10)
    assert cb.call(good) == "ok"                                      # 又是原来的 10 秒


def test_part4_state_changes_are_reported_in_order():
    seen = []
    cb, clock = make(failure_threshold=1, open_timeout=5, on_state_change=lambda old, new: seen.append((old, new)))
    fail(cb)
    clock.advance(5)
    fail(cb)
    clock.advance(5)
    cb.call(good)
    assert seen == [(State.CLOSED, State.OPEN), (State.OPEN, State.HALF_OPEN), (State.HALF_OPEN, State.OPEN),
                    (State.OPEN, State.HALF_OPEN), (State.HALF_OPEN, State.CLOSED)]


def test_part4_listener_runs_outside_the_lock():
    box = {}
    cb_holder = {}

    def listener(old, new):
        box["state_seen_inside_listener"] = cb_holder["cb"].state   # 在锁里调用的话，这一行会死锁
        box["metrics"] = cb_holder["cb"].metrics

    cb, _ = make(failure_threshold=1, on_state_change=listener)
    cb_holder["cb"] = cb
    t = threading.Thread(target=lambda: fail(cb), daemon=True)
    t.start()
    t.join(T)
    assert not t.is_alive()
    assert box["state_seen_inside_listener"] is State.OPEN


def test_part4_a_failing_listener_does_not_break_the_breaker():
    def listener(old, new):
        raise RuntimeError("monitoring is down")

    cb, clock = make(failure_threshold=1, open_timeout=1, on_state_change=listener)
    fail(cb)
    assert cb.state is State.OPEN
    clock.advance(1)
    assert cb.call(good) == "ok" and cb.state is State.CLOSED
