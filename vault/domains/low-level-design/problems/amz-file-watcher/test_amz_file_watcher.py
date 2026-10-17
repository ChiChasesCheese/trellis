import importlib
import os
import threading

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))
K = impl.EventKind


class FakeFS:
    """内存里的文件系统：测试自己决定每个文件的 mtime 与 size，没有真实磁盘、没有真实时钟。"""

    def __init__(self):
        self.files: dict[str, impl.Stat] = {}
        self.scans = 0
        self.root_exists = True

    def put(self, path, mtime=1, size=1):
        self.files[path] = impl.Stat(mtime, size)

    def remove(self, path):
        del self.files[path]

    def scan(self, root, recursive):
        self.scans += 1
        if not self.root_exists:
            raise impl.RootNotFoundError(root)
        if recursive:
            return dict(self.files)
        return {p: s for p, s in self.files.items() if "/" not in p}


def watch(fs=None, **kw):
    fs = fs or FakeFS()
    w = impl.Watcher(fs, "/data", **kw)
    seen = []
    w.subscribe(seen.append)
    return fs, w, seen


def pairs(events):
    return [(e.kind.name, e.path) for e in events]


# ---- 第 1 关：快照比对 ----

def test_diff_is_a_pure_function_of_two_snapshots():
    old = {"a": impl.Stat(1, 1), "b": impl.Stat(1, 1), "c": impl.Stat(1, 1)}
    new = {"b": impl.Stat(2, 1), "c": impl.Stat(1, 1), "d": impl.Stat(5, 5)}
    assert pairs(impl.diff(old, new)) == [("DELETED", "a"), ("MODIFIED", "b"), ("CREATED", "d")]


def test_first_poll_only_takes_the_baseline():
    fs, w, seen = watch()
    fs.put("existing.txt")
    assert w.poll() == [] and seen == []
    assert w.poll() == []


def test_created_modified_deleted_are_reported_once_each():
    fs, w, seen = watch()
    w.poll()
    fs.put("a.txt")
    assert pairs(w.poll()) == [("CREATED", "a.txt")]
    fs.put("a.txt", mtime=2)
    assert pairs(w.poll()) == [("MODIFIED", "a.txt")]
    fs.remove("a.txt")
    assert pairs(w.poll()) == [("DELETED", "a.txt")]
    assert w.poll() == []
    assert pairs(seen) == [("CREATED", "a.txt"), ("MODIFIED", "a.txt"), ("DELETED", "a.txt")]


def test_an_edit_in_the_same_mtime_tick_is_caught_when_the_size_changes():
    fs, w, _ = watch()
    fs.put("log.txt", mtime=100, size=10)
    w.poll()
    fs.put("log.txt", mtime=100, size=25)  # 时间粒度太粗，mtime 没变
    assert pairs(w.poll()) == [("MODIFIED", "log.txt")]


def test_unchanged_files_produce_no_events():
    fs, w, _ = watch()
    for name in "abc":
        fs.put(name)
    w.poll()
    assert w.poll() == [] and w.poll() == []


def test_rename_shows_up_as_a_delete_plus_a_create():
    fs, w, _ = watch()
    fs.put("old.txt", 5, 5)
    w.poll()
    fs.remove("old.txt")
    fs.put("new.txt", 5, 5)
    assert pairs(w.poll()) == [("CREATED", "new.txt"), ("DELETED", "old.txt")]


def test_missing_root_is_an_error_on_poll():
    fs, w, _ = watch()
    fs.root_exists = False
    with pytest.raises(impl.RootNotFoundError):
        w.poll()


# ---- 第 2 关：订阅、过滤、递归 ----

def test_subscribers_can_filter_by_kind_and_unsubscribe():
    fs, w, seen = watch()
    only_deletes, unsub = [], None
    unsub = w.subscribe(only_deletes.append, kinds=[K.DELETED])
    w.poll()
    fs.put("a")
    w.poll()
    fs.remove("a")
    w.poll()
    assert pairs(only_deletes) == [("DELETED", "a")]
    unsub()
    unsub()  # 重复取消是无害的
    fs.put("b")
    w.poll()
    fs.remove("b")
    w.poll()
    assert len(only_deletes) == 1 and len(seen) == 4


def test_include_filter_hides_files_from_every_stage():
    fs, w, seen = watch(include=lambda p: p.endswith(".py"))
    w.poll()
    fs.put("a.py")
    fs.put("a.pyc")
    fs.put("notes.txt")
    w.poll()
    assert pairs(seen) == [("CREATED", "a.py")]


def test_recursive_flag_decides_whether_subdirectories_are_watched():
    fs = FakeFS()
    _, deep, deep_seen = watch(fs)
    _, flat, flat_seen = watch(fs, recursive=False)
    deep.poll()
    flat.poll()
    fs.put("top.txt")
    fs.put("sub/inner.txt")
    deep.poll()
    flat.poll()
    assert pairs(deep_seen) == [("CREATED", "sub/inner.txt"), ("CREATED", "top.txt")]
    assert pairs(flat_seen) == [("CREATED", "top.txt")]


def test_a_failing_callback_is_recorded_and_does_not_stop_the_others():
    fs, w, seen = watch()
    boom = RuntimeError("boom")

    def bad(event):
        raise boom

    w.subscribe(bad)
    later = []
    w.subscribe(later.append)
    w.poll()
    fs.put("a")
    w.poll()
    assert len(seen) == len(later) == 1
    assert [f.error for f in w.failures] == [boom] and w.failures[0].event.path == "a"
    fs.put("b")
    assert pairs(w.poll()) == [("CREATED", "b")]  # 监听器仍在工作


def test_failure_log_is_bounded():
    fs, w, _ = watch()
    w.subscribe(lambda e: 1 / 0)
    w.poll()
    for i in range(250):
        fs.put(f"f{i}")
    w.poll()
    assert 0 < len(w.failures) <= 100


def test_callback_may_subscribe_without_deadlock():
    fs, w, _ = watch()
    extra = []
    w.subscribe(lambda e: w.subscribe(extra.append))
    w.poll()
    fs.put("a")
    w.poll()
    fs.put("b")
    w.poll()
    assert pairs(extra) == [("CREATED", "b")]


# ---- 第 3 关：去抖 ----

def test_settle_waits_until_two_polls_agree():
    fs, w, seen = watch(settle=True)
    w.poll()
    fs.put("big.bin", 1, 10)
    assert w.poll() == []  # 刚出现，还不稳定
    fs.put("big.bin", 2, 500)  # 还在写
    assert w.poll() == []
    assert pairs(w.poll()) == [("CREATED", "big.bin")]  # 连续两轮相同
    assert w.poll() == []
    assert len(seen) == 1


def test_settle_collapses_a_burst_of_writes_into_one_modified():
    fs, w, seen = watch(settle=True)
    fs.put("doc", 1, 1)
    w.poll()
    for i in range(2, 8):
        fs.put("doc", i, i)
        assert w.poll() == []
    assert pairs(w.poll()) == [("MODIFIED", "doc")]
    assert len(seen) == 1


def test_settle_never_reports_a_file_that_came_and_went_between_polls():
    fs, w, seen = watch(settle=True)
    w.poll()
    fs.put("tmp~")
    w.poll()
    fs.remove("tmp~")
    w.poll()
    w.poll()
    assert seen == []


def test_settle_reports_a_delete_only_after_it_stays_deleted():
    fs, w, seen = watch(settle=True)
    fs.put("a")
    w.poll()
    fs.remove("a")
    assert w.poll() == []
    assert pairs(w.poll()) == [("DELETED", "a")]


# ---- 真实磁盘：tmp_path + 显式 poll + 显式 mtime，不依赖时间流逝 ----

def test_disk_file_system_sees_real_files_recursively(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.txt").write_text("hi")
    (tmp_path / "sub" / "b.txt").write_text("hello")
    fs = impl.DiskFileSystem()
    snap = fs.scan(str(tmp_path), True)
    assert set(snap) == {"a.txt", "sub/b.txt"} and snap["sub/b.txt"].size == 5
    assert set(fs.scan(str(tmp_path), False)) == {"a.txt"}


def test_watcher_on_a_real_directory_with_explicit_mtimes(tmp_path):
    w = impl.Watcher(impl.DiskFileSystem(), str(tmp_path))
    seen = []
    w.subscribe(seen.append)
    w.poll()
    target = tmp_path / "f.txt"
    target.write_text("one")
    os.utime(target, ns=(1_000_000_000, 1_000_000_000))
    assert pairs(w.poll()) == [("CREATED", "f.txt")]
    os.utime(target, ns=(2_000_000_000, 2_000_000_000))  # 内容不变，只有时间变
    assert pairs(w.poll()) == [("MODIFIED", "f.txt")]
    target.unlink()
    assert pairs(w.poll()) == [("DELETED", "f.txt")]


def test_disk_file_system_does_not_follow_symlink_loops(tmp_path):
    (tmp_path / "d").mkdir()
    (tmp_path / "d" / "x.txt").write_text("x")
    os.symlink(tmp_path, tmp_path / "d" / "loop")
    assert set(impl.DiskFileSystem().scan(str(tmp_path), True)) == {"d/x.txt"}


def test_disk_file_system_rejects_a_missing_root(tmp_path):
    with pytest.raises(impl.RootNotFoundError):
        impl.DiskFileSystem().scan(str(tmp_path / "nope"), True)


# ---- 第 4 关：后台线程与关闭（用 Event 同步，不睡眠）----

def test_background_thread_polls_and_stop_ends_it():
    fs, w, seen = watch()
    w.poll()
    got = threading.Event()
    w.subscribe(lambda e: got.set())
    fs.put("a")
    w.start(interval=0.001)
    assert w.running
    assert got.wait(timeout=10)
    w.stop()
    assert not w.running
    assert pairs(seen) == [("CREATED", "a")]


def test_start_twice_is_harmless_and_restart_after_stop_works():
    fs, w, seen = watch()
    w.poll()
    w.start(0.001)
    w.start(0.001)
    w.stop()
    assert not w.running
    got = threading.Event()
    w.subscribe(lambda e: got.set())
    fs.put("late")
    w.start(0.001)
    assert got.wait(timeout=10)
    w.stop()
    assert not w.running
    assert pairs(seen) == [("CREATED", "late")]


def test_stop_called_from_inside_a_callback_neither_hangs_nor_fails():
    fs, w, _ = watch()
    w.poll()
    after_stop = threading.Event()

    def stopper(event):
        w.stop()  # 在轮询线程自己里调用：不能 join 自己
        after_stop.set()

    w.subscribe(stopper)
    fs.put("a")
    w.start(interval=0.001)
    assert after_stop.wait(timeout=10)
    w.stop()  # 主线程再 stop 一次：等线程真正退出
    assert not w.running
    assert w.failures == ()


def test_a_missing_root_does_not_kill_the_polling_thread():
    fs, w, seen = watch()
    w.poll()
    fs.root_exists = False
    w.start(0.001)
    while fs.scans < 5:  # 让线程至少撞上几次错误
        pass
    fs.root_exists = True
    got = threading.Event()
    w.subscribe(lambda e: got.set())
    fs.put("back")
    assert got.wait(timeout=10)
    w.stop()
    assert w.running is False
