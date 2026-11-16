import gc
import importlib
import itertools
import json
import math
import os
import random
import weakref

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
Sample, Event, StackRun = impl.Sample, impl.Event, impl.StackRun
TraceConverter, convert_samples, compress_samples = impl.TraceConverter, impl.convert_samples, impl.compress_samples


def S(ts, *names):
    return Sample(ts, tuple(names))


def start(ts, name):
    return Event("start", ts, name)


def end(ts, name):
    return Event("end", ts, name)


def run_all(samples, n=1):
    converter = TraceConverter(n)
    out = []
    for sample in samples:
        out.extend(converter.feed(sample))
    return out


# ------------------------------------------------------------------ 独立的参照模型（只看完整历史，不带任何状态）

def oracle_events(stacks, n):
    """第 j 个采样的事件，直接按定义算：前缀 p 在 j 时已确认 = 它是最近 n 个采样（含 j）每一个的前缀。"""
    def confirmed(j):
        if j < 0 or j + 1 < n:
            return set()
        window = stacks[j + 1 - n: j + 1]
        top = stacks[j]
        return {top[: i + 1] for i in range(len(top)) if all(w[: i + 1] == top[: i + 1] for w in window)}

    out = []
    for j, top in enumerate(stacks):
        ts = j * 3 + 1
        before, now = confirmed(j - 1), confirmed(j)
        # 上一个采样已确认、但不是本栈前缀的帧：从叶到根结束
        gone = sorted((p for p in before if top[: len(p)] != p), key=len, reverse=True)
        out += [end(ts, p[-1]) for p in gone]
        # 本次刚确认（上一个采样时没确认）的帧：从根到叶开始
        out += [start(ts, p[-1]) for p in sorted(now - before, key=len)]
    return out


def oracle_snapshot(stacks, n):
    if not stacks:
        return {"version": 1, "confirmations": n, "last_ts": None, "previous": [], "streaks": []}
    j = len(stacks) - 1
    top = stacks[j]
    streaks = []
    for i in range(len(top)):
        run = 0
        while run <= j and stacks[j - run][: i + 1] == top[: i + 1]:
            run += 1
        streaks.append(min(n, run))
    return {"version": 1, "confirmations": n, "last_ts": j * 3 + 1, "previous": list(top), "streaks": streaks}


def random_stacks(rng, length):
    names = ["a", "b", "c"]
    stacks = []
    for _ in range(length):
        if stacks and rng.random() < 0.45:  # 偏向重复和只改末尾，让前缀与连续次数真的起作用
            base = list(stacks[-1])
            if base and rng.random() < 0.6:
                base[rng.randrange(len(base))] = rng.choice(names)
            if rng.random() < 0.3:
                base = base[: rng.randrange(len(base) + 1)]
            stacks.append(tuple(base))
        else:
            stacks.append(tuple(rng.choice(names) for _ in range(rng.randrange(0, 6))))
    return stacks


def as_samples(stacks):
    return [Sample(j * 3 + 1, stack) for j, stack in enumerate(stacks)]


# ------------------------------------------------------------------ README 的例子与第 1、2 关

def test_readme_example():
    converter = TraceConverter(confirmations=2)
    assert converter.feed(Sample(1, ["main"])) == []
    state = converter.snapshot()
    assert state == {"version": 1, "confirmations": 2, "last_ts": 1, "previous": ["main"], "streaks": [1]}
    resumed = TraceConverter.from_snapshot(state)
    assert resumed.feed(Sample(2, ["main"])) == [start(2, "main")]
    assert resumed.feed(Sample(3, [])) == [end(3, "main")]


def test_close_old_suffix_before_opening_new_one():
    converter = TraceConverter()
    assert converter.feed(Sample(1, ("main", "read"))) == [start(1, "main"), start(1, "read")]
    assert converter.feed(Sample(2, ("main", "write"))) == [end(2, "read"), start(2, "write")]
    assert converter.feed(Sample(3, ("main", "write"))) == []  # 相同的栈什么也不产生


def test_empty_stack_closes_everything_leaf_first():
    events = run_all([S(1, "a", "b", "c"), S(2)])
    assert events[-3:] == [end(2, "c"), end(2, "b"), end(2, "a")]


def test_input_exhaustion_emits_no_end_events():
    assert list(convert_samples([S(0, "main")])) == [start(0, "main")]
    assert list(convert_samples([])) == []


def test_identity_is_the_full_prefix_not_the_name():
    # 递归：同名的帧在不同深度是不同的帧
    assert run_all([S(1, "f"), S(2, "f", "f"), S(3, "f", "f", "f"), S(4, "f", "f")]) == [
        start(1, "f"), start(2, "f"), start(3, "f"), end(4, "f")]
    # 根变了，叶子同名也要先结束再开始
    assert run_all([S(1, "a", "x"), S(2, "b", "x")]) == [
        start(1, "a"), start(1, "x"), end(2, "x"), end(2, "a"), start(2, "b"), start(2, "x")]


def test_no_call_is_inferred_between_samples():
    # 从 (a,b,c) 直接到 (a,d)：只有 c、b 结束和 d 开始，不会"补出"中间的调用
    events = run_all([S(1, "a", "b", "c"), S(2, "a", "d")])
    assert events[3:] == [end(2, "c"), end(2, "b"), start(2, "d")]


def test_event_timestamp_and_name_are_taken_as_is():
    events = run_all([Sample(1.5, ["  sp ace ", "ünï-名字"])])
    assert events == [start(1.5, "  sp ace "), start(1.5, "ünï-名字")]


# ------------------------------------------------------------------ 第 3 关：确认

def test_debounce_opens_on_the_nth_consecutive_sample():
    converter = TraceConverter(3)
    assert converter.feed(S(1, "m")) == []
    assert converter.feed(S(2, "m")) == []
    assert converter.feed(S(3, "m")) == [start(3, "m")]  # 用确认那个采样的时间戳，不回填
    assert converter.feed(S(4, "m")) == []


def test_preserved_parent_keeps_its_streak_when_child_changes():
    events = run_all([S(1, "m", "x"), S(2, "m", "y"), S(3, "m", "y")], 2)
    # m 在第 2 个采样确认；x 只出现一次，从未确认；y 在第 3 个采样确认
    assert events == [start(2, "m"), start(3, "y")]


def test_break_resets_the_streak_so_runs_never_add_up():
    assert run_all([S(1, "m"), S(2), S(3, "m")], 2) == []
    assert run_all([S(1, "m"), S(2), S(3, "m"), S(4, "m")], 2) == [start(4, "m")]


def test_confirmed_frame_ends_at_once_and_unconfirmed_never_ends():
    events = run_all([S(1, "a", "b"), S(2, "a", "b"), S(3, "c"), S(4, "c"), S(5)], 2)
    assert events == [start(2, "a"), start(2, "b"), end(3, "b"), end(3, "a"), start(4, "c"), end(5, "c")]
    # 第 3 个采样的 c 只出现一次就被替换：它没确认过，所以没有结束事件
    assert run_all([S(1, "a"), S(2, "a"), S(3, "c"), S(4, "a")], 2) == [start(2, "a"), end(3, "a")]


def test_ends_come_before_starts_and_leaf_before_root_in_one_sample():
    events = run_all([S(1, "a", "b", "c"), S(2, "a", "b", "c"), S(3, "a", "x", "y"), S(4, "a", "x", "y")], 2)
    at3 = [e for e in events if e.ts == 3]
    assert at3 == [end(3, "c"), end(3, "b")]
    assert [e for e in events if e.ts == 4] == [start(4, "x"), start(4, "y")]


def test_parent_and_child_confirmed_in_the_same_sample_start_root_first():
    assert run_all([S(1, "a", "b"), S(2, "a", "b")], 2) == [start(2, "a"), start(2, "b")]


def test_recursive_frames_confirm_independently():
    events = run_all([S(1, "f"), S(2, "f", "f"), S(3, "f", "f"), S(4, "f")], 2)
    assert events == [start(2, "f"), start(3, "f"), end(4, "f")]


@pytest.mark.parametrize("bad", [0, -1, True, False, 1.0, "2", None, 2.5])
def test_confirmations_must_be_a_positive_exact_int(bad):
    with pytest.raises(ValueError):
        TraceConverter(bad)
    with pytest.raises(ValueError):
        convert_samples([], bad)


def test_each_converter_owns_its_state():
    one, two = TraceConverter(1), TraceConverter(1)
    one.feed(S(5, "a"))
    assert two.feed(S(1, "b")) == [start(1, "b")]  # 另一个转换器的时间戳不影响它
    assert two.snapshot()["previous"] == ["b"]


# ------------------------------------------------------------------ 第 4 关：惰性与压缩

class Counting:
    """记录被读了几个采样的迭代器。"""

    def __init__(self, samples):
        self.samples, self.read = list(samples), 0

    def __iter__(self):
        for sample in self.samples:
            self.read += 1
            yield sample


def test_convert_samples_reads_nothing_until_iteration_starts():
    source = Counting([S(1, "a"), S(2, "b")])
    stream = convert_samples(source)
    assert source.read == 0
    next(stream)
    assert source.read == 1


def test_convert_samples_finishes_the_current_samples_events_before_reading_on():
    source = Counting([S(1, "a", "b", "c"), S(2, "a", "b", "c"), S(3, "x")])
    stream = convert_samples(source)
    assert [next(stream), next(stream), next(stream)] == [start(1, "a"), start(1, "b"), start(1, "c")]
    assert source.read == 1  # 三个事件都来自第一个采样
    assert next(stream) == end(3, "c")  # 第二个采样没有事件，读到第三个才有
    assert source.read == 3


def test_convert_samples_equals_feeding_a_fresh_converter():
    rng = random.Random(7)
    for seed in range(60):
        stacks = random_stacks(random.Random(seed), rng.randrange(0, 20))
        n = 1 + seed % 4
        samples = as_samples(stacks)
        assert list(convert_samples(samples, n)) == run_all(samples, n), (seed, n)


def test_convert_samples_keeps_no_history():
    alive = []

    def source():
        for j in range(200):
            sample = Sample(j + 1, ("a", "b", str(j % 3)))
            alive.append(weakref.ref(sample))
            yield sample

    stream = convert_samples(source(), 2)
    peak = 0
    for _ in stream:
        gc.collect()
        peak = max(peak, sum(ref() is not None for ref in alive))
    assert peak <= 1  # 派生的上界：最多只有手上这一个采样还活着
    assert sum(ref() is not None for ref in alive) == 0


def test_compress_runs_report_first_and_last_timestamp_and_count():
    samples = [S(1, "a"), S(4, "a"), S(5), S(6), S(9, "a"), S(10, "a", "b")]
    assert list(compress_samples(samples)) == [
        StackRun(1, 4, ("a",), 2), StackRun(5, 6, (), 2), StackRun(9, 9, ("a",), 1), StackRun(10, 10, ("a", "b"), 1)]
    assert list(compress_samples([])) == []
    assert isinstance(next(compress_samples([Sample(1, ["a"])])).stack, tuple)


def test_compress_yields_a_run_as_soon_as_the_first_changed_sample_is_read():
    source = Counting([S(1, "a"), S(2, "a"), S(3, "b"), S(4, "b"), S(5, "c")])
    stream = compress_samples(source)
    assert source.read == 0
    assert next(stream) == StackRun(1, 2, ("a",), 2)
    assert source.read == 3
    assert next(stream) == StackRun(3, 4, ("b",), 2)
    assert source.read == 5


def test_compress_matches_groupby_oracle_and_applies_no_debounce():
    for seed in range(60):
        stacks = random_stacks(random.Random(seed), random.Random(seed).randrange(0, 25))
        expected = []
        for key, group in itertools.groupby(enumerate(stacks), key=lambda item: item[1]):
            idx = [j for j, _ in group]
            expected.append(StackRun(idx[0] * 3 + 1, idx[-1] * 3 + 1, key, len(idx)))
        assert list(compress_samples(as_samples(stacks))) == expected, seed


def test_compress_validates_and_earlier_output_stays_out():
    stream = compress_samples([S(1, "a"), S(2, "b"), Sample(2, ("c",))])
    assert next(stream) == StackRun(1, 1, ("a",), 1)
    with pytest.raises(ValueError):
        next(stream)
    with pytest.raises(ValueError):
        list(compress_samples([Sample(1, ("",))]))


# ------------------------------------------------------------------ 第 5 关：先校验再提交

@pytest.mark.parametrize("ts", [True, False, math.nan, math.inf, -math.inf, -1, -0.5, "1", None, [1], 1 + 0j])
def test_bad_timestamps_are_rejected(ts):
    converter = TraceConverter()
    with pytest.raises(ValueError):
        converter.feed(Sample(ts, ("a",)))
    assert converter.snapshot()["last_ts"] is None
    with pytest.raises(ValueError):
        list(compress_samples([Sample(ts, ("a",))]))


def test_timestamps_must_strictly_increase():
    converter = TraceConverter()
    converter.feed(S(5, "a"))
    for bad in (5, 4, 5.0, 4.999):
        with pytest.raises(ValueError):
            converter.feed(Sample(bad, ("a",)))
    assert converter.feed(S(5.5, "a")) == []
    with pytest.raises(ValueError):
        list(compress_samples([S(2, "a"), S(2, "a")]))


def test_zero_is_a_valid_first_timestamp():
    assert run_all([S(0, "a")]) == [start(0, "a")]
    assert run_all([S(0.0, "a")]) == [start(0.0, "a")]


def test_timestamps_compare_exactly_without_converting_ints_to_floats():
    big = 2 ** 53
    converter = TraceConverter()
    converter.feed(Sample(float(big), ("a",)))
    assert converter.feed(Sample(big + 1, ("a",))) == []  # 转成 float 就会相等而被拒绝
    with pytest.raises(ValueError):
        converter.feed(Sample(float(big), ("a",)))  # 2**53 小于已经收下的 2**53+1
    assert converter.feed(Sample(float(big + 2), ("a",))) == []  # 2**53+2 能精确表示，且大于 2**53+1
    equal = TraceConverter()
    equal.feed(Sample(big, ("a",)))
    with pytest.raises(ValueError):
        equal.feed(Sample(float(big), ("a",)))  # int 与 float 数值相等也是重复
    huge = 10 ** 400  # 超出 float 的范围，math.isfinite 会溢出
    converter = TraceConverter()
    assert converter.feed(Sample(huge, ("a",))) == [start(huge, "a")]
    assert converter.feed(Sample(huge + 1, ())) == [end(huge + 1, "a")]
    with pytest.raises(ValueError):
        converter.feed(Sample(huge, ("a",)))
    with pytest.raises(ValueError):
        converter.feed(Sample(1.0, ("a",)))  # 任何 float 都小于 10**400


@pytest.mark.parametrize("stack", [("a", ""), ("", ), (1,), ("a", None), (b"a",), ["a", 3], "ab", None, 7])
def test_bad_stacks_are_rejected(stack):
    with pytest.raises(ValueError):
        TraceConverter().feed(Sample(1, stack))
    with pytest.raises(ValueError):
        list(compress_samples([Sample(1, stack)]))


def test_failed_feed_leaves_no_trace_and_does_not_consume_its_timestamp():
    converter = TraceConverter(2)
    converter.feed(S(1, "m", "x"))
    before = converter.snapshot()
    with pytest.raises(ValueError):
        converter.feed(Sample(2, ("m", "x", "")))  # 名字不合格：时间戳 2 不能被消耗
    with pytest.raises(ValueError):
        converter.feed(Sample(0, ("m", "x")))
    assert converter.snapshot() == before
    assert converter.feed(S(2, "m", "x")) == [start(2, "m"), start(2, "x")]  # 连续次数没被打断


def test_stack_is_copied_before_it_is_stored():
    stack = ["a", "b"]
    converter = TraceConverter()
    converter.feed(Sample(1, stack))
    stack.append("c")
    stack[0] = "z"
    assert converter.snapshot()["previous"] == ["a", "b"]
    assert converter.feed(Sample(2, ["a", "b"])) == []


def test_whitespace_and_unicode_names_are_valid_and_kept():
    names = [" ", "\t", "名字", "ß", "a b"]
    assert [e.name for e in run_all([Sample(1, names)])] == names


# ------------------------------------------------------------------ 第 6 关：快照

def test_snapshot_shape_before_and_after_samples():
    converter = TraceConverter(3)
    assert converter.snapshot() == {"version": 1, "confirmations": 3, "last_ts": None, "previous": [], "streaks": []}
    converter.feed(S(1, "a", "b"))
    converter.feed(S(2, "a", "c"))
    assert converter.snapshot() == {"version": 1, "confirmations": 3, "last_ts": 2, "previous": ["a", "c"], "streaks": [2, 1]}
    converter.feed(S(3))
    assert converter.snapshot() == {"version": 1, "confirmations": 3, "last_ts": 3, "previous": [], "streaks": []}


def test_streaks_are_capped_at_n():
    converter = TraceConverter(2)
    for ts in range(1, 6):
        converter.feed(S(ts, "a", "b"))
    assert converter.snapshot()["streaks"] == [2, 2]


def test_snapshot_and_restored_state_own_their_lists():
    converter = TraceConverter(2)
    converter.feed(S(1, "a"))
    state = converter.snapshot()
    state["previous"].append("hacked")
    state["streaks"][0] = 99
    assert converter.snapshot()["previous"] == ["a"]
    state = converter.snapshot()
    first, second = TraceConverter.from_snapshot(state), TraceConverter.from_snapshot(state)
    state["previous"].append("later")
    state["streaks"].append(1)
    assert first.feed(S(2, "a")) == [start(2, "a")]
    assert second.snapshot()["previous"] == ["a"]  # 另一个恢复出来的转换器不受影响
    assert converter.snapshot()["streaks"] == [1]  # 原转换器也不受影响


def test_restored_converter_requires_strictly_greater_timestamp():
    converter = TraceConverter()
    converter.feed(S(7, "a"))
    restored = TraceConverter.from_snapshot(converter.snapshot())
    for bad in (7, 6.9, 0):
        with pytest.raises(ValueError):
            restored.feed(Sample(bad, ("a",)))
    assert restored.feed(S(7.1, "b")) == [end(7.1, "a"), start(7.1, "b")]
    empty = TraceConverter.from_snapshot(TraceConverter(4).snapshot())
    assert empty.snapshot()["confirmations"] == 4
    assert empty.feed(S(0, "a")) == []


def test_restore_emits_nothing_and_resumes_a_pending_recursive_stack():
    converter = TraceConverter(3)
    for ts in (1, 2):
        converter.feed(S(ts, "f", "f", "f"))
    restored = TraceConverter.from_snapshot(converter.snapshot())
    assert restored.feed(S(3, "f", "f", "f")) == [start(3, "f"), start(3, "f"), start(3, "f")]
    assert restored.feed(S(4, "f")) == [end(4, "f"), end(4, "f")]


def valid_state(**override):
    state = {"version": 1, "confirmations": 3, "last_ts": 5, "previous": ["a", "b"], "streaks": [3, 2]}
    state.update(override)
    return state


@pytest.mark.parametrize("state", [
    None, [], "x", 3,
    {k: v for k, v in valid_state().items() if k != "version"},
    {**valid_state(), "extra": 1},
    valid_state(version=2), valid_state(version=True), valid_state(version=1.0), valid_state(version="1"),
    valid_state(confirmations=0), valid_state(confirmations=True), valid_state(confirmations=3.0),
    valid_state(previous=("a", "b")), valid_state(streaks=(3, 2)), valid_state(previous=["a"]),
    valid_state(streaks=[3]), valid_state(previous=["a", ""]), valid_state(previous=["a", 7]),
    valid_state(last_ts=None), valid_state(last_ts=True), valid_state(last_ts=math.nan),
    valid_state(last_ts=-1), valid_state(last_ts="5"), valid_state(last_ts=math.inf),
    valid_state(last_ts=None, previous=[], streaks=[3]), valid_state(last_ts=None, previous=["a"], streaks=[]),
    valid_state(streaks=[3, 0]), valid_state(streaks=[4, 2]), valid_state(streaks=[3.0, 2]), valid_state(streaks=[True, 1]),
    valid_state(streaks=[1, 2]), valid_state(streaks=[2, 3]),
])
def test_invalid_snapshots_are_rejected(state):
    with pytest.raises(ValueError):
        TraceConverter.from_snapshot(state)


def test_structurally_valid_snapshots_are_accepted():
    for state in (valid_state(), valid_state(last_ts=2.5), valid_state(last_ts=10 ** 400),
                  valid_state(last_ts=0, previous=[], streaks=[]), valid_state(streaks=[1, 1]),
                  valid_state(confirmations=1, streaks=[1, 1])):
        assert TraceConverter.from_snapshot(state).snapshot() == state


# ------------------------------------------------------------------ 属性测试：很多随机流、很多快照点

def test_incremental_events_and_snapshot_match_the_history_oracle():
    for seed in range(300):
        rng = random.Random(seed)
        stacks = random_stacks(rng, rng.randrange(0, 22))
        n = 1 + seed % 4
        converter = TraceConverter(n)
        got = []
        for j, sample in enumerate(as_samples(stacks)):
            got += converter.feed(sample)
            assert converter.snapshot() == oracle_snapshot(stacks[: j + 1], n), (seed, n, j)
        assert got == oracle_events(stacks, n), (seed, n)


def test_resume_gives_identical_output_at_every_snapshot_point():
    checked = 0
    for seed in range(400):
        rng = random.Random(1000 + seed)
        stacks = random_stacks(rng, rng.randrange(0, 26))
        n = 1 + seed % 5
        samples = as_samples(stacks)
        reference = TraceConverter(n)
        expected = [reference.feed(s) for s in samples]
        for split in range(len(samples) + 1):
            head = TraceConverter(n)
            for s in samples[:split]:
                head.feed(s)
            state = json.loads(json.dumps(head.snapshot()))  # 经过 JSON 往返，真的落过盘也一样
            resumed = TraceConverter.from_snapshot(state)
            assert resumed.snapshot() == head.snapshot(), (seed, split)
            tail = [resumed.feed(s) for s in samples[split:]]
            assert tail == expected[split:], (seed, n, split)
            assert resumed.snapshot() == reference.snapshot(), (seed, n, split)
            checked += 1
    assert checked > 5000


def test_resuming_after_every_single_sample_is_still_identical():
    for seed in range(200):
        rng = random.Random(5000 + seed)
        stacks = random_stacks(rng, rng.randrange(1, 30))
        n = 1 + seed % 4
        samples = as_samples(stacks)
        expected = run_all(samples, n)
        converter, got = TraceConverter(n), []
        for s in samples:
            got += converter.feed(s)
            converter = TraceConverter.from_snapshot(converter.snapshot())  # 每个采样之后都重启一次
        assert got == expected, (seed, n)


def test_failed_feeds_anywhere_leave_the_output_unchanged():
    for seed in range(150):
        rng = random.Random(9000 + seed)
        stacks = random_stacks(rng, rng.randrange(1, 20))
        n = 1 + seed % 4
        samples = as_samples(stacks)
        clean, noisy = TraceConverter(n), TraceConverter(n)
        for s in samples:
            before = noisy.snapshot()
            for bad in (Sample(s.ts, s.stack + ("",)), Sample(s.ts, (*s.stack, 5)), Sample(-1, s.stack), Sample(True, s.stack)):
                if rng.random() < 0.5:
                    with pytest.raises(ValueError):
                        noisy.feed(bad)
                    assert noisy.snapshot() == before
            assert noisy.feed(s) == clean.feed(s), (seed, n)
        assert noisy.snapshot() == clean.snapshot()
