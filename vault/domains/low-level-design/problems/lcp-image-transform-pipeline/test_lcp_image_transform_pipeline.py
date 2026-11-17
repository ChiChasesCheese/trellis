"""PixelFlow 的测试：契约逐条、准入窗口的纯逻辑、真线程下的并发上限。

并发测试只用事件和屏障，不用 sleep。所有等待都带 10 秒上限，只为把"挂死"变成一条断言失败；
正确的实现永远不会等到上限。上限类的断言（并发数、在途字节、取用数）对正确实现是确定的；
对违反上限的实现，只有违反发生在被拦住的任务放行之前才抓得到，调度器决定不了这件事，所以
"最多"这一类规则的确定性证明放在 `AdmissionWindow` 的单元测试里（不涉及线程，没有调度）。
"""

import importlib
import os
import random
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Job, Result, Pipeline, Window = impl.ImageJob, impl.TransformResult, impl.ImagePipeline, impl.AdmissionWindow

WAIT = 10


def must(event: threading.Event) -> None:
    assert event.wait(WAIT), "timed out waiting for an event"


def sized(letter: str, size: int) -> Job:
    """image_id 是字母，data 是 size 个同一个字母：单变换链里 len(data) 就是原图大小。"""
    return Job(letter, letter.encode() * size)


class Run:
    """在单独线程里跑 pipeline.run，让测试线程可以同时放行、观察被拦住的任务。"""

    def __init__(self, pipeline, jobs, transforms):
        self.outcome = {}
        self.thread = threading.Thread(target=self._go, args=(pipeline, jobs, transforms), daemon=True)
        self.thread.start()

    def _go(self, pipeline, jobs, transforms):
        try:
            self.outcome["results"] = pipeline.run(jobs, transforms)
        except BaseException as exc:  # noqa: BLE001 - 测试要把任何东西带回测试线程
            self.outcome["error"] = exc

    def result(self):
        self.thread.join(WAIT)
        assert not self.thread.is_alive(), "run() did not return"
        if "error" in self.outcome:
            raise self.outcome["error"]
        return self.outcome["results"]


class Counter:
    def __init__(self):
        self.lock = threading.Lock()
        self.value = 0

    def bump(self) -> int:
        with self.lock:
            self.value += 1
            return self.value


class Probe:
    """线程安全的记账：同时在变换里的任务数和原图字节数，以及各自的峰值。"""

    def __init__(self):
        self.lock = threading.Lock()
        self.active = self.peak = self.active_bytes = self.peak_bytes = 0

    def enter(self, size: int) -> None:
        with self.lock:
            self.active += 1
            self.active_bytes += size
            self.peak = max(self.peak, self.active)
            self.peak_bytes = max(self.peak_bytes, self.active_bytes)

    def leave(self, size: int) -> None:
        with self.lock:
            self.active -= 1
            self.active_bytes -= size


# ---------------------------------------------------------------- 单张图与结果

def test_readme_example():
    def uppercase_except_y(data):
        if data == b"y!":
            raise ValueError("invalid image")
        return data.upper()

    jobs = [Job("a", b"x"), Job("b", b"y"), Job("a", b"z")]
    results = Pipeline(2, 100).run(jobs, [lambda d: d + b"!", uppercase_except_y])
    assert results == [
        Result(0, "a", b"X!", None),
        Result(1, "b", None, "ValueError: invalid image"),
        Result(2, "a", b"Z!", None),
    ]


def test_empty_chain_is_identity_and_empty_batch_is_valid():
    assert Pipeline(2, 10).run([Job("a", b"abc"), Job("b", b"")], []) == [
        Result(0, "a", b"abc", None),
        Result(1, "b", b"", None),
    ]
    assert Pipeline(2, 10).run([], [bytes.upper]) == []
    assert Pipeline(2, 10).run(iter(()), []) == []


def test_each_transform_runs_once_in_order_and_feeds_the_next():
    calls = {}
    lock = threading.Lock()

    def step(tag):
        def transform(data):
            with lock:
                calls.setdefault(data[:1], []).append(tag)
            return data + tag.encode()

        return transform

    results = Pipeline(3, 100).run([Job("p", b"p"), Job("q", b"q")], [step("1"), step("2"), step("3")])
    assert [r.data for r in results] == [b"p123", b"q123"]
    assert calls == {b"p": ["1", "2", "3"], b"q": ["1", "2", "3"]}


def test_duplicate_ids_are_kept_and_index_is_the_input_position():
    jobs = [Job("same", bytes([i])) for i in range(6)]
    results = Pipeline(3, 100).run(jobs, [lambda d: d])
    assert [r.index for r in results] == list(range(6))
    assert [r.image_id for r in results] == ["same"] * 6
    assert [r.data for r in results] == [bytes([i]) for i in range(6)]


def test_failure_stops_that_image_only():
    calls = {}
    lock = threading.Lock()

    def step(n):
        def transform(data):
            with lock:
                calls.setdefault(data[:1], []).append(n)
            if n == 2 and data[:1] == b"b":
                raise KeyError("pixel")
            return data

        return transform

    jobs = [Job("a", b"a"), Job("b", b"b"), Job("c", b"c")]
    results = Pipeline(2, 100).run(jobs, [step(1), step(2), step(3)])
    assert [r.error for r in results] == [None, "KeyError: 'pixel'", None]
    assert results[1].data is None
    assert calls == {b"a": [1, 2, 3], b"b": [1, 2], b"c": [1, 2, 3]}


def test_error_text_keeps_type_empty_and_multiline_messages():
    class Odd(Exception):
        pass

    messages = {b"1": ValueError(), b"2": Odd("line one\nline two"), b"3": RuntimeError("")}

    def explode(data):
        raise messages[data]

    results = Pipeline(1, 10).run([Job(str(i), str(i).encode()) for i in (1, 2, 3)], [explode])
    assert [r.error for r in results] == ["ValueError: ", "Odd: line one\nline two", "RuntimeError: "]


def test_base_exception_is_not_caught():
    class Halt(BaseException):
        pass

    halt = Halt("stop")

    def transform(data):
        if data == b"boom":
            raise halt
        return data

    with pytest.raises(Halt) as info:
        Pipeline(2, 100).run([Job("a", b"a"), Job("b", b"boom"), Job("c", b"c")], [transform])
    assert info.value is halt


def test_matches_a_sequential_reference_on_a_random_batch():
    rng = random.Random(7)
    jobs = [Job(f"img{i % 7}", bytes(rng.randrange(256) for _ in range(rng.randrange(0, 30)))) for i in range(150)]

    def flip(data):
        return bytes(b ^ 0xFF for b in data)

    def picky(data):
        if sum(data) % 5 == 0:
            raise ValueError(f"bad sum {sum(data)}")
        return data[::-1]

    expected = []
    for i, job in enumerate(jobs):
        try:
            expected.append(Result(i, job.image_id, picky(flip(job.data)), None))
        except Exception as exc:
            expected.append(Result(i, job.image_id, None, f"{type(exc).__name__}: {exc}"))
    assert any(r.error for r in expected) and any(r.data is not None for r in expected)
    for workers, limit in [(1, 1), (3, 40), (8, 10_000)]:
        assert Pipeline(workers, limit).run(iter(jobs), [flip, picky]) == expected


def test_constructor_limits_must_be_positive():
    for workers, memory in [(0, 1), (1, 0), (-1, 5)]:
        with pytest.raises(ValueError):
            Pipeline(workers, memory)


def test_one_pipeline_serves_many_runs_including_overlapping_ones():
    pipeline = Pipeline(2, 100)
    assert pipeline.run([Job("a", b"a")], [bytes.upper]) == [Result(0, "a", b"A", None)]
    box = {}

    def go(tag):
        box[tag] = pipeline.run([Job(tag, tag.encode() * i) for i in range(1, 30)], [bytes.upper])

    threads = [threading.Thread(target=go, args=(tag,)) for tag in ("x", "y")]
    for t in threads:
        t.start()
    for t in threads:
        t.join(WAIT)
    for tag in ("x", "y"):
        assert [r.data for r in box[tag]] == [tag.upper().encode() * i for i in range(1, 30)]


# ---------------------------------------------------------------- 真线程：顺序、并发

def test_results_follow_input_order_when_completion_is_reversed():
    started = [threading.Event() for _ in range(3)]
    may_finish = [threading.Event() for _ in range(3)]
    finished = [threading.Event() for _ in range(3)]
    order, lock = [], threading.Lock()

    def transform(data):
        i = int(data)
        started[i].set()
        must(may_finish[i])
        with lock:
            order.append(i)
        finished[i].set()
        return data

    run = Run(Pipeline(3, 100), [Job(str(i), str(i).encode()) for i in range(3)], [transform])
    for event in started:
        must(event)  # 三张图同时在变换里：串行执行在这里就卡住
    for i in (2, 1, 0):  # 完成顺序恰好是输入顺序的反面
        may_finish[i].set()
        must(finished[i])
    assert [r.image_id for r in run.result()] == ["0", "1", "2"]
    assert order == [2, 1, 0]


@pytest.mark.parametrize("workers", [1, 2, 5])
def test_max_workers_chains_really_run_at_the_same_time(workers):
    barrier = threading.Barrier(workers, timeout=WAIT)
    probe = Probe()

    def transform(data):
        probe.enter(len(data))
        barrier.wait()  # 凑不齐 workers 个同时在场就是 BrokenBarrierError，变成这张图的错误
        probe.leave(len(data))
        return data

    jobs = [Job(str(i), b"x") for i in range(3 * workers)]
    results = Pipeline(workers, 10_000).run(jobs, [transform])
    assert [r.error for r in results] == [None] * len(jobs)
    assert probe.peak == workers


def test_never_more_chains_than_max_workers():
    workers = 3
    barrier = threading.Barrier(workers, timeout=WAIT)
    probe = Probe()

    def transform(data):
        probe.enter(1)
        barrier.wait()
        probe.leave(1)
        return data

    results = Pipeline(workers, 10_000).run([Job(str(i), b"x") for i in range(4 * workers)], [transform])
    assert all(r.error is None for r in results)
    assert probe.peak == workers  # 计数在变换返回之前减掉，所以它只会少算，不会多算


# ---------------------------------------------------------------- 惰性读取

def test_requests_stay_within_completions_plus_workers():
    workers, total = 2, 12
    entered, finished = Counter(), Counter()
    all_entered, gate = threading.Event(), threading.Event()
    violations = []

    def transform(data):
        if entered.bump() == workers:
            all_entered.set()
        must(gate)
        finished.bump()  # 在变换返回之前加：future 完成时它一定已经加过
        return data

    def source():
        for k in range(total):
            done = finished.value
            if k > done + workers:  # 取第 k 个时，已放行的 + 1 个队头 <= 完成数 + workers
                violations.append((k, done))
            yield Job(str(k), b"x")

    run = Run(Pipeline(workers, 10_000), source(), [transform])
    must(all_entered)
    gate.set()
    assert len(run.result()) == total
    assert violations == []


def test_while_every_chain_is_blocked_at_most_workers_plus_one_inputs_were_requested():
    workers = 3
    requested, entered = Counter(), Counter()
    all_entered, gate = threading.Event(), threading.Event()

    def transform(data):
        if entered.bump() == workers:
            all_entered.set()
        must(gate)
        return data

    def source():
        for k in range(20):
            requested.bump()
            yield Job(str(k), b"x")

    run = Run(Pipeline(workers, 10_000), source(), [transform])
    must(all_entered)
    assert requested.value <= workers + 1
    gate.set()
    assert len(run.result()) == 20


def test_a_failing_input_iterator_propagates_and_leaves_no_running_chain():
    started, ended = Counter(), Counter()

    def transform(data):
        started.bump()
        ended.bump()
        return data

    def source():
        yield Job("a", b"a")
        yield Job("b", b"b")
        yield Job("c", b"c")
        raise RuntimeError("source broke")

    with pytest.raises(RuntimeError, match="source broke"):
        Pipeline(2, 100).run(source(), [transform])
    assert started.value == ended.value  # run() 返回时没有链还在跑


# ---------------------------------------------------------------- 内存预算与先进先出

def test_two_jobs_that_exactly_fill_the_budget_run_together():
    barrier = threading.Barrier(2, timeout=WAIT)

    def transform(data):
        barrier.wait()  # 恰好等于预算也要放行：用 >= 比较的实现在这里凑不齐
        return data

    results = Pipeline(2, 10).run([sized("a", 5), sized("b", 5)], [transform])
    assert [r.error for r in results] == [None, None]


def test_in_flight_bytes_stay_within_the_budget_and_fill_it():
    probe = Probe()
    barrier = threading.Barrier(2, timeout=WAIT)

    def transform(data):
        probe.enter(len(data))
        barrier.wait()
        probe.leave(len(data))
        return data

    results = Pipeline(4, 10).run([sized("a", 4) for _ in range(8)], [transform])
    assert all(r.error is None for r in results)
    assert probe.peak_bytes == 8  # 4 + 4 能同时在途，4 + 4 + 4 = 12 > 10 不行


def test_head_of_line_is_not_skipped_for_a_smaller_later_job():
    requested = Counter()
    finished0, started0 = threading.Event(), threading.Event()
    release0 = threading.Event()
    seen = {}

    def transform(data):
        name = data[:1]
        if name == b"a":
            started0.set()
            must(release0)
            finished0.set()
        else:
            seen[name] = finished0.is_set()  # b、c 开始时 a 必须已经整条链结束
        return data

    def source():
        for job in (sized("a", 6), sized("b", 8), sized("c", 1)):
            requested.bump()
            yield job

    run = Run(Pipeline(3, 10), source(), [transform])
    must(started0)
    assert requested.value <= 2  # a 已放行，b 是等待放行的队头，c 不能被取出来
    release0.set()
    results = run.result()
    assert [r.error for r in results] == [None] * 3
    assert seen == {b"b": True, b"c": True}  # 6 + 1 本来放得下，但队头 b 在前面


def test_an_oversized_head_waits_for_everything_then_runs_alone():
    probe = Probe()
    seen = {}
    lock = threading.Lock()
    release_first = threading.Event()
    first_in = threading.Event()

    def transform(data):
        name = data[:1]
        probe.enter(len(data))
        with lock:
            seen[name] = probe.active  # 进来时同时在变换里的图数（含自己）
        if name == b"a":
            first_in.set()
            must(release_first)
        probe.leave(len(data))
        return data

    run = Run(Pipeline(3, 10), [sized("a", 3), sized("b", 25), sized("c", 3)], [transform])
    must(first_in)
    release_first.set()
    results = run.result()
    assert [r.error for r in results] == [None] * 3
    assert seen[b"b"] == 1  # 超大的 b 进来时没有任何别的图在途
    assert seen[b"c"] == 1  # c 要等 b 结束


def test_a_single_job_larger_than_the_whole_budget_still_completes():
    results = Pipeline(4, 1).run([sized("a", 50), sized("b", 50)], [bytes.upper])
    assert [r.data for r in results] == [b"A" * 50, b"B" * 50]


def test_a_failed_job_gives_its_bytes_back():
    def transform(data):
        if data[:1] == b"a":
            raise ValueError("bad")
        return data

    run = Run(Pipeline(2, 10), [sized("a", 8), sized("b", 8), sized("c", 8)], [transform])
    results = run.result()  # 失败时不还字节，b 永远放不进去，这里就挂死
    assert [r.error for r in results] == ["ValueError: bad", None, None]


# ---------------------------------------------------------------- 准入窗口：纯逻辑，没有调度

def test_window_never_admits_more_jobs_than_slots():
    window = Window(2, 1000)
    assert [window.try_admit(1) for _ in range(3)] == [True, True, False]
    assert (window.jobs_in_flight, window.bytes_in_flight, window.has_slot) == (2, 2, False)
    window.release(1)
    assert window.has_slot and window.try_admit(1)


def test_window_budget_boundary_is_inclusive():
    window = Window(5, 10)
    assert window.try_admit(5) and window.try_admit(5)  # 5 + 5 恰好等于预算
    assert not window.try_admit(1)
    window.release(5)
    assert not window.try_admit(6)  # 5 + 6 = 11 > 10
    assert window.try_admit(5)


def test_window_oversized_head_enters_only_when_empty_and_then_excludes_everyone():
    window = Window(5, 10)
    assert window.try_admit(1)
    assert not window.try_admit(25)  # 有别的图在途，超大的不能进
    window.release(1)
    assert window.try_admit(25)  # 空了才进
    assert not window.try_admit(1)  # 它在途时，连 1 字节也不行
    assert not window.try_admit(0)  # 0 字节同样：总数已经超过预算
    window.release(25)
    assert window.try_admit(1)


def test_window_refusal_changes_nothing():
    window = Window(1, 10)
    assert window.try_admit(4)
    for size in (1, 0, 7):
        assert not window.try_admit(size)
    assert (window.jobs_in_flight, window.bytes_in_flight) == (1, 4)


def test_window_can_admit_only_asks():
    window = Window(2, 10)
    assert window.can_admit(10) and window.can_admit(11)  # 空窗口：恰好用满和超大的都可以
    assert (window.jobs_in_flight, window.bytes_in_flight) == (0, 0)  # 问不改状态
    window.try_admit(6)
    assert window.can_admit(4) and not window.can_admit(5)


def test_window_release_more_than_admitted_is_an_error_not_an_assert():
    window = Window(2, 10)
    with pytest.raises(RuntimeError):
        window.release(1)
    window.try_admit(3)
    with pytest.raises(RuntimeError):
        window.release(4)
    assert (window.jobs_in_flight, window.bytes_in_flight) == (1, 3)


def test_window_rejects_invalid_arguments():
    for args in [(0, 1), (1, 0)]:
        with pytest.raises(ValueError):
            Window(*args)
    with pytest.raises(ValueError):
        Window(1, 1).try_admit(-1)
