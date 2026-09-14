import random
import tracemalloc

import pytest

HAPPY_UP_TO_50 = [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49]


def _forbidden(*_a, **_k):
    raise AssertionError("Part 2 must not build a set/dict (O(1) extra space)")


def _brute_cycle(step, n, b, p):
    seen, i = {}, 0
    while n not in seen:
        seen[n] = i
        n = step(n, b, p)
        i += 1
    start = seen[n]
    cyc = [k for k, v in seen.items() if v >= start]
    return len(cyc), min(cyc)


def _digit_power_step(n, b, p):
    t = 0
    while n:
        n, d = divmod(n, b)
        t += d ** p
    return t


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize("n,expected", [(19, True), (2, False), (1, True), (7, True), (20, False)])
def test_worked_examples_set(impl, n, expected):
    assert impl.is_happy_set(n) is expected


@pytest.mark.part1
@pytest.mark.edge
def test_happy_numbers_up_to_50(impl):
    assert [n for n in range(1, 51) if impl.is_happy_set(n)] == HAPPY_UP_TO_50


@pytest.mark.part1
@pytest.mark.edge
def test_huge_number(impl):
    assert impl.is_happy_set(10 ** 300) is True  # digits: one 1 and zeros
    assert impl.is_happy_set(2 * 10 ** 300) is False  # reduces to 4


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("bad", [0, -7])
def test_non_positive_raises(impl, bad):
    with pytest.raises(ValueError):
        impl.is_happy_set(bad)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize("n,expected", [(19, True), (2, False), (1, True), (116, False), (100, True)])
def test_worked_examples_floyd(impl, n, expected):
    assert impl.is_happy_floyd(n) is expected


@pytest.mark.part2
@pytest.mark.edge
def test_floyd_agrees_with_set_on_range(impl):
    rng = random.Random(0)
    for n in list(range(1, 3000)) + [rng.randint(1, 10 ** 18) for _ in range(2000)]:
        assert impl.is_happy_floyd(n) == impl.is_happy_set(n), n


@pytest.mark.part2
@pytest.mark.edge
def test_floyd_builds_no_set_or_dict(impl, monkeypatch):
    monkeypatch.setattr(impl, "set", _forbidden, raising=False)
    monkeypatch.setattr(impl, "dict", _forbidden, raising=False)
    for n in (2, 4, 19, 116, 10 ** 50 + 3):
        impl.is_happy_floyd(n)


@pytest.mark.part2
@pytest.mark.edge
def test_floyd_peak_memory_is_tiny(impl):
    tracemalloc.start()
    try:
        for n in range(1, 2000):
            impl.is_happy_floyd(n)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert peak < 16_000, f"peak {peak} bytes"


@pytest.mark.part2
@pytest.mark.edge
def test_floyd_non_positive_raises(impl):
    with pytest.raises(ValueError):
        impl.is_happy_floyd(0)


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_examples(impl):
    assert impl.cycle_info(19) == (1, 1)
    assert impl.cycle_info(2) == (8, 4)          # the classic unhappy cycle 4 → 16 → … → 20 → 4
    assert impl.cycle_info(153, 10, 3) == (1, 153)  # Armstrong number: fixed point
    assert impl.cycle_info(5, 2, 2) == (1, 1)     # in base 2 every number is happy


@pytest.mark.part3
@pytest.mark.edge
def test_part3_against_brute_force(impl):
    rng = random.Random(1)
    for _ in range(1500):
        n, b, p = rng.randint(1, 10 ** 6), rng.randint(2, 16), rng.randint(1, 4)
        assert impl.cycle_info(n, b, p) == _brute_cycle(_digit_power_step, n, b, p), (n, b, p)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_invalid_base_or_power(impl):
    with pytest.raises(ValueError):
        impl.cycle_info(10, 1, 2)
    with pytest.raises(ValueError):
        impl.cycle_info(10, 10, 0)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_queries(run_script):
    rng = random.Random(0)
    body = "\n".join(str(rng.randint(1, 10 ** 12)) for _ in range(100_000))
    r = run_script("PART 2\n" + body + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n19\n2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\nfalse\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n7\n116\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\nfalse\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n2 10 2\n153 10 3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "8 4\n1 153\n"
