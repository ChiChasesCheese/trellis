import random

import pytest


def _brute(piles, k):
    """Re-sort and shrink the current max each iteration -- O(k n log n), a
    different code path from the heap under test but the same greedy rule."""
    piles = list(piles)
    for _ in range(k):
        if not piles or max(piles) == 0:
            break
        piles.sort()
        piles[-1] -= piles[-1] // 2
    return sum(piles)


def _brute_stream(ops):
    """Simulate the online add/apply stream with a plain sort-based list,
    independent of StoneStream's heap."""
    piles: list[int] = []
    out = []
    for op, val in ops:
        if op == "ADD":
            piles.append(val)
        else:
            for _ in range(val):
                if not piles or max(piles) == 0:
                    break
                piles.sort()
                piles[-1] -= piles[-1] // 2
            out.append(sum(piles))
    return out


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "piles,k,expected",
    [
        ([5, 4, 9], 2, 12),      # LC1962 example 1
        ([4, 3, 6, 7], 3, 12),   # LC1962 example 2
        ([1], 5, 1),             # halving 1 -> 1 - 0 = 1 forever (floor(1/2)=0)
    ],
)
def test_worked_examples(impl, piles, k, expected):
    assert impl.min_total_after_k_removals(piles, k) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_k_zero_is_a_no_op(impl):
    assert impl.min_total_after_k_removals([5, 4, 9], 0) == 18


@pytest.mark.part1
@pytest.mark.edge
def test_k_larger_than_needed_converges(impl):
    # Repeated halving of any pile eventually hits a fixed point (1 -> 1, 0 -> 0).
    assert impl.min_total_after_k_removals([1, 1, 1], 100) == 3


@pytest.mark.part1
@pytest.mark.edge
def test_single_pile(impl):
    assert impl.min_total_after_k_removals([10], 1) == 5


@pytest.mark.part1
@pytest.mark.edge
def test_all_piles_equal(impl):
    assert impl.min_total_after_k_removals([8, 8, 8], 1) == 20  # one 8 -> 4


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "piles,k",
    [([0], 1), ([-1], 1), ([1.5], 1), ([5], -1)],
)
def test_invalid_input_raises(impl, piles, k):
    with pytest.raises(ValueError):
        impl.min_total_after_k_removals(piles, k)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_sort_based_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(1, 6)
        piles = [rng.randint(1, 30) for _ in range(n)]
        k = rng.randint(0, 10)
        assert impl.min_total_after_k_removals(piles, k) == _brute(piles, k), (piles, k)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(0)
    n = 100_000
    piles = [rng.randint(1, 10_000) for _ in range(n)]
    k = 100_000
    body = " ".join(map(str, piles))
    r = run_script(f"PART 1\n{n} {k}\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout) >= 0
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_stream_matches_batch_after_all_adds(impl):
    st = impl.StoneStream()
    st.add(5)
    st.add(4)
    st.add(9)
    assert st.apply(2) == 12


@pytest.mark.part2
@pytest.mark.edge
def test_stream_interleaved_add_and_apply(impl):
    st = impl.StoneStream()
    st.add(5)
    st.add(4)
    st.add(9)
    assert st.apply(2) == 12  # piles now effectively [3, 4, 5] (sum 12)
    st.add(2)
    assert st.apply(1) == 12  # add 2 -> total 14; halve the max (5 -> 3) -> 12


@pytest.mark.part2
@pytest.mark.edge
def test_stream_empty_apply(impl):
    st = impl.StoneStream()
    assert st.apply(5) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_stream_apply_zero_is_a_no_op(impl):
    st = impl.StoneStream()
    st.add(3)
    st.add(7)
    assert st.apply(0) == 10


@pytest.mark.part2
@pytest.mark.edge
def test_stream_add_rejects_invalid_pile(impl):
    st = impl.StoneStream()
    with pytest.raises(ValueError):
        st.add(0)


@pytest.mark.part2
@pytest.mark.edge
def test_stream_apply_rejects_negative_k(impl):
    st = impl.StoneStream()
    st.add(5)
    with pytest.raises(ValueError):
        st.apply(-1)


@pytest.mark.part2
@pytest.mark.edge
def test_stream_random_against_sort_based_brute_force(impl):
    rng = random.Random(1)
    for _ in range(80):
        ops = []
        for _ in range(rng.randint(1, 15)):
            if rng.random() < 0.6:
                ops.append(("ADD", rng.randint(1, 30)))
            else:
                ops.append(("APPLY", rng.randint(0, 5)))
        expected = _brute_stream(ops)
        st = impl.StoneStream()
        actual = []
        for op, val in ops:
            if op == "ADD":
                st.add(val)
            else:
                actual.append(st.apply(val))
        assert actual == expected, ops


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k_ops(run_script):
    rng = random.Random(2)
    ops = []
    for i in range(90_000):
        ops.append(f"ADD {rng.randint(1, 10_000)}")
    ops.append("APPLY 100000")
    body = "\n".join(ops)
    r = run_script(f"PART 2\n{len(ops)}\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert int(r.stdout.strip()) >= 0
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n3 2\n5 4 9\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "12\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n4\nADD 5\nADD 4\nADD 9\nAPPLY 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "12\n"
