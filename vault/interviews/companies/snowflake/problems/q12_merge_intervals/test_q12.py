import random

import pytest


def _brute(intervals):
    """Repeatedly fuse any pair that overlaps or touches at a shared point
    (a.start <= b.end and b.start <= a.end), independent of the sort-and-sweep
    algorithm under test. O(n^2) per pass, fine for the small random inputs here."""
    ivs = [list(iv) for iv in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(ivs)):
            for j in range(i + 1, len(ivs)):
                a, b = ivs[i], ivs[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    ivs[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    del ivs[j]
                    changed = True
                    break
            if changed:
                break
    ivs.sort()
    return ivs


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "intervals,expected",
    [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),  # LC56 example 1
        ([[1, 4], [4, 5]], [[1, 5]]),  # LC56 example 2 -- touching counts as overlapping
        ([[1, 10], [2, 3]], [[1, 10]]),  # nested containment
        ([], []),
        ([[5, 5]], [[5, 5]]),
    ],
)
def test_worked_examples(impl, intervals, expected):
    assert impl.merge_intervals(intervals) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_single_interval(impl):
    assert impl.merge_intervals([[1, 2]]) == [[1, 2]]


@pytest.mark.part1
@pytest.mark.edge
def test_already_disjoint_unsorted_input(impl):
    assert impl.merge_intervals([[15, 18], [1, 3], [8, 10]]) == [[1, 3], [8, 10], [15, 18]]


@pytest.mark.part1
@pytest.mark.edge
def test_negative_bounds(impl):
    assert impl.merge_intervals([[-5, -2], [-3, 0], [2, 4]]) == [[-5, 0], [2, 4]]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_intervals(impl):
    assert impl.merge_intervals([[1, 3], [1, 3], [1, 3]]) == [[1, 3]]


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "intervals",
    [
        [[1]],           # wrong arity
        [[3, 1]],        # start > end
        [["a", "b"]],    # non-int
        [[1, 2, 3]],     # wrong arity
    ],
)
def test_malformed_interval_raises(impl, intervals):
    with pytest.raises(ValueError):
        impl.merge_intervals(intervals)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_point_marking_brute_force(impl):
    rng = random.Random(0)
    for _ in range(500):
        n = rng.randint(0, 8)
        intervals = []
        for _ in range(n):
            a = rng.randint(0, 30)
            b = rng.randint(a, 30)
            intervals.append([a, b])
        assert impl.merge_intervals(intervals) == _brute(intervals), intervals


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(0)
    n = 100_000
    intervals = []
    for _ in range(n):
        a = rng.randint(0, 200_000)
        intervals.append((a, a + rng.randint(0, 5)))
    body = "\n".join(f"{s} {e}" for s, e in intervals)
    r = run_script(f"PART 1\n{n}\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_stream_add_then_snapshot(impl):
    st = impl.IntervalStream()
    st.add([1, 3])
    st.add([6, 8])
    assert st.snapshot() == [[1, 3], [6, 8]]
    st.add([2, 5])
    assert st.snapshot() == [[1, 5], [6, 8]]
    st.add([7, 9])
    assert st.snapshot() == [[1, 5], [6, 9]]


@pytest.mark.part2
@pytest.mark.edge
def test_stream_empty_snapshot(impl):
    st = impl.IntervalStream()
    assert st.snapshot() == []


@pytest.mark.part2
@pytest.mark.edge
def test_stream_snapshot_does_not_mutate_state(impl):
    st = impl.IntervalStream()
    st.add([1, 2])
    first = st.snapshot()
    first.append([99, 100])  # mutate the returned list
    assert st.snapshot() == [[1, 2]]  # internal state must be unaffected


@pytest.mark.part2
@pytest.mark.edge
def test_stream_add_rejects_malformed_interval(impl):
    st = impl.IntervalStream()
    with pytest.raises(ValueError):
        st.add([5, 1])


@pytest.mark.part2
@pytest.mark.edge
def test_stream_matches_batch_merge_at_every_point(impl):
    rng = random.Random(1)
    st = impl.IntervalStream()
    seen = []
    for _ in range(200):
        a = rng.randint(0, 50)
        b = rng.randint(a, 50)
        st.add([a, b])
        seen.append([a, b])
        if rng.random() < 0.1:
            assert st.snapshot() == impl.merge_intervals(seen)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k_ops(run_script):
    rng = random.Random(2)
    n = 100_000
    ops = []
    for i in range(n):
        a = rng.randint(0, 200_000)
        ops.append(f"ADD {a} {a + rng.randint(0, 5)}")
        if i % 25_000 == 24_999:
            ops.append("SNAPSHOT")
    ops.append("SNAPSHOT")
    body = "\n".join(ops)
    r = run_script(f"PART 2\n{len(ops)}\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n4\n1 3\n2 6\n8 10\n15 18\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1,6 8,10 15,18\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n4\nADD 1 3\nADD 6 8\nSNAPSHOT\nADD 2 5\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1,3 6,8\n"
