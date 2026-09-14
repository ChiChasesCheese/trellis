import random

import pytest

LINES = ["a", "b", "ERR_x", "c", "d", "e", "ERR_y", "f", "g"]


def _brute_grep(lines, target, around):
    n = len(lines)
    keep = [False] * n
    for i, line in enumerate(lines):
        if target in line:
            for j in range(max(0, i - around), min(n - 1, i + around) + 1):
                keep[j] = True
    return [l for i, l in enumerate(lines) if keep[i]]


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_examples_part1(impl):
    assert impl.grep(LINES, "ERR", 1) == ["b", "ERR_x", "c", "e", "ERR_y", "f"]
    assert impl.grep(LINES, "ERR", 0) == ["ERR_x", "ERR_y"]
    assert impl.grep(LINES, "ERR", 5) == LINES


@pytest.mark.part1
@pytest.mark.edge
def test_no_matches(impl):
    assert impl.grep(["a", "b", "c"], "ERR", 2) == []


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input(impl):
    assert impl.grep([], "ERR", 2) == []


@pytest.mark.part1
@pytest.mark.edge
def test_match_is_its_own_context(impl):
    assert impl.grep(["ERR"], "ERR", 0) == ["ERR"]


@pytest.mark.part1
@pytest.mark.edge
def test_overlapping_windows_no_duplicates(impl):
    lines = ["ERR1", "x", "ERR2"]  # windows [0,1] and [1,2] overlap at index 1
    result = impl.grep(lines, "ERR", 1)
    assert result == ["ERR1", "x", "ERR2"]
    assert len(result) == len(set(range(len(result))))  # no line index emitted twice


@pytest.mark.part1
@pytest.mark.edge
def test_negative_around_raises(impl):
    with pytest.raises(ValueError):
        impl.grep(LINES, "ERR", -1)


@pytest.mark.part1
@pytest.mark.edge
def test_agrees_with_brute_force_random(impl):
    rng = random.Random(0)
    for _ in range(300):
        n = rng.randint(0, 15)
        lines = [f"x{rng.randint(0,3)}" if rng.random() < 0.7 else f"ERR{rng.randint(0,3)}" for _ in range(n)]
        around = rng.randint(0, 5)
        assert impl.grep(lines, "ERR", around) == _brute_grep(lines, "ERR", around), (lines, around)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_worked_examples_part2(impl):
    assert impl.grep_grouped(LINES, "ERR", 1, 2) == ["b", "ERR_x", "c", "d", "e", "ERR_y", "f", "g"]
    assert impl.grep_grouped(LINES, "ERR", 0, 0) == ["ERR_x", "--", "ERR_y"]


@pytest.mark.part2
@pytest.mark.edge
def test_no_leading_or_trailing_separator(impl):
    result = impl.grep_grouped(LINES, "ERR", 0, 0)
    assert result[0] != "--"
    assert result[-1] != "--"


@pytest.mark.part2
@pytest.mark.edge
def test_single_match_no_separator(impl):
    assert impl.grep_grouped(["a", "ERR", "b"], "ERR", 1, 1) == ["a", "ERR", "b"]


@pytest.mark.part2
@pytest.mark.edge
def test_negative_before_after_raises(impl):
    with pytest.raises(ValueError):
        impl.grep_grouped(LINES, "ERR", -1, 0)
    with pytest.raises(ValueError):
        impl.grep_grouped(LINES, "ERR", 0, -1)


@pytest.mark.part2
@pytest.mark.edge
def test_asymmetric_before_after(impl):
    lines = ["a", "b", "c", "ERR", "d", "e", "f"]
    assert impl.grep_grouped(lines, "ERR", 2, 1) == ["b", "c", "ERR", "d"]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_stream_matches_batch_worked_examples(impl):
    assert list(impl.grep_stream(iter(LINES), "ERR", 1)) == impl.grep(LINES, "ERR", 1)
    assert list(impl.grep_stream(iter(LINES), "ERR", 0)) == impl.grep(LINES, "ERR", 0)


@pytest.mark.part3
@pytest.mark.edge
def test_stream_empty(impl):
    assert list(impl.grep_stream(iter([]), "ERR", 2)) == []


@pytest.mark.part3
@pytest.mark.edge
def test_stream_negative_raises(impl):
    with pytest.raises(ValueError):
        list(impl.grep_stream(iter(LINES), "ERR", -1))


@pytest.mark.part3
def test_stream_agrees_with_batch_random(impl):
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(0, 15)
        lines = [f"x{rng.randint(0,3)}" if rng.random() < 0.7 else f"ERR{rng.randint(0,3)}" for _ in range(n)]
        around = rng.randint(0, 5)
        expected = impl.grep(lines, "ERR", around)
        got = list(impl.grep_stream(iter(lines), "ERR", around))
        assert got == expected, (lines, around)


@pytest.mark.part3
@pytest.mark.edge
def test_stream_only_consumes_iterator_once(impl):
    """A real one-pass iterator (not a list) must work -- guards against secretly calling
    list(lines) and reusing Part1's implementation."""
    def gen():
        yield from LINES

    assert list(impl.grep_stream(gen(), "ERR", 1)) == impl.grep(LINES, "ERR", 1)


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_input(run_script):
    rng = random.Random(0)
    n = 200_000
    body_lines = []
    for i in range(n):
        body_lines.append("ERR" if i % 5000 == 0 else f"line{i}")
    body = "\n".join(body_lines)
    stdin = f"PART 1\nN {n}\n{body}\nQ ERR 2\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    body = "\n".join(LINES)
    r = run_script(f"PART 1\nN 9\n{body}\nQ ERR 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "b\nERR_x\nc\ne\nERR_y\nf\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    body = "\n".join(LINES)
    r = run_script(f"PART 2\nN 9\n{body}\nQ ERR 0 0\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ERR_x\n--\nERR_y\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    body = "\n".join(LINES)
    r = run_script(f"PART 3\nN 9\n{body}\nQ ERR 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "b\nERR_x\nc\ne\nERR_y\nf\n"
