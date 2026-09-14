import random

import pytest

EXAMPLE = dict(s0=2, n=3, k=3, b=3, m=2, a=15)
EXAMPLE_ANSWER = 5


def _generate_reference(s0, n, k, b, m):
    """Local, independent reimplementation of the generator for test bookkeeping
    only (not used to validate part1/part2 against each other)."""
    if n <= 0:
        return []
    sides = [s0]
    for _ in range(n - 1):
        prev = sides[-1]
        sides.append(((k * prev + b) % m) + 1 + prev)
    return sides


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_official_example(impl):
    assert impl.part1(**EXAMPLE) == EXAMPLE_ANSWER


@pytest.mark.part1
@pytest.mark.edge
def test_generation_matches_hand_trace(impl):
    # sides should be [2,4,6] for the official example; verify indirectly via a=huge
    # (every pair counts) and a=0 (no pair counts, since sides are all positive)
    assert impl.part1(s0=2, n=3, k=3, b=3, m=2, a=10**9) == 9
    assert impl.part1(s0=2, n=3, k=3, b=3, m=2, a=0) == 0


@pytest.mark.part1
@pytest.mark.edge
def test_n_equals_1_only_pair_is_self(impl):
    assert impl.part1(s0=5, n=1, k=1, b=1, m=10, a=25) == 1  # 5*5=25 <= 25
    assert impl.part1(s0=5, n=1, k=1, b=1, m=10, a=24) == 0  # 5*5=25 > 24


@pytest.mark.part1
@pytest.mark.edge
def test_m_equals_1_exact_count(impl):
    # m=1 -> mod term always 0 -> sides[i] = 1 + sides[i-1] (simple +1 ladder)
    # s0=1, n=4 -> sides = [1,2,3,4]
    sides = _generate_reference(s0=1, n=4, k=999, b=999, m=1)
    assert sides == [1, 2, 3, 4]
    expected = sum(1 for x in sides for y in sides if x * y <= 4)
    assert impl.part1(s0=1, n=4, k=999, b=999, m=1, a=4) == expected


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_part2_official_example(impl):
    assert impl.part2(**EXAMPLE) == EXAMPLE_ANSWER


@pytest.mark.part2
@pytest.mark.edge
def test_part2_n_equals_1(impl):
    assert impl.part2(s0=5, n=1, k=1, b=1, m=10, a=25) == 1
    assert impl.part2(s0=5, n=1, k=1, b=1, m=10, a=24) == 0


@pytest.mark.part2
@pytest.mark.edge
def test_part2_a_zero_and_a_huge(impl):
    assert impl.part2(s0=2, n=3, k=3, b=3, m=2, a=0) == 0
    assert impl.part2(s0=2, n=3, k=3, b=3, m=2, a=10**9) == 9


@pytest.mark.part2
def test_part2_randomized_cross_check_against_part1(impl):
    rng = random.Random(0)
    trials = 50
    for _ in range(trials):
        s0 = rng.randint(1, 20)
        n = rng.randint(1, 50)
        k = rng.choice([0, 0, rng.randint(0, 10)])
        b = rng.choice([0, 0, rng.randint(0, 10)])
        m = rng.choice([1, 1, rng.randint(2, 20)])
        # vary a: sometimes tiny (below smallest product), sometimes huge (above largest)
        a_choice = rng.choice(["tiny", "huge", "mid"])
        if a_choice == "tiny":
            a = 0
        elif a_choice == "huge":
            a = 10**12
        else:
            a = rng.randint(0, 10_000)
        p1 = impl.part1(s0, n, k, b, m, a)
        p2 = impl.part2(s0, n, k, b, m, a)
        assert p1 == p2, f"mismatch for s0={s0},n={n},k={k},b={b},m={m},a={a}: {p1} != {p2}"


@pytest.mark.part2
@pytest.mark.perf
def test_part2_perf_1e6_n(impl):
    import time

    rng = random.Random(0)
    s0 = rng.randint(1, 100)
    n = 1_000_000
    k = rng.randint(0, 1000)
    b = rng.randint(0, 1000)
    m = rng.randint(2, 1000)
    a = 10**15
    t0 = time.perf_counter()
    result = impl.part2(s0, n, k, b, m, a)
    elapsed = time.perf_counter() - t0
    assert isinstance(result, int)
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n2 3 3 3 2 15\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part1_dispatch(run_script):
    r = run_script("PART 1\n2 3 3 3 2 15\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "5\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_n_equals_1(run_script):
    r = run_script("PART 2\n5 1 1 1 10 25\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n"
