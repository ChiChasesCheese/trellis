"""线程池参考解的 pytest 套件：`IMPL=solution` 必须全绿，`IMPL=starter` 必须失败。

并发测试靠 `wait_until` 轮询 `pending`／`waiting_submitters` 或 `Event`／`Barrier` 来确认
状态，`Thread.join(timeout=...)`／`Future.result(timeout=...)` 只是防止真死锁把测试挂死，
从不是断言用时本身。
"""

import importlib
import os
import threading
import time

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def wait_until(predicate, timeout=2.0, interval=0.01) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


# ---- 第 1 关：worker 拉任务、Future、任务异常不杀死 worker ------------------


def test_submit_returns_a_future_carrying_the_result():
    pool = impl.ThreadPool(num_workers=2)
    future = pool.submit(lambda x, y: x + y, 3, 4)
    assert future.result(timeout=2) == 7
    assert future.done()
    pool.shutdown()


def test_exactly_as_many_tasks_run_at_once_as_there_are_workers():
    live, peak, guard = 0, 0, threading.Lock()
    rendezvous = threading.Barrier(3, timeout=5)

    def slow_task():
        nonlocal live, peak
        with guard:
            live += 1
            peak = max(peak, live)
        rendezvous.wait()
        with guard:
            live -= 1
        return "done"

    pool = impl.ThreadPool(num_workers=3)
    futures = [pool.submit(slow_task) for _ in range(6)]
    results = [f.result(timeout=5) for f in futures]
    pool.shutdown()
    assert peak == 3
    assert results == ["done"] * 6


def test_a_raising_task_does_not_kill_its_worker():
    pool = impl.ThreadPool(num_workers=1)

    def boom():
        raise ValueError("bad task")

    failing = pool.submit(boom)
    with pytest.raises(ValueError):
        failing.result(timeout=2)

    ok = pool.submit(lambda: 42)             # 同一个（唯一的）worker 必须还活着
    assert ok.result(timeout=2) == 42
    pool.shutdown()


def test_future_exception_method_returns_it_without_raising():
    pool = impl.ThreadPool(num_workers=1)

    def boom():
        raise KeyError("missing")

    future = pool.submit(boom)
    exc = future.exception(timeout=2)
    assert isinstance(exc, KeyError)
    pool.shutdown()


def test_add_done_callback_runs_immediately_if_already_done_and_later_otherwise():
    pool = impl.ThreadPool(num_workers=1)
    already_done = pool.submit(lambda: 1)
    already_done.result(timeout=2)
    seen = []
    already_done.add_done_callback(lambda f: seen.append(f.result()))
    assert seen == [1]                       # 已完成：同步立即执行

    still_running = pool.submit(lambda: 2)
    callback_ran = threading.Event()
    box = []

    def on_done(f):
        box.append(f.result())
        callback_ran.set()

    still_running.add_done_callback(on_done)
    assert callback_ran.wait(timeout=2)
    assert box == [2]
    pool.shutdown()


def test_result_raises_future_timeout_while_the_task_is_still_running():
    pool = impl.ThreadPool(num_workers=1)
    started, release = threading.Event(), threading.Event()

    def slow():
        started.set()
        release.wait(timeout=5)
        return "late"

    future = pool.submit(slow)
    assert started.wait(timeout=2)
    with pytest.raises(impl.FutureTimeout):
        future.result(timeout=0.05)
    release.set()
    assert future.result(timeout=2) == "late"
    pool.shutdown()


def test_num_workers_must_be_positive():
    with pytest.raises(ValueError):
        impl.ThreadPool(num_workers=0)


# ---- 第 2 关：shutdown(wait=True/False)，submit 之后失败 --------------------


def test_shutdown_wait_true_waits_for_every_queued_task_to_complete():
    pool = impl.ThreadPool(num_workers=2)
    done, guard = [], threading.Lock()

    def task(i):
        with guard:
            done.append(i)
        return i

    futures = [pool.submit(task, i) for i in range(10)]
    pool.shutdown(wait=True)
    assert sorted(done) == list(range(10))
    assert all(f.done() for f in futures)


def test_shutdown_wait_false_abandons_tasks_still_in_the_queue():
    pool = impl.ThreadPool(num_workers=1)
    started, release = threading.Event(), threading.Event()

    def blocker():
        started.set()
        release.wait(timeout=5)
        return "first"

    first = pool.submit(blocker)
    assert started.wait(timeout=2)
    queued = [pool.submit(lambda: "should never run") for _ in range(3)]
    pool.shutdown(wait=False)
    for future in queued:
        with pytest.raises(impl.PoolShutdown):
            future.result(timeout=2)
    release.set()
    assert first.result(timeout=2) == "first"   # 正在跑的任务不受影响


def test_submit_after_shutdown_raises_pool_shutdown():
    pool = impl.ThreadPool(num_workers=1)
    pool.shutdown()
    with pytest.raises(impl.PoolShutdown):
        pool.submit(lambda: 1)


def test_shutdown_called_twice_is_a_no_op_the_second_time():
    pool = impl.ThreadPool(num_workers=1)
    pool.shutdown()
    pool.shutdown()
    assert pool.is_shutdown


def test_context_manager_shuts_down_on_exit():
    with impl.ThreadPool(num_workers=2) as pool:
        assert pool.submit(lambda: "hi").result(timeout=2) == "hi"
    assert pool.is_shutdown


# ---- 第 3 关：背压——队满时挡住调用方 -----------------------------------------


def test_submit_blocks_the_caller_once_the_queue_is_at_capacity():
    pool = impl.ThreadPool(num_workers=1, queue_capacity=1)
    started, release = threading.Event(), threading.Event()

    def blocker():
        started.set()
        release.wait(timeout=5)

    pool.submit(blocker)                 # 占住唯一的 worker
    assert started.wait(timeout=2)
    pool.submit(lambda: None)            # 填满队列里唯一的位置，这次不阻塞

    blocked = threading.Thread(target=pool.submit, args=(lambda: None,))
    blocked.start()
    assert wait_until(lambda: pool.waiting_submitters == 1)
    release.set()
    blocked.join(timeout=2)
    assert not blocked.is_alive()
    pool.shutdown()


def test_queue_capacity_limits_pending_tasks_not_running_ones():
    """`queue_capacity` 挡的是"排队等着被取走"的任务数，不是"正在运行"的任务数：
    三个 worker、容量为 1，三个同时占住 worker 的任务应该都能立刻提交成功。"""
    pool = impl.ThreadPool(num_workers=3, queue_capacity=1)
    barrier = threading.Barrier(3, timeout=5)
    release = threading.Event()

    def blocker():
        barrier.wait()
        release.wait(timeout=5)
        return "ok"

    futures = []

    def submit_all():
        for _ in range(3):
            futures.append(pool.submit(blocker))

    submitter = threading.Thread(target=submit_all)
    submitter.start()
    submitter.join(timeout=5)
    assert not submitter.is_alive()
    assert len(futures) == 3
    release.set()
    assert [f.result(timeout=5) for f in futures] == ["ok"] * 3
    pool.shutdown()


def test_pending_reports_tasks_still_sitting_in_the_queue():
    pool = impl.ThreadPool(num_workers=1)
    started, release = threading.Event(), threading.Event()

    def gate():
        started.set()
        release.wait(timeout=5)

    pool.submit(gate)
    assert started.wait(timeout=2)
    pool.submit(lambda: None)
    pool.submit(lambda: None)
    assert wait_until(lambda: pool.pending == 2)
    release.set()
    pool.shutdown()


# ---- 第 4 关：per-task 优先级，不碰 worker 循环 -------------------------------


def test_lower_priority_number_runs_before_higher_ones():
    pool = impl.ThreadPool(num_workers=1)
    started, release = threading.Event(), threading.Event()

    def gate():
        started.set()
        release.wait(timeout=5)

    pool.submit(gate)                    # 挡住唯一的 worker，直到三个任务都排好队
    assert started.wait(timeout=2)

    order, guard = [], threading.Lock()

    def record(label):
        with guard:
            order.append(label)

    pool.submit(record, "low", priority=10)
    pool.submit(record, "high", priority=1)
    pool.submit(record, "mid", priority=5)
    release.set()
    pool.shutdown(wait=True)
    assert order == ["high", "mid", "low"]


def test_equal_priority_tasks_run_in_submission_order():
    pool = impl.ThreadPool(num_workers=1)
    started, release = threading.Event(), threading.Event()

    def gate():
        started.set()
        release.wait(timeout=5)

    pool.submit(gate)
    assert started.wait(timeout=2)

    order, guard = [], threading.Lock()

    def record(label):
        with guard:
            order.append(label)

    for label in ("a", "b", "c"):
        pool.submit(record, label, priority=1)
    release.set()
    pool.shutdown(wait=True)
    assert order == ["a", "b", "c"]
