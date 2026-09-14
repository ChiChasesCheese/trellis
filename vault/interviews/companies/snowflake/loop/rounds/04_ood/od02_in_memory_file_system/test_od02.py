import random
import re
import threading

import pytest

EX1 = [
    "MKDIR /a/b/c",
    "ADD /a/b/c/d hello",
    "LS /",
    "LS /a/b/c",
    "READ /a/b/c/d",
    "ADD /a/b/c/d world",
    "READ /a/b/c/d",
]
EX1_OUT = ["['a']", "['d']", "hello", "helloworld"]

EX2 = [
    "MKDIR /x",
    "ADD /x/f hi",
    "RM /x",
    "RMDIR /x/f",
    "RMDIR /x",
    "RM /x/f",
    "RMDIR /x",
    "LS /",
]
EX2_OUT = ["ERROR:IsADirectoryError", "ERROR:NotADirectoryError", "ERROR:OSError", "[]"]

EX3 = ["MKDIR /d", "ADD /d/big aaaa", "ADD /d/big bbbb", "SIZE /d/big", "READ /d/big"]
EX3_OUT = ["8", "aaaabbbb"]


# ------------------------------------------------------------------ Part 1: LC 588 base API
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.part1(EX1) == EX1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_ls_root_empty_initially(impl):
    fs = impl.FileSystem()
    assert fs.ls("/") == []


@pytest.mark.part1
@pytest.mark.edge
def test_mkdir_existing_dir_is_noop(impl):
    fs = impl.FileSystem()
    fs.mkdir("/a")
    fs.mkdir("/a")  # must not raise
    assert fs.ls("/") == ["a"]


@pytest.mark.part1
@pytest.mark.edge
def test_mkdir_existing_file_raises(impl):
    fs = impl.FileSystem()
    fs.mkdir("/a")
    fs.add_content_to_file("/a/f", "x")
    with pytest.raises(FileExistsError):
        fs.mkdir("/a/f")


@pytest.mark.part1
@pytest.mark.edge
def test_add_content_missing_parent_raises_not_auto_created(impl):
    fs = impl.FileSystem()
    with pytest.raises(FileNotFoundError):
        fs.add_content_to_file("/no/such/dir/f", "x")


@pytest.mark.part1
@pytest.mark.edge
def test_add_content_empty_string_is_legal_noop(impl):
    fs = impl.FileSystem()
    fs.add_content_to_file("/f", "")
    assert fs.read_content_from_file("/f") == ""


@pytest.mark.part1
@pytest.mark.edge
def test_read_missing_or_directory_raises(impl):
    fs = impl.FileSystem()
    with pytest.raises(FileNotFoundError):
        fs.read_content_from_file("/ghost")
    fs.mkdir("/d")
    with pytest.raises(IsADirectoryError):
        fs.read_content_from_file("/d")


@pytest.mark.part1
def test_ls_file_returns_basename_only(impl):
    fs = impl.FileSystem()
    fs.add_content_to_file("/f", "hello")
    assert fs.ls("/f") == ["f"]


# ------------------------------------------------------------------ Part 2: rm / rmdir
@pytest.mark.part2
def test_worked_example_2(impl):
    assert impl.part2(EX2) == EX2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_root_cannot_be_removed(impl):
    fs = impl.FileSystem()
    with pytest.raises(PermissionError):
        fs.rm("/")
    with pytest.raises(PermissionError):
        fs.rmdir("/")


@pytest.mark.part2
@pytest.mark.edge
def test_rm_missing_raises(impl):
    fs = impl.FileSystem()
    with pytest.raises(FileNotFoundError):
        fs.rm("/ghost")
    with pytest.raises(FileNotFoundError):
        fs.rmdir("/ghost")


@pytest.mark.part2
def test_rmdir_empty_dir_succeeds(impl):
    fs = impl.FileSystem()
    fs.mkdir("/a")
    fs.rmdir("/a")
    assert fs.ls("/") == []


# ------------------------------------------------------------------ Part 3: chunked storage
@pytest.mark.part3
def test_worked_example_3(impl):
    assert impl.part3(EX3) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_size_matches_sum_of_appended_chunks(impl):
    fs = impl.FileSystem()
    fs.add_content_to_file("/f", "ab")
    fs.add_content_to_file("/f", "cde")
    fs.add_content_to_file("/f", "")
    assert fs.size("/f") == 5
    assert fs.read_content_from_file("/f") == "abcde"


@pytest.mark.part3
@pytest.mark.edge
def test_size_missing_or_directory_raises(impl):
    fs = impl.FileSystem()
    with pytest.raises(FileNotFoundError):
        fs.size("/ghost")
    fs.mkdir("/d")
    with pytest.raises(IsADirectoryError):
        fs.size("/d")


@pytest.mark.part3
@pytest.mark.perf
def test_perf_many_small_appends_no_quadratic_blowup(impl):
    import time

    fs = impl.FileSystem()
    n, chunk = 20_000, "x" * 50
    t0 = time.perf_counter()
    for _ in range(n):
        fs.add_content_to_file("/big", chunk)
    elapsed = time.perf_counter() - t0
    assert fs.size("/big") == n * len(chunk)
    assert elapsed < 2.0, f"too slow (likely O(n^2) string concat): {elapsed:.2f}s"


# ------------------------------------------------------------------ Part 4: per-path locking
@pytest.mark.part4
def test_concurrent_appends_to_same_file_lose_nothing_and_keep_per_thread_order(impl):
    fs = impl.FileSystem()
    n_threads, n_writes = 20, 50

    def worker(tid: int):
        for i in range(n_writes):
            fs.add_content_to_file("/shared", f"[{tid}-{i}]")

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    content = fs.read_content_from_file("/shared")
    tokens = re.findall(r"\[(\d+)-(\d+)\]", content)
    assert len(tokens) == n_threads * n_writes  # no lost updates
    by_thread: dict[int, list[int]] = {}
    for tid_s, i_s in tokens:
        by_thread.setdefault(int(tid_s), []).append(int(i_s))
    assert len(by_thread) == n_threads
    for tid, seq in by_thread.items():
        assert seq == list(range(n_writes)), f"thread {tid} out of order: {seq}"


@pytest.mark.part4
@pytest.mark.edge
def test_concurrent_appends_to_different_files_all_land(impl):
    fs = impl.FileSystem()
    fs.mkdir("/d")
    n_files = 30

    def worker(i: int):
        fs.add_content_to_file(f"/d/f{i}", f"content-{i}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_files)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=15)

    assert sorted(fs.ls("/d")) == sorted(f"f{i}" for i in range(n_files))
    for i in range(n_files):
        assert fs.read_content_from_file(f"/d/f{i}") == f"content-{i}"


# ------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_ls_output_is_python_list_repr(impl):
    out = impl.part1(["MKDIR /a", "MKDIR /b", "LS /"])
    assert out == ["['a', 'b']"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 1\n" + "\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n" + "\n".join(EX2) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX2_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.edge
def test_add_content_double_space_preserves_leading_space(run_script):
    r = run_script("PART 1\n" + "\n".join(["ADD /f  world", "READ /f"]) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == [" world"]
