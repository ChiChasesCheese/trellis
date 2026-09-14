import random
import time

import pytest

LC56_EX1 = [[1, 3], [2, 6], [8, 10], [15, 18]]


def brute_merge(intervals, gap):
    ivs = sorted(intervals)
    out = []
    for s, e in ivs:
        if out and s <= out[-1][1] + gap:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def brute_uncovered(intervals):
    keep = []
    for i, (a, b) in enumerate(intervals):
        covered = any((c <= a and b <= d) and (j < i if (c, d) == (a, b) else True) for j, (c, d) in enumerate(intervals) if j != i)
        if not covered:
            keep.append([a, b])
    return sorted(keep)


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_lc56_examples(impl):
    assert impl.merge(LC56_EX1) == [[1, 6], [8, 10], [15, 18]]
    assert impl.merge([[1, 4], [4, 5]]) == [[1, 5]]


@pytest.mark.part1
@pytest.mark.edge
def test_merge_boundaries(impl):
    assert impl.merge([[1, 4], [5, 6]]) == [[1, 4], [5, 6]]      # real endpoints: 4 < 5 -> no merge
    assert impl.merge([[1, 4], [4, 4]]) == [[1, 4]]
    assert impl.merge([[5, 5], [5, 5]]) == [[5, 5]]
    assert impl.merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]     # contained ones vanish
    assert impl.merge([[0, 0]]) == [[0, 0]]
    assert impl.merge([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_merge_unsorted_and_chain(impl):
    assert impl.merge([[8, 10], [1, 3], [15, 18], [2, 6]]) == [[1, 6], [8, 10], [15, 18]]
    assert impl.merge([[3, 4], [2, 3], [1, 2], [0, 1]]) == [[0, 4]]
    assert impl.merge([[1, 4], [0, 4]]) == [[0, 4]]
    assert impl.merge([[1, 4], [0, 0]]) == [[0, 0], [1, 4]]


@pytest.mark.part1
def test_merge_random_against_brute(impl):
    rng = random.Random(0)
    for _ in range(200):
        ivs = [sorted([rng.randrange(0, 30), rng.randrange(0, 30)]) for _ in range(rng.randrange(0, 12))]
        assert impl.merge([list(iv) for iv in ivs]) == brute_merge(ivs, 0)


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_lc1288_examples(impl):
    assert impl.remove_covered_intervals([[1, 4], [3, 6], [2, 8]]) == 2
    assert impl.uncovered([[1, 4], [3, 6], [2, 8]]) == [[1, 4], [2, 8]]
    assert impl.remove_covered_intervals([[1, 4], [2, 3]]) == 1
    assert impl.uncovered([[1, 4], [2, 3]]) == [[1, 4]]


@pytest.mark.part2
@pytest.mark.edge
def test_covered_same_start_and_chains(impl):
    assert impl.remove_covered_intervals([[1, 2], [1, 4], [3, 4]]) == 1     # same start: end desc
    assert impl.remove_covered_intervals([[1, 10], [2, 9], [3, 8]]) == 1
    assert impl.remove_covered_intervals([[1, 2], [3, 4], [5, 6]]) == 3
    assert impl.remove_covered_intervals([[0, 100000]] + [[i, i + 1] for i in range(0, 100, 7)]) == 1
    assert impl.remove_covered_intervals([[1, 4]]) == 1
    assert impl.remove_covered_intervals([]) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_covered_duplicates_and_touching(impl):
    assert impl.uncovered([[1, 4], [1, 4]]) == [[1, 4]]          # equal intervals: one survives
    assert impl.uncovered([[1, 4], [4, 6]]) == [[1, 4], [4, 6]]  # touching is not covering
    assert impl.uncovered([[2, 3], [1, 3]]) == [[1, 3]]          # same end, earlier start covers


@pytest.mark.part2
def test_covered_random_against_brute(impl):
    rng = random.Random(1)
    for _ in range(200):
        ivs = []
        while len(ivs) < rng.randrange(0, 10):
            a, b = rng.randrange(0, 15), rng.randrange(0, 15)
            if a < b and [a, b] not in ivs:
                ivs.append([a, b])
        assert impl.uncovered([list(iv) for iv in ivs]) == brute_uncovered(ivs)
        assert impl.remove_covered_intervals([list(iv) for iv in ivs]) == len(brute_uncovered(ivs))


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_fill_gaps_example(impl):
    L = impl.Labeled
    got = impl.fill_gaps([L(10, 20, "VISA"), L(30, 40, "MC"), L(35, 38, "AMEX"), L(50, 60, "MC"), L(61, 70, "MC")], 0, 99)
    assert got == [L(0, 29, "VISA"), L(30, 49, "MC"), L(35, 38, "AMEX"), L(50, 99, "MC")]
    assert impl.fill_gaps([L(3, 4, "X")], 0, 9) == [L(0, 9, "X")]
    assert impl.fill_gaps([], 0, 9) == []


@pytest.mark.part3
@pytest.mark.edge
def test_fill_gaps_nested_holder_and_ties(impl):
    L = impl.Labeled
    # nested: the covering interval (holder of max end) grows across the gap, the inner one keeps bounds
    assert impl.fill_gaps([L(0, 50, "A"), L(10, 20, "B"), L(70, 99, "C")], 0, 99) == [L(0, 69, "A"), L(10, 20, "B"), L(70, 99, "C")]
    # tie on max end: [0,50,A] and [40,50,B] -> A (smaller start) is extended
    assert impl.fill_gaps([L(0, 50, "A"), L(40, 50, "B"), L(70, 99, "C")], 0, 99) == [L(0, 69, "A"), L(40, 50, "B"), L(70, 99, "C")]
    # largest-end tie for the hi extension also picks the covering interval
    assert impl.fill_gaps([L(0, 50, "A"), L(40, 50, "B")], 0, 99) == [L(0, 99, "A"), L(40, 50, "B")]
    # touching intervals: no gap, nothing extended; different labels never merge
    assert impl.fill_gaps([L(0, 4, "A"), L(5, 9, "B")], 0, 9) == [L(0, 4, "A"), L(5, 9, "B")]


@pytest.mark.part3
@pytest.mark.edge
def test_fill_gaps_merge_same_label(impl):
    L = impl.Labeled
    assert impl.fill_gaps([L(0, 4, "A"), L(5, 9, "A")], 0, 9) == [L(0, 9, "A")]
    assert impl.fill_gaps([L(2, 4, "A"), L(6, 9, "A")], 0, 9) == [L(0, 9, "A")]        # gap filled then merged
    assert impl.fill_gaps([L(0, 3, "A"), L(2, 5, "A"), L(6, 9, "A")], 0, 9) == [L(0, 9, "A")]
    assert impl.fill_gaps([L(0, 3, "A"), L(4, 5, "B"), L(6, 9, "A")], 0, 9) == [L(0, 3, "A"), L(4, 5, "B"), L(6, 9, "A")]


@pytest.mark.part3
def test_fill_gaps_covers_whole_range(impl):
    L = impl.Labeled
    rng = random.Random(2)
    for _ in range(100):
        lo, hi = 0, 60
        ivs = []
        for _ in range(rng.randrange(1, 6)):
            a, b = sorted([rng.randrange(lo, hi + 1), rng.randrange(lo, hi + 1)])
            ivs.append(L(a, b, rng.choice("AB")))
        out = impl.fill_gaps(ivs, lo, hi)
        assert out == sorted(out)
        covered = set()
        for s, e, _ in out:
            assert lo <= s <= e <= hi
            covered.update(range(s, e + 1))
        assert covered == set(range(lo, hi + 1))
        assert min(o.start for o in out) == lo and max(o.end for o in out) == hi


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_inclusive_examples(impl):
    assert impl.merge_inclusive([[1, 2], [3, 4]]) == [[1, 4]]
    assert impl.merge_inclusive([[1, 2], [4, 5]]) == [[1, 2], [4, 5]]
    assert impl.merge_inclusive(LC56_EX1) == [[1, 6], [8, 10], [15, 18]]


@pytest.mark.part4
@pytest.mark.edge
def test_inclusive_boundaries_and_random(impl):
    assert impl.merge_inclusive([[5, 5], [6, 6], [8, 8]]) == [[5, 6], [8, 8]]
    assert impl.merge_inclusive([[3, 4], [1, 2]]) == [[1, 4]]
    assert impl.merge_inclusive([]) == []
    rng = random.Random(3)
    for _ in range(200):
        ivs = [sorted([rng.randrange(0, 30), rng.randrange(0, 30)]) for _ in range(rng.randrange(0, 12))]
        assert impl.merge_inclusive([list(iv) for iv in ivs]) == brute_merge(ivs, 1)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    ex = "1 3\n2 6\n8 10\n15 18\n"
    r = run_script("PART 1\n" + ex)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1 6\n8 10\n15 18\n"
    assert run_script("PART 2\n1 4\n3 6\n2 8\n").stdout == "2\n1 4\n2 8\n"
    assert run_script("PART 3\n0 99\n10 20 VISA\n30 40 MC\n35 38 AMEX\n50 60 MC\n61 70 MC\n\n").stdout == (
        "0 29 VISA\n30 49 MC\n35 38 AMEX\n50 99 MC\n")
    assert run_script("PART 4\n1 2\n3 4\n").stdout == "1 4\n"
    assert run_script("PART 1\n").stdout == ""
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max_and_stress(impl, run_script):
    rng = random.Random(0)
    lc56 = [sorted([rng.randrange(0, 10_001), rng.randrange(0, 10_001)]) for _ in range(10_000)]
    lc1288 = list({tuple(sorted([rng.randrange(0, 100_000), rng.randrange(1, 100_001)])) for _ in range(1200)})
    lc1288 = [list(t) for t in lc1288 if t[0] < t[1]][:1000]
    big = [sorted([rng.randrange(0, 10**9), rng.randrange(0, 10**9)]) for _ in range(100_000)]
    t0 = time.perf_counter()
    for _ in range(10):
        impl.merge([list(iv) for iv in lc56])
        impl.remove_covered_intervals([list(iv) for iv in lc1288])
    impl.merge([list(iv) for iv in big])
    impl.remove_covered_intervals([list(iv) for iv in big])
    impl.merge_inclusive([list(iv) for iv in big])
    assert time.perf_counter() - t0 < 2.0
    r = run_script("PART 1\n" + "\n".join(f"{s} {e}" for s, e in lc56) + "\n")
    assert r.returncode == 0, r.stderr
    assert [list(map(int, ln.split())) for ln in r.stdout.splitlines()] == brute_merge(lc56, 0)
    assert r.seconds < 2.0 and r.max_rss_mb < 256
