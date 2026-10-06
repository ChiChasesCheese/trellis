import builtins
import os
import tempfile
import time
import tracemalloc

import pytest


def put(root, rel, data=b"", mtime=None):
    p = os.path.join(str(root), rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode())
    if mtime is not None:
        os.utime(p, (mtime, mtime))
    return p


def rel(root, groups):
    return [[os.path.relpath(p, str(root)) for p in g] for g in groups]


def collide_pair(root, a="a.bin", b="b.bin", head=1024, tail=64):
    """Two files: same size, same first 1 KiB, different tail -> _calculate_hash collides."""
    prefix = b"\x07" * head
    put(root, a, prefix + b"A" * tail)
    put(root, b, prefix + b"B" * tail)


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_part1_worked_example_line_driven(impl):
    lines = [
        "FILE a/x.jpg cat", "FILE b/y.jpg cat", "FILE c/z.jpg dog", "FILE d/w.jpg cat",
        "FILE e/e1.jpg", "FILE e/e2.jpg", "LINK f/l.jpg a/x.jpg", "FILE g/u.jpg lonely",
    ]
    assert impl.part1(lines) == ["a/x.jpg b/y.jpg d/w.jpg", "e/e1.jpg e/e2.jpg"]


@pytest.mark.part1
def test_find_duplicates_basic_groups_and_ordering(impl, tmp_path):
    put(tmp_path, "z/two.txt", "same")
    put(tmp_path, "a/one.txt", "same")
    put(tmp_path, "m/other1.txt", "other")
    put(tmp_path, "b/other2.txt", "other")
    put(tmp_path, "solo.txt", "unique!")
    got = rel(tmp_path, impl.find_duplicates(str(tmp_path)))
    # paths sorted inside a group, groups sorted by first path
    assert got == [["a/one.txt", "z/two.txt"], ["b/other2.txt", "m/other1.txt"]]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_root_and_no_duplicates(impl, tmp_path):
    assert impl.find_duplicates(str(tmp_path)) == []
    put(tmp_path, "a", "1")
    put(tmp_path, "b", "22")
    assert impl.find_duplicates(str(tmp_path)) == []


@pytest.mark.part1
@pytest.mark.edge
def test_empty_files_are_duplicates_of_each_other(impl, tmp_path):
    put(tmp_path, "e1")
    put(tmp_path, "sub/e2")
    put(tmp_path, "full", "x")
    assert rel(tmp_path, impl.find_duplicates(str(tmp_path))) == [["e1", os.path.join("sub", "e2")]]


@pytest.mark.part1
@pytest.mark.edge
def test_symlinks_are_not_followed_or_counted(impl, tmp_path):
    put(tmp_path, "real/a.txt", "payload")
    os.symlink(str(tmp_path / "real" / "a.txt"), str(tmp_path / "file_link.txt"))
    os.symlink(str(tmp_path / "real"), str(tmp_path / "dir_link"))
    os.symlink(str(tmp_path / "does_not_exist"), str(tmp_path / "dangling"))
    # the real file is alone: links to it (file, directory, dangling) are neither walked nor duplicates
    assert impl.find_duplicates(str(tmp_path)) == []
    put(tmp_path, "copy.txt", "payload")
    assert rel(tmp_path, impl.find_duplicates(str(tmp_path))) == [["copy.txt", os.path.join("real", "a.txt")]]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file permissions")
def test_unreadable_file_is_skipped_and_counted(impl, tmp_path):
    put(tmp_path, "a.txt", "dup")
    put(tmp_path, "b.txt", "dup")
    bad = put(tmp_path, "c.txt", "dup")
    os.chmod(bad, 0)
    try:
        res = impl.scan_duplicates(str(tmp_path))
    finally:
        os.chmod(bad, 0o644)
    assert rel(tmp_path, res.groups) == [["a.txt", "b.txt"]]
    assert res.skipped == 1


@pytest.mark.part1
@pytest.mark.edge
def test_unreadable_file_via_vanishing_file_counted(impl, tmp_path):
    # works as root too: the file disappears between size bucketing and reading
    put(tmp_path, "a.txt", "dup")
    put(tmp_path, "b.txt", "dup")
    victim = put(tmp_path, "c.txt", "dup")

    def flaky_hash(path):
        if path == victim:
            raise PermissionError("denied")
        return impl._calculate_hash(path)

    res = impl.scan_duplicates(str(tmp_path), hash_fn=flaky_hash)
    assert rel(tmp_path, res.groups) == [["a.txt", "b.txt"]]
    assert res.skipped == 1


@pytest.mark.part1
def test_unique_size_files_are_never_read(impl, tmp_path, monkeypatch):
    put(tmp_path, "d1.txt", "twelve bytes")
    put(tmp_path, "d2.txt", "twelve bytes")
    lone = put(tmp_path, "lone.txt", "I have a size nobody else has")
    opened = []
    real_open = builtins.open

    def spy(file, *a, **k):
        opened.append(os.fspath(file))
        return real_open(file, *a, **k)

    monkeypatch.setattr(builtins, "open", spy)
    got = impl.find_duplicates(str(tmp_path))
    monkeypatch.undo()
    assert len(got) == 1
    assert lone not in opened


@pytest.mark.part1
@pytest.mark.edge
def test_chunk_size_validation_and_tiny_chunks(impl, tmp_path):
    put(tmp_path, "a", "abcdefghij")
    put(tmp_path, "b", "abcdefghij")
    put(tmp_path, "c", "abcdefghiX")
    for bad in (0, -1):
        with pytest.raises(ValueError):
            impl.find_duplicates(str(tmp_path), chunk_size=bad)
    for cs in (1, 3, 10, 11, 4096):
        assert rel(tmp_path, impl.find_duplicates(str(tmp_path), chunk_size=cs)) == [["a", "b"]]


@pytest.mark.part1
@pytest.mark.perf
def test_large_files_are_streamed_not_slurped(impl, tmp_path):
    blob = os.urandom(4 << 20)
    put(tmp_path, "big1.bin", blob)
    put(tmp_path, "big2.bin", blob)
    put(tmp_path, "big3.bin", blob[:-1] + bytes([blob[-1] ^ 1]))
    tracemalloc.start()
    try:
        got = impl.find_duplicates(str(tmp_path), chunk_size=4096)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert rel(tmp_path, got) == [["big1.bin", "big2.bin"]]
    assert peak < 1 << 20, f"peak {peak} bytes: read the file in chunks, not all at once"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example_line_driven(impl):
    # a.bin and b.bin collide under _calculate_hash (same size, same first KiB) but differ in content
    head = "H" * 1024
    lines = [f"FILE a.bin {head}A", f"FILE b.bin {head}B", f"FILE c.bin {head}A", f"FILE d.bin {head}B"]
    assert impl.part2(lines) == ["a.bin c.bin", "b.bin d.bin"]


@pytest.mark.part2
def test_given_hash_really_collides(impl, tmp_path):
    collide_pair(tmp_path)
    a, b = str(tmp_path / "a.bin"), str(tmp_path / "b.bin")
    assert impl._calculate_hash(a) == impl._calculate_hash(b)
    assert open(a, "rb").read() != open(b, "rb").read()


@pytest.mark.part2
def test_collision_does_not_produce_false_group(impl, tmp_path):
    collide_pair(tmp_path)
    assert impl.find_duplicates_verified(str(tmp_path)) == []


@pytest.mark.part2
def test_collision_bucket_with_real_duplicates_splits_correctly(impl, tmp_path):
    prefix = b"\x07" * 1024
    for name, tail in [("a1", b"A"), ("a2", b"A"), ("b1", b"B"), ("c1", b"C"), ("b2", b"B"), ("a3", b"A")]:
        put(tmp_path, name, prefix + tail * 10)
    got = rel(tmp_path, impl.find_duplicates_verified(str(tmp_path)))
    assert got == [["a1", "a2", "a3"], ["b1", "b2"]]


@pytest.mark.part2
@pytest.mark.edge
def test_constant_hash_is_still_correct(impl, tmp_path):
    # worst case: the hash function is useless -- correctness must come from the byte comparison
    for i in range(6):
        put(tmp_path, f"f{i}", "dup-A" if i % 2 == 0 else "dup-B")
    got = rel(tmp_path, impl.find_duplicates_verified(str(tmp_path), hash_fn=lambda p: 0))
    assert got == [["f0", "f2", "f4"], ["f1", "f3", "f5"]]


@pytest.mark.part2
@pytest.mark.edge
def test_files_equal(impl, tmp_path):
    a = put(tmp_path, "a", b"x" * 10_000)
    b = put(tmp_path, "b", b"x" * 10_000)
    c = put(tmp_path, "c", b"x" * 9_999 + b"y")
    d = put(tmp_path, "d", b"x" * 9_999)
    for cs in (1, 7, 4096, 1 << 20):
        assert impl.files_equal(a, b, cs) is True
        assert impl.files_equal(a, c, cs) is False  # differs in the very last byte
        assert impl.files_equal(a, d, cs) is False  # different size
    with pytest.raises(ValueError):
        impl.files_equal(a, b, 0)


@pytest.mark.part2
@pytest.mark.edge
def test_verified_agrees_with_strong_hash_on_a_random_tree(impl, tmp_path):
    import random

    rng = random.Random(1)
    for i in range(300):
        body = bytes(rng.choice(b"ab") for _ in range(rng.randint(0, 6)))
        put(tmp_path, f"d{i % 7}/f{i}", body)
    assert impl.find_duplicates_verified(str(tmp_path), chunk_size=2) == impl.find_duplicates(str(tmp_path), chunk_size=2)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_20k_small_files_plus_big_ones(impl, tmp_path):
    import random

    rng = random.Random(0)
    for i in range(20_000):
        size = rng.randint(0, 40)  # lots of same-size files => lots of hashing
        put(tmp_path, f"d{i % 50}/f{i}", bytes(rng.getrandbits(8) for _ in range(size)) if size < 3 else b"%d" % i + b"x" * size)
    blob = os.urandom(2 << 20)
    for n in ("big_a", "big_b", "big_c"):
        put(tmp_path, f"big/{n}", blob)
    t0 = time.perf_counter()
    strong = impl.find_duplicates(str(tmp_path))
    t1 = time.perf_counter()
    verified = impl.find_duplicates_verified(str(tmp_path))
    t2 = time.perf_counter()
    assert ["big_a", "big_b", "big_c"] in [[os.path.basename(p) for p in g] for g in strong]
    assert strong == verified
    assert t1 - t0 < 2.0 and t2 - t1 < 2.0, (t1 - t0, t2 - t1)


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_example_line_driven(impl):
    lines = [
        "POLICY oldest",
        "FILE a/x.jpg cat 300", "FILE b/y.jpg cat 100", "FILE c/long_name_z.jpg cat 200",
        "FILE d/q.jpg dog 5", "FILE d/r.jpg dog 5",
    ]
    # oldest copy of "cat" is b/y.jpg; the "dog" pair ties on mtime and path length -> lexicographic: keep d/q.jpg
    assert impl.part3(lines) == ["a/x.jpg", "c/long_name_z.jpg", "d/r.jpg"]


@pytest.mark.part3
def test_policy_oldest(impl, tmp_path):
    a = put(tmp_path, "a.jpg", "same", mtime=300)
    b = put(tmp_path, "b.jpg", "same", mtime=100)
    c = put(tmp_path, "c.jpg", "same", mtime=200)
    assert impl.plan_deletions([[a, b, c]], "oldest") == sorted([a, c])


@pytest.mark.part3
def test_policy_shortest_path(impl, tmp_path):
    a = put(tmp_path, "deep/er/dir/a.jpg", "same", mtime=1)
    b = put(tmp_path, "b.jpg", "same", mtime=999)
    c = put(tmp_path, "sub/c.jpg", "same", mtime=2)
    assert impl.plan_deletions([[a, b, c]], "shortest_path") == sorted([a, c])


@pytest.mark.part3
def test_policy_prefer_dir_and_fallback(impl, tmp_path):
    keep_dir = str(tmp_path / "originals")
    a = put(tmp_path, "downloads/a.jpg", "same", mtime=1)
    b = put(tmp_path, "originals/b.jpg", "same", mtime=500)
    c = put(tmp_path, "originals_backup/c.jpg", "same", mtime=2)  # prefix-sibling, NOT inside keep_dir
    assert impl.plan_deletions([[a, b, c]], "prefer_dir", prefer_dir=keep_dir) == sorted([a, c])
    # a group with no copy under prefer_dir falls back to 'oldest'
    d = put(tmp_path, "x/d.jpg", "other", mtime=10)
    e = put(tmp_path, "y/e.jpg", "other", mtime=20)
    assert impl.plan_deletions([[d, e]], "prefer_dir", prefer_dir=keep_dir) == [e]


@pytest.mark.part3
def test_dry_run_default_touches_nothing_and_real_run_keeps_one(impl, tmp_path):
    a = put(tmp_path, "a.jpg", "same", mtime=1)
    b = put(tmp_path, "b.jpg", "same", mtime=2)
    c = put(tmp_path, "c.jpg", "same", mtime=3)
    plan = impl.plan_deletions([[a, b, c]])
    assert plan == [b, c] and all(os.path.exists(p) for p in (a, b, c))
    done = impl.plan_deletions([[a, b, c]], dry_run=False)
    assert done == [b, c]
    assert os.path.exists(a) and not os.path.exists(b) and not os.path.exists(c)


@pytest.mark.part3
@pytest.mark.edge
def test_plan_deletions_edge_cases(impl, tmp_path):
    assert impl.plan_deletions([]) == []
    a = put(tmp_path, "a", "x")
    assert impl.plan_deletions([[a]]) == []  # a group of one is never a deletion
    b = put(tmp_path, "b", "x")
    gone = str(tmp_path / "gone")
    assert impl.plan_deletions([[a, gone]]) == []  # the other copy vanished: nothing left to dedupe
    with pytest.raises(ValueError):
        impl.plan_deletions([[a, b]], "newest")
    with pytest.raises(ValueError):
        impl.plan_deletions([[a, b]], "prefer_dir")


@pytest.mark.part3
@pytest.mark.edge
def test_plan_never_deletes_every_copy(impl, tmp_path):
    groups = []
    for g in range(20):
        groups.append([put(tmp_path, f"g{g}/f{i}", f"c{g}", mtime=i) for i in range(4)])
    for pol in ("oldest", "shortest_path"):
        victims = set(impl.plan_deletions(groups, pol))
        for g in groups:
            assert sum(p not in victims for p in g) == 1


# ------------------------------------------------------------------------ Part 4
FLAT = [[10] * 8 for _ in range(8)]
HALF = [[0] * 8 for _ in range(4)] + [[255] * 8 for _ in range(4)]


@pytest.mark.part4
def test_part4_worked_example_line_driven(impl):
    a = ",".join(["0"] * 32 + ["255"] * 32)
    b = ",".join(["0"] * 32 + ["255"] * 31 + ["0"])
    c = ",".join(["255"] * 32 + ["0"] * 32)
    assert impl.part4(["THRESHOLD 2", f"IMG a {a}", f"IMG b {b}", f"IMG c {c}"]) == ["a b"]


@pytest.mark.part4
def test_average_hash_values(impl):
    assert impl.average_hash(HALF) == 0x00000000FFFFFFFF
    assert impl.average_hash(FLAT) == 0  # nothing is strictly above the mean
    brighter = [[min(255, v + 20) for v in row] for row in HALF]
    assert impl.average_hash(brighter) == impl.average_hash(HALF)  # brightness shift keeps structure


@pytest.mark.part4
def test_hamming(impl):
    assert impl.hamming(0, 0) == 0
    assert impl.hamming(0b1010, 0b0101) == 4
    assert impl.hamming((1 << 64) - 1, 0) == 64


@pytest.mark.part4
@pytest.mark.edge
def test_average_hash_rejects_bad_shapes(impl):
    for bad in ([], [[1] * 8] * 7, [[1] * 7] * 8, [[1] * 8] * 7 + [[1] * 9]):
        with pytest.raises(ValueError):
            impl.average_hash(bad)


@pytest.mark.part4
def test_group_similar_threshold_and_transitivity(impl):
    def flip(m, k):  # flip k pixels from 0 to 255 in the dark half
        m = [r[:] for r in m]
        for i in range(k):
            m[i // 8][i % 8] = 255
        return m

    imgs = {"a": HALF, "b": flip(HALF, 3), "c": flip(HALF, 6), "far": [[255] * 8 for _ in range(4)] + [[0] * 8 for _ in range(4)]}
    h = {n: impl.average_hash(m) for n, m in imgs.items()}
    assert impl.hamming(h["a"], h["b"]) == 3 and impl.hamming(h["b"], h["c"]) == 3 and impl.hamming(h["a"], h["c"]) == 6
    assert impl.group_similar(imgs, threshold=3) == [["a", "b", "c"]]  # a~b, b~c: connected although a!~c
    assert impl.group_similar(imgs, threshold=2) == []
    assert impl.group_similar(imgs, threshold=64) == [["a", "b", "c", "far"]]
    with pytest.raises(ValueError):
        impl.group_similar(imgs, threshold=-1)


@pytest.mark.part4
@pytest.mark.edge
def test_group_similar_empty_and_single(impl):
    assert impl.group_similar({}) == []
    assert impl.group_similar({"only": HALF}) == []


# ------------------------------------------------------------------------ io
@pytest.mark.io
def test_part1_io(run_script):
    r = run_script("PART 1\nFILE a/x.jpg cat\nFILE b/y.jpg cat\nFILE c/z.jpg dog\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a/x.jpg b/y.jpg\n"


@pytest.mark.io
def test_part3_io(run_script):
    r = run_script("PART 3\nPOLICY shortest_path\nFILE a/long/x.jpg cat\nFILE y.jpg cat\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a/long/x.jpg\n"


@pytest.mark.io
def test_part2_io_no_groups_prints_nothing(run_script):
    head = "H" * 1024
    r = run_script(f"PART 2\nFILE a.bin {head}A\nFILE b.bin {head}B\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == ""
