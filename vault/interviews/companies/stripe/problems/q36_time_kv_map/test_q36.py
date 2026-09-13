import random

import pytest


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_block1_verbatim(impl):
    d = impl.MultiTimeMap()
    d.set(1, 1, 0)
    d.set(1, 2, 2)
    assert d.get(1, 1) == 1
    assert d.get(1, 3) == 2


@pytest.mark.part1
def test_example_block2_verbatim(impl):
    d = impl.MultiTimeMap()
    d.set(1, 1, 5)
    assert d.get(1, 0) is None
    assert d.get(1, 10) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_example_block3_same_time_overwrites(impl):
    d = impl.MultiTimeMap()
    d.set(1, 1, 0)
    d.set(1, 2, 0)
    assert d.get(1, 0) == 2
    assert d.get_all(1, 0) == [2]      # one version per distinct time


@pytest.mark.part1
@pytest.mark.edge
def test_get_boundaries_and_unknown_key(impl):
    d = impl.MultiTimeMap()
    d.set("k", "v", 5)
    assert d.get("k", 4) is None
    assert d.get("k", 5) == "v"        # '<=' not '<'
    assert d.get("k", 6) == "v"
    assert d.get("missing", 5) is None
    assert impl.MultiTimeMap().get("k", 0) is None


@pytest.mark.part1
@pytest.mark.edge
def test_out_of_order_writes(impl):
    d = impl.MultiTimeMap()
    d.set("k", "c", 30)
    d.set("k", "a", 10)
    d.set("k", "b", 20)
    assert [d.get("k", t) for t in (9, 10, 15, 20, 25, 30, 99)] == [None, "a", "a", "b", "b", "c", "c"]


@pytest.mark.part1
@pytest.mark.fmt
def test_process_part1_lines_null(impl):
    out = impl.process(["SET 1 1 0", "SET 1 2 2", "GET 1 1", "GET 1 3", "GET 2 0"], 1)
    assert out == ["1", "2", "null"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_get_all(impl):
    out = impl.process(["SET k a 1", "SET k c 3", "SET k b 2", "GETALL k 2", "GETALL k 0", "GETALL k 3"], 2)
    assert out == ["a b", "", "a b c"]


@pytest.mark.part2
@pytest.mark.edge
def test_get_all_empty_and_unknown(impl):
    d = impl.MultiTimeMap()
    assert d.get_all("k", 100) == []
    d.set("k", "x", 50)
    assert d.get_all("k", 49) == []
    assert d.get_all("k", 50) == ["x"]
    assert d.get_all("other", 50) == []


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_ttl(impl):
    out = impl.process(["SET s x 10 5", "GET s 14", "GET s 15", "SET s y 20", "GET s 100"], 3)
    assert out == ["x", "null", "y"]


@pytest.mark.part3
@pytest.mark.edge
def test_ttl_boundaries(impl):
    d = impl.MultiTimeMap()
    d.set("k", "v", 10, ttl=5)
    assert d.get("k", 9) is None
    assert d.get("k", 10) == "v"
    assert d.get("k", 14) == "v"       # time + ttl - 1 alive
    assert d.get("k", 15) is None      # time + ttl expired (exclusive end)
    d.set("z", "v", 0, ttl=0)          # ttl 0: never readable
    assert d.get("z", 0) is None


@pytest.mark.part3
@pytest.mark.edge
def test_expired_newer_version_hides_older_and_get_all_filters(impl):
    d = impl.MultiTimeMap()
    d.set("k", "old", 0)               # no ttl
    d.set("k", "new", 10, ttl=2)
    assert d.get("k", 11) == "new"
    assert d.get("k", 12) is None      # no fallback to 'old'
    assert d.get("k", 5) == "old"
    assert d.get_all("k", 11) == ["old", "new"]
    assert d.get_all("k", 12) == ["old"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_first_missing_positive(impl):
    assert impl.first_missing_positive([3, 4, -1, 1]) == 2
    assert impl.first_missing_positive([1, 2, 0]) == 3
    assert impl.process(["3 4 -1 1"], 4) == ["2"]


@pytest.mark.part4
@pytest.mark.edge
def test_first_missing_positive_edges(impl):
    assert impl.first_missing_positive([]) == 1
    assert impl.first_missing_positive([1]) == 2
    assert impl.first_missing_positive([2]) == 1
    assert impl.first_missing_positive([1, 1, 2, 2]) == 3
    assert impl.first_missing_positive([-5, -1, 0]) == 1
    assert impl.first_missing_positive(list(range(1, 1001))) == 1001


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\nSET s x 10 5\n\nGET s 14\nGET s 15\nSET s y 20\nGET s 100\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "x\nnull\ny\n"
    assert run_script("PART 2\nSET k a 1\nGETALL k 0\nGETALL k 1\n").stdout == "\na\n"
    assert run_script("PART 4\n\n").stdout == "1\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_200k_ops(run_script):
    rng = random.Random(0)
    lines = []
    for _ in range(200_000):
        k = rng.randrange(1000)
        if rng.random() < 0.5:
            lines.append(f"SET k{k} v{rng.randrange(10)} {rng.randrange(1_000_000)}")
        else:
            lines.append(f"GET k{k} {rng.randrange(1_000_000)}")
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == sum(ln.startswith("GET") for ln in lines)
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
