import random

import pytest


def _brute_is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def _brute_min_add(s):
    """O(n) two-pass counting re-implementation, independent of the single-pass builder."""
    open_needed = 0
    unmatched_close = 0
    for ch in s:
        if ch == "(":
            open_needed += 1
        elif open_needed > 0:
            open_needed -= 1
        else:
            unmatched_close += 1
    return unmatched_close + open_needed


def _brute_longest_valid(s):
    """O(n^2) brute force: check every substring for validity, longest & leftmost wins."""
    n = len(s)
    best_len, best_start = 0, 0
    for i in range(n):
        depth = 0
        for j in range(i, n):
            depth += 1 if s[j] == "(" else -1
            if depth < 0:
                break
            if depth == 0 and (j - i + 1) > best_len:
                best_len = j - i + 1
                best_start = i
    return best_len, best_start


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "s,expected",
    [("()", True), ("()[]{}", True), ("(]", False), ("([)]", False), ("{[]}", True), ("", True)],
)
def test_worked_examples(impl, s, expected):
    assert impl.is_valid(s) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_only_opening(impl):
    assert impl.is_valid("(((") is False


@pytest.mark.part1
@pytest.mark.edge
def test_only_closing(impl):
    assert impl.is_valid(")))") is False


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_character_raises(impl):
    with pytest.raises(ValueError):
        impl.is_valid("(a)")


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_brute_force(impl):
    rng = random.Random(0)
    for _ in range(500):
        s = "".join(rng.choice("()[]{}") for _ in range(rng.randint(0, 10)))
        assert impl.is_valid(s) == _brute_is_valid(s), s


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_500000_chars(run_script):
    rng = random.Random(0)
    s = "".join(rng.choice("()[]{}") for _ in range(500_000))
    r = run_script("PART 1\n" + s + "\n", timeout=10)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize(
    "s,expected",
    [("())", (1, "()()")), ("(((", (3, "((()))")), ("()", (0, "()")), (")(", (2, "()()")), ("", (0, ""))],
)
def test_part2_worked_examples(impl, s, expected):
    assert impl.min_add_to_make_valid(s) == expected


@pytest.mark.part2
@pytest.mark.edge
def test_part2_invalid_character_raises(impl):
    with pytest.raises(ValueError):
        impl.min_add_to_make_valid("([)")


@pytest.mark.part2
@pytest.mark.edge
def test_part2_count_matches_independent_formula_and_result_is_valid(impl):
    rng = random.Random(1)
    for _ in range(500):
        s = "".join(rng.choice("()") for _ in range(rng.randint(0, 15)))
        n, out = impl.min_add_to_make_valid(s)
        assert n == _brute_min_add(s), s
        assert len(out) == len(s) + n
        assert _brute_is_valid(out)
        # the result must contain s as a subsequence (only insertions, no deletions/reorders)
        it = iter(out)
        assert all(ch in it for ch in s)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_500000_chars(run_script):
    rng = random.Random(0)
    s = "".join(rng.choice("()") for _ in range(500_000))
    r = run_script("PART 2\n" + s + "\n", timeout=10)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
@pytest.mark.parametrize(
    "s,expected",
    [
        ("(()", (2, 1)),
        (")()())", (4, 1)),
        ("", (0, 0)),
        ("()(()", (2, 0)),
        ("()(())", (6, 0)),
    ],
)
def test_part3_worked_examples(impl, s, expected):
    assert impl.longest_valid_substring(s) == expected


@pytest.mark.part3
@pytest.mark.edge
def test_part3_no_valid_substring(impl):
    assert impl.longest_valid_substring(")))") == (0, 0)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_invalid_character_raises(impl):
    with pytest.raises(ValueError):
        impl.longest_valid_substring("[()]")


@pytest.mark.part3
@pytest.mark.edge
def test_part3_leftmost_on_tie(impl):
    # two disjoint length-2 valid runs -> leftmost wins
    length, start = impl.longest_valid_substring("()x()".replace("x", ")("))
    assert (length, start) == (2, 0)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_matches_brute_force_length_and_validity(impl):
    rng = random.Random(2)
    for _ in range(300):
        s = "".join(rng.choice("()") for _ in range(rng.randint(0, 12)))
        length, start = impl.longest_valid_substring(s)
        brute_len, _ = _brute_longest_valid(s)
        assert length == brute_len, s
        if length:
            assert _brute_is_valid(s[start : start + length])
            # leftmost: no valid substring of the same length starts earlier
            assert not _brute_is_valid(s[start - 1 : start - 1 + length]) if start > 0 else True


@pytest.mark.part3
@pytest.mark.perf
def test_perf_part3_500000_chars(run_script):
    rng = random.Random(0)
    s = "".join(rng.choice("()") for _ in range(500_000))
    r = run_script("PART 3\n" + s + "\n", timeout=10)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n()\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n())\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "1\n()()\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n)()())\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "4 1\n"
