import hashlib
import importlib
import os
import random
import threading
import tracemalloc
from pathlib import Path

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def put(root: Path, name: str, data: bytes) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


class Probe(impl.FileDeduplicator):
    """记录两个钩子的调用，并可以让指定路径的钩子抛异常。"""

    def __init__(self, *args, fail_sample=(), fail_full=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.samples: list[str] = []
        self.fulls: list[str] = []
        self.fail_sample = {str(p) for p in fail_sample}
        self.fail_full = {str(p) for p in fail_full}
        self._lock = threading.Lock()

    def _sample_fingerprint(self, path, size):
        with self._lock:
            self.samples.append(str(path))
        if str(path) in self.fail_sample:
            super()._sample_fingerprint(path, size)  # 先真的读一遍，再抛：读到的字节不能计入
            raise OSError("sample boom")
        return super()._sample_fingerprint(path, size)

    def _full_digest(self, path):
        with self._lock:
            self.fulls.append(str(path))
        if str(path) in self.fail_full:
            super()._full_digest(path)
            raise OSError("hash boom")
        return super()._full_digest(path)


# ---- README 的例子与基本形状 ----

def test_readme_example_two_groups_and_a_missing_path(tmp_path):
    a = put(tmp_path, "a.txt", b"alpha")
    b = put(tmp_path, "b.txt", b"bravo!")
    c = put(tmp_path, "c.txt", b"alpha")
    d = put(tmp_path, "d.txt", b"bravo!")
    missing = tmp_path / "missing.txt"
    report = impl.FileDeduplicator().scan([d, missing, c, b, a])
    assert report.groups == (
        impl.DuplicateGroup(str(a), (str(c),), 5),
        impl.DuplicateGroup(str(b), (str(d),), 6),
    )
    assert [i.path for i in report.issues] == [str(missing)]
    assert "No such file" in report.issues[0].error
    assert report.files_considered == 4


def test_constructor_limits_must_be_positive():
    for workers, sample in [(0, 1), (1, 0), (-1, 5)]:
        with pytest.raises(ValueError):
            impl.FileDeduplicator(workers, sample)
    impl.FileDeduplicator(1, 1)


def test_empty_input_is_a_valid_empty_report():
    assert impl.FileDeduplicator().scan([]) == impl.ScanReport((), (), 0, 0)


def test_one_pass_iterable_is_consumed_once(tmp_path):
    a = put(tmp_path, "a", b"same")
    b = put(tmp_path, "b", b"same")
    report = impl.FileDeduplicator().scan(p for p in [b, a])
    assert report.groups == (impl.DuplicateGroup(str(a), (str(b),), 4),)


def test_string_roots_and_path_roots_are_the_same_identity(tmp_path):
    a = put(tmp_path, "a", b"x")
    report = impl.FileDeduplicator().scan([str(a), a, str(tmp_path) + "/a", tmp_path / "." / "a"])
    assert report.files_considered == 1


# ---- 发现：目录、重叠根、软链接、特殊文件 ----

def test_directories_are_walked_recursively_and_overlapping_roots_count_once(tmp_path):
    put(tmp_path, "top.txt", b"payload")
    put(tmp_path, "sub/deep/copy.txt", b"payload")
    probe = Probe()
    report = probe.scan([tmp_path, tmp_path / "sub", tmp_path / "sub" / "deep" / "copy.txt", str(tmp_path) + "/"])
    assert report.files_considered == 2
    assert len(report.groups) == 1 and report.groups[0].size == 7
    assert sorted(probe.samples) == sorted(set(probe.samples))  # 没有路径被抽样两次
    assert len(probe.samples) == 2


def test_symlinks_are_reported_not_followed(tmp_path):
    real = put(tmp_path, "real.txt", b"data")
    twin = put(tmp_path, "twin.txt", b"data")
    (tmp_path / "link.txt").symlink_to(real)
    (tmp_path / "broken").symlink_to(tmp_path / "nowhere")
    other = tmp_path / "other"
    put(other, "inside.txt", b"data")
    (tmp_path / "dirlink").symlink_to(other, target_is_directory=True)
    report = impl.FileDeduplicator().scan([tmp_path / "link.txt", tmp_path / "broken", tmp_path / "dirlink", real, twin])
    assert {i.path for i in report.issues} == {str(tmp_path / "link.txt"), str(tmp_path / "broken"), str(tmp_path / "dirlink")}
    assert report.files_considered == 2
    assert report.groups == (impl.DuplicateGroup(str(real), (str(twin),), 4),)
    walked = impl.FileDeduplicator().scan([tmp_path])
    assert str(tmp_path / "other" / "inside.txt") in {s for g in walked.groups for s in (g.canonical, *g.duplicates)}
    assert str(tmp_path / "dirlink") in {i.path for i in walked.issues}
    assert walked.files_considered == 3  # real、twin、inside；软链接指向的目录不会被走第二遍


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="needs fifo support")
def test_special_files_become_issues_and_do_not_block(tmp_path):
    fifo = tmp_path / "pipe"
    os.mkfifo(fifo)
    a = put(tmp_path, "a", b"zz")
    b = put(tmp_path, "b", b"zz")
    report = impl.FileDeduplicator().scan([tmp_path])  # 打开一个没人写的 fifo 会永远阻塞：必须不打开它
    assert [i.path for i in report.issues] == [str(fifo)]
    assert report.groups == (impl.DuplicateGroup(str(a), (str(b),), 2),)
    assert report.files_considered == 2


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores permissions")
def test_unreadable_directory_is_one_issue_and_siblings_survive(tmp_path):
    locked = tmp_path / "locked"
    put(locked, "hidden", b"qq")
    a = put(tmp_path, "a", b"qq")
    b = put(tmp_path, "b", b"qq")
    locked.chmod(0)
    try:
        report = impl.FileDeduplicator().scan([tmp_path])
    finally:
        locked.chmod(0o755)
    assert [i.path for i in report.issues] == [str(locked)]
    assert "Permission denied" in report.issues[0].error
    assert report.groups == (impl.DuplicateGroup(str(a), (str(b),), 2),)


def test_repeated_missing_path_is_one_issue(tmp_path):
    gone = tmp_path / "gone"
    report = impl.FileDeduplicator().scan([gone, str(gone), tmp_path / "." / "gone"])
    assert len(report.issues) == 1 and report.files_considered == 0


# ---- 逐级缩小 ----

def test_unique_sizes_never_reach_a_hook(tmp_path):
    put(tmp_path, "one", b"a")
    put(tmp_path, "two", b"bb")
    put(tmp_path, "three", b"ccc")
    probe = Probe()
    report = probe.scan([tmp_path])
    assert report.groups == () and report.bytes_hashed == 0
    assert probe.samples == [] and probe.fulls == []


def test_sample_reads_head_then_tail_without_overlap(tmp_path):
    sizes = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 8, 10: 8, 20: 8}  # 文件大小 -> sample_size=4 时读到的字节
    dedup = impl.FileDeduplicator(sample_size=4)
    for size, expected in sizes.items():
        data = bytes(range(size))
        path = put(tmp_path, f"f{size}", data)
        digest, nread = dedup._sample_fingerprint(path, size)
        head = data[:4]
        tail_start = max(len(head), size - 4)
        assert nread == expected == len(head) + len(data[tail_start:]), size
        assert digest == sha(head + data[tail_start:]), size


def test_same_size_different_sample_never_reaches_full_hash(tmp_path):
    put(tmp_path, "a", b"A" * 10 + b"mid" + b"Z" * 10)
    put(tmp_path, "b", b"B" * 10 + b"mid" + b"Z" * 10)
    probe = Probe(sample_size=8)
    report = probe.scan([tmp_path])
    assert report.groups == () and probe.fulls == []
    assert len(probe.samples) == 2
    assert report.bytes_hashed == 2 * 16


def test_same_sample_different_middle_is_caught_by_full_hash(tmp_path):
    a = put(tmp_path, "a", b"HEAD" + b"1" * 20 + b"TAIL")
    b = put(tmp_path, "b", b"HEAD" + b"2" * 20 + b"TAIL")
    c = put(tmp_path, "c", b"HEAD" + b"1" * 20 + b"TAIL")
    probe = Probe(sample_size=4)
    report = probe.scan([tmp_path])
    assert report.groups == (impl.DuplicateGroup(str(a), (str(c),), 28),)
    assert sorted(probe.fulls) == sorted(str(p) for p in (a, b, c))  # b 的抽样与 a、c 相同，所以也被全量哈希


def test_full_hash_is_streamed_with_bounded_memory(tmp_path):
    size = 24 * 1024 * 1024
    path = tmp_path / "big"
    with open(path, "wb") as out:
        for _ in range(size // (1 << 20)):
            out.write(b"\x5a" * (1 << 20))
    dedup = impl.FileDeduplicator()
    tracemalloc.start()
    digest, nread = dedup._full_digest(path)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert nread == size
    assert digest == sha(b"\x5a" * size)
    assert peak < size // 4


def test_empty_files_are_duplicates_of_each_other(tmp_path):
    a = put(tmp_path, "a", b"")
    b = put(tmp_path, "b", b"")
    report = impl.FileDeduplicator().scan([b, a])
    assert report.groups == (impl.DuplicateGroup(str(a), (str(b),), 0),)
    assert report.bytes_hashed == 0 and report.files_considered == 2


def test_hard_links_are_distinct_paths_with_equal_content(tmp_path):
    a = put(tmp_path, "a", b"linked")
    b = tmp_path / "b"
    os.link(a, b)
    report = impl.FileDeduplicator().scan([a, b])
    assert report.groups == (impl.DuplicateGroup(str(a), (str(b),), 6),)


# ---- 碰撞安全 ----

class AlwaysCollides(impl.FileDeduplicator):
    def _sample_fingerprint(self, path, size):
        return "same-sample", 1

    def _full_digest(self, path):
        return "same-digest", 2


def test_digest_collision_is_split_into_exact_groups(tmp_path):
    names = {"a": b"one", "b": b"two", "c": b"one", "d": b"two", "e": b"six", "f": b"one"}
    paths = {n: put(tmp_path, n, data) for n, data in names.items()}
    report = AlwaysCollides().scan(list(paths.values()))
    assert report.groups == (
        impl.DuplicateGroup(str(paths["a"]), (str(paths["c"]), str(paths["f"])), 3),
        impl.DuplicateGroup(str(paths["b"]), (str(paths["d"]),), 3),
    )  # e 与谁都不同：不成组，也不是问题
    assert report.issues == ()
    assert report.bytes_hashed == 6 * (1 + 2)


def test_collision_with_a_changed_file_still_compares_bytes(tmp_path):
    class Changer(AlwaysCollides):
        def _full_digest(self, path):
            if path.name == "b":
                path.write_bytes(b"changed")  # 哈希之后内容变了；长度也变
            return super()._full_digest(path)

    a = put(tmp_path, "a", b"abc")
    b = put(tmp_path, "b", b"abc")
    c = put(tmp_path, "c", b"abc")
    report = Changer().scan([a, b, c])
    assert report.groups == (impl.DuplicateGroup(str(a), (str(c),), 3),)


# ---- 失败隔离与记账 ----

def test_sample_failure_is_isolated_and_counts_zero_bytes(tmp_path):
    a = put(tmp_path, "a", b"xx" * 8)
    b = put(tmp_path, "b", b"xx" * 8)
    c = put(tmp_path, "c", b"yy" * 8)
    d = put(tmp_path, "d", b"yy" * 8)
    probe = Probe(sample_size=4, fail_sample=[a])
    report = probe.scan([a, b, c, d])
    assert report.groups == (impl.DuplicateGroup(str(c), (str(d),), 16),)
    assert [i.path for i in report.issues] == [str(a)]
    assert "sample boom" in report.issues[0].error
    assert report.files_considered == 4
    assert str(b) in probe.samples and str(b) not in probe.fulls  # 抽样时 b 的伙伴失败了，它独自留下：不再读
    sample_bytes = 3 * 8  # b、c、d 各读了 4 + 4 字节；a 抛了异常，不计
    full_bytes = 2 * 16
    assert report.bytes_hashed == sample_bytes + full_bytes


def test_full_hash_failure_keeps_the_other_group_and_counts_zero(tmp_path):
    a = put(tmp_path, "a", b"aa")
    b = put(tmp_path, "b", b"aa")
    c = put(tmp_path, "c", b"bbb")
    d = put(tmp_path, "d", b"bbb")
    probe = Probe(fail_full=[b])
    report = probe.scan([a, b, c, d])
    assert report.groups == (impl.DuplicateGroup(str(c), (str(d),), 3),)
    assert [i.path for i in report.issues] == [str(b)]
    assert "hash boom" in report.issues[0].error
    assert report.bytes_hashed == 2 + 2 + 3 + 3 + 2 + 3 + 3  # 四次抽样，全量只有 a、c、d 成功


def test_metadata_failure_in_one_root_does_not_stop_the_rest(tmp_path):
    a = put(tmp_path, "a", b"hello")
    b = put(tmp_path, "b", b"hello")
    report = impl.FileDeduplicator().scan([tmp_path / "nope" / "deeper", a, b])
    assert len(report.issues) == 1 and report.groups[0].canonical == str(a)


def test_exact_compare_failure_is_blamed_on_the_path_that_failed(tmp_path):
    class Deleter(impl.FileDeduplicator):
        def _full_digest(self, path):
            result = super()._full_digest(path)
            if path.name == "c":
                for p in path.parent.glob("c"):
                    p.unlink()  # 哈希完成之后消失：比较时才发现
            return result

    a = put(tmp_path, "a", b"same")
    b = put(tmp_path, "b", b"same")
    c = put(tmp_path, "c", b"same")
    report = Deleter().scan([a, b, c])
    assert report.groups == (impl.DuplicateGroup(str(a), (str(b),), 4),)
    assert [i.path for i in report.issues] == [str(c)]


def test_unreadable_representative_hands_over_to_the_next_member(tmp_path):
    class DeleteFirst(impl.FileDeduplicator):
        def _full_digest(self, path):
            result = super()._full_digest(path)
            if path.name == "a":
                path.unlink()
            return result

    a = put(tmp_path, "a", b"same")
    b = put(tmp_path, "b", b"same")
    c = put(tmp_path, "c", b"same")
    report = DeleteFirst().scan([a, b, c])
    assert report.groups == (impl.DuplicateGroup(str(b), (str(c),), 4),)  # a 是最小路径，但它读不了
    assert [i.path for i in report.issues] == [str(a)]


def test_verification_reads_are_not_counted(tmp_path):
    a = put(tmp_path, "a", b"q" * 100)
    b = put(tmp_path, "b", b"q" * 100)
    report = impl.FileDeduplicator(sample_size=10).scan([a, b])
    assert report.bytes_hashed == 2 * 20 + 2 * 100


def test_groups_duplicates_and_issues_are_sorted_by_string(tmp_path):
    names = ["b", "B", "a", "_z", "a.txt"]
    for n in names:
        put(tmp_path, n, b"all-the-same")
    report = impl.FileDeduplicator().scan([tmp_path / n for n in names] + [tmp_path / "zz", tmp_path / "Zz"])
    order = sorted(str(tmp_path / n) for n in names)
    assert report.groups == (impl.DuplicateGroup(order[0], tuple(order[1:]), 12),)
    assert [i.path for i in report.issues] == [str(tmp_path / "Zz"), str(tmp_path / "zz")]


def test_ordering_is_by_string_not_by_path_components(tmp_path):
    dot = put(tmp_path, "a.txt", b"twin")
    nested = put(tmp_path, "a/b", b"twin")
    report = impl.FileDeduplicator().scan([nested, dot])
    assert str(dot) < str(nested) and sorted([nested, dot]) == [nested, dot]  # 两种排法确实不同
    assert report.groups == (impl.DuplicateGroup(str(dot), (str(nested),), 4),)


# ---- 并发 ----

class Gate(impl.FileDeduplicator):
    """前 max_workers 个钩子互相等待：只有同时跑起这么多个才能放行；另外记录同时活动的最大数。"""

    def __init__(self, workers, **kw):
        super().__init__(workers, **kw)
        self.lock = threading.Lock()
        self.active = self.peak = self.entered = 0
        self.barrier = threading.Barrier(workers)

    def _enter(self):
        with self.lock:
            self.active += 1
            self.peak = max(self.peak, self.active)
            self.entered += 1
            first_wave = self.entered <= self.max_workers
        if first_wave:
            self.barrier.wait(timeout=10)

    def _leave(self):
        with self.lock:
            self.active -= 1

    def _sample_fingerprint(self, path, size):
        self._enter()
        try:
            return super()._sample_fingerprint(path, size)
        finally:
            self._leave()

    def _full_digest(self, path):
        self._enter()
        try:
            return super()._full_digest(path)
        finally:
            self._leave()


@pytest.mark.parametrize("workers", [1, 2, 3])
def test_hooks_run_exactly_max_workers_at_once(tmp_path, workers):
    paths = []
    for g in range(4):  # 四个大小各两个相同文件：八个抽样钩子都符合条件
        for k in range(2):
            paths.append(put(tmp_path, f"g{g}f{k}", bytes([g]) * (10 + g)))
    gate = Gate(workers, sample_size=4)
    report = gate.scan(paths)
    assert gate.peak == workers  # 屏障保证至少 workers 个同时在；线程池保证不会更多
    assert len(report.groups) == 4


def test_stages_overlap_a_slow_sample_does_not_hold_back_other_groups_full_hash(tmp_path):
    """大小组 X 的一个抽样钩子一直等到别的组的全量哈希开始：阶段若是整体分批，就会等到超时。"""
    started = threading.Event()

    class Overlap(impl.FileDeduplicator):
        def _sample_fingerprint(self, path, size):
            if path.name == "x1":
                assert started.wait(timeout=10), "full hash of another group never started"
            return super()._sample_fingerprint(path, size)

        def _full_digest(self, path):
            started.set()
            return super()._full_digest(path)

    x1 = put(tmp_path, "x1", b"xxxx")
    x2 = put(tmp_path, "x2", b"xxxx")
    y1 = put(tmp_path, "y1", b"yyyyy")
    y2 = put(tmp_path, "y2", b"yyyyy")
    report = Overlap(max_workers=3).scan([x1, x2, y1, y2])
    assert len(report.groups) == 2


def test_concurrent_scans_on_one_instance_do_not_interfere(tmp_path):
    for i in range(6):
        put(tmp_path, f"f{i}", b"same-bytes" if i % 2 else b"other-data")
    dedup = impl.FileDeduplicator(max_workers=3)
    expected = dedup.scan([tmp_path])
    results: list[object] = []
    start = threading.Barrier(4)

    def run():
        start.wait()
        results.append(dedup.scan([tmp_path]))

    threads = [threading.Thread(target=run) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results == [expected] * 4


# ---- 与暴力参照对拍 ----

def reference(paths):
    by_content: dict[bytes, list[str]] = {}
    for p in sorted({str(Path(x)) for x in paths}):
        by_content.setdefault(Path(p).read_bytes(), []).append(p)
    return [(v[0], tuple(v[1:]), len(k)) for k, v in sorted(by_content.items(), key=lambda kv: kv[1][0]) if len(v) > 1]


@pytest.mark.parametrize("seed", range(8))
@pytest.mark.parametrize("workers", [1, 5])
def test_random_trees_match_brute_force_for_any_worker_count(tmp_path, seed, workers):
    rng = random.Random(seed)
    pool = [bytes(rng.randrange(3) for _ in range(rng.choice([0, 1, 7, 8, 9, 17, 40]))) for _ in range(9)]
    made = []
    for i in range(30):
        made.append(put(tmp_path, f"d{rng.randrange(4)}/n{i}", rng.choice(pool)))
    report = impl.FileDeduplicator(workers, sample_size=8).scan([tmp_path, made[0], str(made[3])])
    got = [(g.canonical, g.duplicates, g.size) for g in report.groups]
    assert got == reference(made)
    assert report.files_considered == len(made) and report.issues == ()
