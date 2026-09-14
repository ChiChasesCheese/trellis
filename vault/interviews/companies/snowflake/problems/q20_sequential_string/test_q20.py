import random
from collections import Counter

import pytest


def _brute(s: str, queries: list[str]) -> list[int]:
    """Ground truth: scan prefix lengths 0..len(s), stop at the first that covers the query's
    digit multiset."""
    out = []
    for q in queries:
        need = Counter(q)
        if not need:
            out.append(0)
            continue
        found = -1
        for L in range(1, len(s) + 1):
            have = Counter(s[:L])
            if all(have[d] >= c for d, c in need.items()):
                found = L
                break
        out.append(found)
    return out


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_source(impl):
    s = "064819848398"
    assert impl.sequential_prefix_lengths_binary(s, ["088", "364", "071"]) == [7, 10, -1]


@pytest.mark.part1
@pytest.mark.edge
def test_order_matching_bug_counterexample(impl):
    # The source's own reference solution matches query digits IN ORDER as a subsequence of s.
    # s = "21": to match "1" then "2" in order you'd need a '1' followed later by a '2', which
    # doesn't exist -> the buggy solution says -1 (or a longer prefix). The correct multiset
    # answer only needs {'1': 1, '2': 1} to both be present somewhere in the prefix: prefix "21"
    # (length 2) already has one of each, in either order.
    assert impl.sequential_prefix_lengths_binary("21", ["12"]) == [2]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_query_needs_zero_length_prefix(impl):
    assert impl.sequential_prefix_lengths_binary("11", [""]) == [0]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_s_all_impossible_except_empty_query(impl):
    assert impl.sequential_prefix_lengths_binary("", ["1", ""]) == [-1, 0]


@pytest.mark.part1
@pytest.mark.edge
def test_digit_never_present_is_impossible(impl):
    assert impl.sequential_prefix_lengths_binary("11111", ["17"]) == [-1]


@pytest.mark.part1
@pytest.mark.edge
def test_needs_all_of_s(impl):
    # every digit of s needed exactly once -> answer is len(s)
    assert impl.sequential_prefix_lengths_binary("321", ["123"]) == [3]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_digit_needs_multiple_occurrences(impl):
    # need two '8's; they occur at positions 3 and 6 (0-based) -> prefix length 7
    assert impl.sequential_prefix_lengths_binary("064819848398", ["88"]) == [7]


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.sequential_prefix_lengths_binary("12a3", ["1"])
    with pytest.raises(ValueError):
        impl.sequential_prefix_lengths_binary("123", ["1x"])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 12)
        s = "".join(rng.choice("012") for _ in range(n))  # small alphabet -> forces collisions
        queries = ["".join(rng.choice("012") for _ in range(rng.randint(0, 4))) for _ in range(5)]
        assert impl.sequential_prefix_lengths_binary(s, queries) == _brute(s, queries), (s, queries)


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_100k(run_script):
    rng = random.Random(1)
    n = 100_000
    s = "".join(rng.choice("0123456789") for _ in range(n))
    m = 20_000
    queries = ["".join(rng.choice("0123456789") for _ in range(25)) for _ in range(m)]
    stdin = f"PART 1\n{s}\n{m}\n" + "\n".join(queries) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert len(r.stdout.splitlines()) == m
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example(impl):
    s = "064819848398"
    assert impl.sequential_prefix_lengths_fast(s, ["088", "364", "071"]) == [7, 10, -1]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_matches_part1_on_random_inputs(impl):
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(0, 30)
        s = "".join(rng.choice("0123456789") for _ in range(n))
        queries = ["".join(rng.choice("0123456789") for _ in range(rng.randint(0, 6))) for _ in range(6)]
        assert impl.sequential_prefix_lengths_fast(s, queries) == impl.sequential_prefix_lengths_binary(s, queries)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.sequential_prefix_lengths_fast("1a2", ["1"])


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_100k_500k_total_query_length(run_script):
    rng = random.Random(3)
    n = 100_000
    s = "".join(rng.choice("0123456789") for _ in range(n))
    m = 20_000
    # total query length ~500_000 (25 chars average)
    queries = ["".join(rng.choice("0123456789") for _ in range(25)) for _ in range(m)]
    stdin = f"PART 2\n{s}\n{m}\n" + "\n".join(queries) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert len(r.stdout.splitlines()) == m
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n064819848398\n3\n088\n364\n071\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7\n10\n-1\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n064819848398\n3\n088\n364\n071\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "7\n10\n-1\n"
