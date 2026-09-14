import random
import string
import time

import pytest


def _brute(s):
    """Assign every index to {skip, seq1, seq2} by recursion (O(3^n), a different
    code path from the bitmask-submask trick under test) and check palindromes at
    the leaves."""
    n = len(s)
    best = 0

    def rec(i, seq1, seq2):
        nonlocal best
        if i == n:
            if seq1 == seq1[::-1] and seq2 == seq2[::-1]:
                best = max(best, len(seq1) * len(seq2))
            return
        rec(i + 1, seq1, seq2)
        rec(i + 1, seq1 + s[i], seq2)
        rec(i + 1, seq1, seq2 + s[i])

    rec(0, "", "")
    return best


def _check_pair(s, idx1, idx2, expected_product):
    """Validate a Part2 answer: disjoint, in range, ascending, both palindromes,
    and the product matches the Part1 maximum (any optimal pair is accepted)."""
    assert idx1 == sorted(idx1) and idx2 == sorted(idx2), "indices must be ascending"
    assert len(set(idx1)) == len(idx1) and len(set(idx2)) == len(idx2), "no repeats within a list"
    assert set(idx1).isdisjoint(idx2), "the two index sets must be disjoint"
    for i in idx1 + idx2:
        assert 0 <= i < len(s), f"index out of range: {i}"
    sub1 = "".join(s[i] for i in idx1)
    sub2 = "".join(s[i] for i in idx2)
    assert sub1 == sub1[::-1], f"{sub1!r} is not a palindrome"
    assert sub2 == sub2[::-1], f"{sub2!r} is not a palindrome"
    assert len(sub1) * len(sub2) == expected_product


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "s,expected",
    [
        ("leetcodecom", 9),   # LC2002 example 1
        ("bb", 1),            # LC2002 example 2
        ("accbcaxxcxx", 25),  # LC2002 example 3
    ],
)
def test_worked_examples(impl, s, expected):
    assert impl.max_product_two_palindromic_subsequences(s) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_minimum_length_two_distinct_chars(impl):
    assert impl.max_product_two_palindromic_subsequences("ab") == 1


@pytest.mark.part1
@pytest.mark.edge
def test_all_same_character(impl):
    # n=12, all 'a': best split is 6/6 -> every subset is a palindrome.
    assert impl.max_product_two_palindromic_subsequences("a" * 12) == 36


@pytest.mark.part1
@pytest.mark.edge
def test_whole_string_is_a_palindrome(impl):
    # "abcba" itself is a palindrome (len 5) but must be split into two DISJOINT
    # pieces -- can't just take the whole thing as one side.
    result = impl.max_product_two_palindromic_subsequences("abcba")
    assert result >= 1
    assert result == _brute("abcba")


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "s",
    ["", "a", "a" * 13, "AB", "ab1", "abÿ"],
)
def test_invalid_input_raises(impl, s):
    with pytest.raises(ValueError):
        impl.max_product_two_palindromic_subsequences(s)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_recursive_brute_force(impl):
    rng = random.Random(0)
    alphabet = "abc"
    for _ in range(120):
        n = rng.randint(2, 8)
        s = "".join(rng.choice(alphabet) for _ in range(n))
        assert impl.max_product_two_palindromic_subsequences(s) == _brute(s), s


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_n12(run_script):
    # n is capped at 12 by the problem itself -- the "large input" IS the constraint
    # boundary: the worst case for the O(3^n) submask enumeration.
    rng = random.Random(0)
    s = "".join(rng.choice(string.ascii_lowercase[:4]) for _ in range(12))
    t0 = time.perf_counter()
    r = run_script(f"PART 1\n{s}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"
    assert time.perf_counter() - t0 < 5.0


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize("s", ["leetcodecom", "bb", "accbcaxxcxx", "ab", "a" * 12, "abcba"])
def test_part2_pair_is_valid_and_optimal(impl, s):
    expected = impl.max_product_two_palindromic_subsequences(s)
    idx1, idx2 = impl.max_product_with_subsequences(s)
    _check_pair(s, idx1, idx2, expected)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_random_against_recursive_brute_force(impl):
    rng = random.Random(1)
    alphabet = "ab"
    for _ in range(60):
        n = rng.randint(2, 8)
        s = "".join(rng.choice(alphabet) for _ in range(n))
        expected = _brute(s)
        idx1, idx2 = impl.max_product_with_subsequences(s)
        _check_pair(s, idx1, idx2, expected)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_invalid_input_raises(impl):
    with pytest.raises(ValueError):
        impl.max_product_with_subsequences("")
    with pytest.raises(ValueError):
        impl.max_product_with_subsequences("a" * 13)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_n12(run_script):
    rng = random.Random(1)
    s = "".join(rng.choice(string.ascii_lowercase[:4]) for _ in range(12))
    r = run_script(f"PART 2\n{s}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() != ""
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nleetcodecom\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "9\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nbb\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert len(lines) == 2
    idx1 = [int(x) for x in lines[0].split(",") if x]
    idx2 = [int(x) for x in lines[1].split(",") if x]
    _check_pair("bb", idx1, idx2, 1)
