"""内存文件系统的验收测试：`IMPL=solution` 全绿，`IMPL=starter` 全红。

所有断言只通过公开方法（`mkdir`/`ls`/`add_file`/`read_file`/`remove`/`move`/`copy`/
`size`/`find`/`snapshot`/`restore`），不触碰任何私有方法或属性——内部要不要有父指针、
要不要给节点存名字，换一种实现照样能过。
"""

from __future__ import annotations

import importlib
import os

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def _fs() -> "impl.FileSystem":
    return impl.FileSystem()


# ---------- 第 1 关：目录树与路径解析 ----------

def test_mkdir_creates_intermediate_directories() -> None:
    fs = _fs()
    fs.mkdir("/a/b/c")
    assert fs.ls("/a") == ["b"]
    assert fs.ls("/a/b") == ["c"]
    assert fs.ls("/a/b/c") == []


def test_ls_returns_sorted_entries() -> None:
    fs = _fs()
    for name in ["zeta", "alpha", "mu"]:
        fs.mkdir(f"/{name}")
    assert fs.ls("/") == ["alpha", "mu", "zeta"]


def test_add_file_and_read_file_round_trip() -> None:
    fs = _fs()
    fs.mkdir("/docs")
    fs.add_file("/docs/readme.md", b"hello")
    assert fs.read_file("/docs/readme.md") == b"hello"
    fs.add_file("/docs/readme.md", b"world")  # 覆盖
    assert fs.read_file("/docs/readme.md") == b"world"


def test_path_must_be_absolute() -> None:
    fs = _fs()
    with pytest.raises(impl.InvalidPathError):
        fs.mkdir("relative/path")


def test_trailing_slash_and_dot_segments_are_ignored() -> None:
    fs = _fs()
    fs.mkdir("/a/b/")
    fs.add_file("/a/./b/../b/file.txt", b"x")
    assert fs.read_file("/a/b/file.txt") == b"x"


def test_dotdot_escaping_root_raises() -> None:
    fs = _fs()
    with pytest.raises(impl.PathEscapesRootError):
        fs.ls("/..")
    with pytest.raises(impl.PathEscapesRootError):
        fs.ls("/a/../..")


def test_add_file_requires_existing_parent_directory() -> None:
    fs = _fs()
    with pytest.raises(impl.PathNotFoundError):
        fs.add_file("/no/such/dir/file.txt", b"x")


def test_mkdir_over_existing_file_raises() -> None:
    fs = _fs()
    fs.add_file("/a", b"x")
    with pytest.raises(impl.ExpectedDirectoryError):
        fs.mkdir("/a/b")


def test_mkdir_is_idempotent_like_mkdir_dash_p() -> None:
    fs = _fs()
    fs.mkdir("/a/b")
    fs.mkdir("/a/b")  # 已经存在，安静地成功
    assert fs.ls("/a") == ["b"]


def test_read_file_on_a_directory_raises() -> None:
    fs = _fs()
    fs.mkdir("/a")
    with pytest.raises(impl.ExpectedFileError):
        fs.read_file("/a")


# ---------- 第 2 关：删除、移动、复制、体积 ----------

def test_remove_non_recursive_on_nonempty_directory_raises() -> None:
    fs = _fs()
    fs.mkdir("/a/b")
    with pytest.raises(impl.DirectoryNotEmptyError):
        fs.remove("/a")


def test_remove_recursive_deletes_whole_subtree() -> None:
    fs = _fs()
    fs.mkdir("/a/b/c")
    fs.add_file("/a/b/file.txt", b"x")
    fs.remove("/a", recursive=True)
    with pytest.raises(impl.PathNotFoundError):
        fs.ls("/a")
    assert fs.ls("/") == []


def test_move_renames_and_relocates() -> None:
    fs = _fs()
    fs.mkdir("/a")
    fs.add_file("/a/file.txt", b"content")
    fs.mkdir("/b")
    fs.move("/a/file.txt", "/b/renamed.txt")
    assert fs.ls("/a") == []
    assert fs.read_file("/b/renamed.txt") == b"content"


def test_move_into_own_subtree_raises_without_losing_data() -> None:
    fs = _fs()
    fs.mkdir("/a/b")
    with pytest.raises(impl.InvalidPathError):
        fs.move("/a", "/a/b/c")
    # 失败之后原树必须原封不动——这是一次真正会造成数据丢失（甚至造出环）的失败路径
    assert fs.ls("/") == ["a"]
    assert fs.ls("/a") == ["b"]


def test_move_to_an_already_occupied_destination_raises_and_keeps_source() -> None:
    fs = _fs()
    fs.add_file("/a.txt", b"a")
    fs.add_file("/b.txt", b"b")
    with pytest.raises(impl.PathAlreadyExistsError):
        fs.move("/a.txt", "/b.txt")
    assert fs.read_file("/a.txt") == b"a"
    assert fs.read_file("/b.txt") == b"b"


def test_copy_file_is_independent_of_the_original() -> None:
    fs = _fs()
    fs.add_file("/a.txt", b"original")
    fs.copy("/a.txt", "/b.txt")
    fs.add_file("/a.txt", b"changed")  # 整体覆盖原文件
    assert fs.read_file("/b.txt") == b"original"  # 复制出来的那份不受影响


def test_copy_directory_deep_duplicates_so_mutation_is_isolated() -> None:
    fs = _fs()
    fs.mkdir("/a")
    fs.add_file("/a/f.txt", b"1")
    fs.copy("/a", "/b")
    fs.add_file("/b/new.txt", b"2")  # 只改复制出来的那一份
    assert fs.ls("/a") == ["f.txt"]  # 原目录不受影响——不是共享了同一张 entries 表
    assert fs.ls("/b") == ["f.txt", "new.txt"]


def test_size_sums_subtree_bytes() -> None:
    fs = _fs()
    fs.mkdir("/a/b")
    fs.add_file("/a/one.txt", b"12345")
    fs.add_file("/a/b/two.txt", b"1234567890")
    assert fs.size("/a/one.txt") == 5
    assert fs.size("/a/b") == 10
    assert fs.size("/a") == 15


# ---------- 第 3 关：搜索 ----------

def test_find_matches_by_glob_across_the_tree() -> None:
    fs = _fs()
    fs.mkdir("/a/b")
    fs.add_file("/a/report.txt", b"x")
    fs.add_file("/a/b/summary.txt", b"y")
    fs.add_file("/a/b/data.csv", b"z")
    assert fs.find("*.txt") == ["/a/b/summary.txt", "/a/report.txt"]
    assert fs.find("*.csv") == ["/a/b/data.csv"]
    assert fs.find("no-match-*") == []


# ---------- 第 4 关：快照与恢复 ----------

def test_snapshot_and_restore_round_trip() -> None:
    fs = _fs()
    fs.mkdir("/a")
    fs.add_file("/a/f.txt", b"before")
    snap = fs.snapshot()
    fs.remove("/a", recursive=True)
    fs.add_file("/g.txt", b"unrelated")
    assert fs.ls("/") == ["g.txt"]
    fs.restore(snap)
    assert fs.ls("/") == ["a"]
    assert fs.read_file("/a/f.txt") == b"before"


def test_restoring_does_not_let_later_mutation_leak_back_into_the_snapshot() -> None:
    fs = _fs()
    fs.mkdir("/a")
    snap = fs.snapshot()
    fs.restore(snap)
    fs.add_file("/new.txt", b"x")  # 恢复之后继续修改当前树
    fs.restore(snap)  # 再恢复同一个快照
    assert fs.ls("/") == ["a"]  # 上一次恢复之后的修改不会沾到这个快照身上
