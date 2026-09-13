import random
import time

import pytest

VOWELS = "aeiou"
MOD = 1_000_000_007


def brute_count(n: int, k: int) -> int:
    """O(26^n) brute force for tiny n, used to cross-check the DP on small cases."""
    if n == 0:
        return 1
    total = 0
    for i in range(26 ** n):
        s = []
        x = i
        for _ in range(n):
            s.append(x % 26)
            x //= 26
        letters = "".join(chr(ord("a") + c) for c in s)
        run = 0
        ok = True
        for ch in letters:
            if ch in VOWELS:
                run += 1
                if run > k:
                    ok = False
                    break
            else:
                run = 0
        if ok:
            total += 1
    return total


# ---------------------------------------------------------------- Part 1: exact count, no mod
@pytest.mark.part1
def test_worked_example_no_vowels_allowed(impl):
    assert impl.part1(1, 0) == 21


@pytest.mark.part1
def test_worked_example_any_letter(impl):
    assert impl.part1(1, 1) == 26
    assert impl.part1(1, 5) == 26


@pytest.mark.part1
@pytest.mark.edge
def test_empty_string_length_zero(impl):
    assert impl.part1(0, 0) == 1
    assert impl.part1(0, 3) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_k_at_least_n_is_unconstrained(impl):
    assert impl.part1(3, 3) == 26 ** 3
    assert impl.part1(3, 10) == 26 ** 3


@pytest.mark.part1
def test_matches_brute_force_small_cases(impl):
    for n in range(0, 4):
        for k in range(0, 4):
            assert impl.part1(n, k) == brute_count(n, k), (n, k)


@pytest.mark.part1
@pytest.mark.edge
def test_no_mod_stays_exact_big_int(impl):
    # sanity: part1 must NOT be modded -- for n large enough that mod would visibly truncate,
    # the result must exceed MOD and not equal part2's modded value except by chance at 0.
    n, k = 30, 30  # unconstrained -> 26**30, astronomically larger than 1e9+7
    assert impl.part1(n, k) == 26 ** n


# ---------------------------------------------------------------- Part 2: mod 1e9+7, large n
@pytest.mark.part2
def test_worked_examples_fastprep(impl):
    assert impl.part2(1, 1) == 26
    assert impl.part2(4, 1) == 412776
    assert impl.part2(4, 2) == 451101


@pytest.mark.part2
def test_part1_part2_agree_on_small_cases(impl):
    assert impl.part1(4, 1) == impl.part2(4, 1) == 412776
    assert impl.part1(4, 2) == impl.part2(4, 2) == 451101


@pytest.mark.part2
@pytest.mark.edge
def test_zero_word_len(impl):
    assert impl.part2(0, 0) == 1
    assert impl.part2(0, 5) == 1


@pytest.mark.part2
@pytest.mark.edge
def test_zero_max_vowels(impl):
    # no vowels allowed at all -> 21**word_len mod
    assert impl.part2(5, 0) == pow(21, 5, MOD)


@pytest.mark.part2
@pytest.mark.edge
def test_max_vowels_at_least_word_len(impl):
    assert impl.part2(6, 6) == pow(26, 6, MOD)
    assert impl.part2(6, 100) == pow(26, 6, MOD)


@pytest.mark.part2
@pytest.mark.perf
def test_perf_word_len_2500(impl):
    t0 = time.perf_counter()
    result = impl.part2(2500, 2500)
    elapsed = time.perf_counter() - t0
    assert 0 <= result < MOD
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


@pytest.mark.part2
@pytest.mark.perf
def test_perf_word_len_2500_small_max_vowels(impl):
    t0 = time.perf_counter()
    result = impl.part2(2500, 3)
    elapsed = time.perf_counter() - t0
    assert 0 <= result < MOD
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


# ---------------------------------------------------------------- Part 3: all-vowel substrings
@pytest.mark.part3
def test_worked_example_single_run_exact(impl):
    assert impl.part3("aeiou") == 1


@pytest.mark.part3
def test_worked_example_extra_trailing_vowel(impl):
    assert impl.part3("aeiouu") == 2


@pytest.mark.part3
def test_worked_example_trailing_consonant(impl):
    assert impl.part3("aeioub") == 1


@pytest.mark.part3
def test_worked_example_two_runs(impl):
    assert impl.part3("aeioubaeiou") == 2


@pytest.mark.part3
@pytest.mark.edge
def test_no_vowels_at_all(impl):
    assert impl.part3("xyz") == 0


@pytest.mark.part3
@pytest.mark.edge
def test_consonant_splits_run_before_all_five_seen(impl):
    # 'b' breaks "aeio" + "u" into two runs, neither contains all 5 vowels
    assert impl.part3("aeiobu") == 0


@pytest.mark.part3
@pytest.mark.edge
def test_empty_string(impl):
    assert impl.part3("") == 0


@pytest.mark.part3
@pytest.mark.edge
def test_missing_one_vowel_never_counts(impl):
    assert impl.part3("aeio" * 5) == 0  # never contains 'u'


@pytest.mark.part3
@pytest.mark.edge
def test_repeated_vowels_before_and_after_completion(impl):
    # "aaeiou": run is one block; all-5 first achieved at index 4 (0-based 'u'), last-seen
    # mins: a=1 (last a), e=2, i=3, o=4, u=5 at j=5 -> min=1 -> contributes 2 (j=4: min(a=1,...)=1->2;
    # j=5: min still a=1 -> +2) total 4. Verified by direct trace, not brute force, so cross-check
    # against brute force below for extra confidence.
    s = "aaeiou"
    assert impl.part3(s) == brute_part3(s)


def brute_part3(s: str) -> int:
    n = len(s)
    total = 0
    for i in range(n):
        for j in range(i, n):
            sub = s[i : j + 1]
            if all(ch in VOWELS for ch in sub) and set(sub) == set(VOWELS):
                total += 1
    return total


@pytest.mark.part3
def test_matches_brute_force_random_short_strings(impl):
    rng = random.Random(0)
    alphabet = "aeioubcd"
    for _ in range(30):
        length = rng.randrange(0, 12)
        s = "".join(rng.choice(alphabet) for _ in range(length))
        assert impl.part3(s) == brute_part3(s), s


@pytest.mark.part3
@pytest.mark.perf
def test_perf_long_random_vowel_heavy_string(impl):
    rng = random.Random(0)
    alphabet = list("aeiou") * 8 + list("bcdfg")  # vowel-heavy, so runs get long
    s = "".join(rng.choice(alphabet) for _ in range(1_000_000))
    t0 = time.perf_counter()
    result = impl.part3(s)
    elapsed = time.perf_counter() - t0
    assert result >= 0
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_io_part1(run_script):
    r = run_script("PART 1\n1 0\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "21\n"


@pytest.mark.part2
@pytest.mark.io
def test_io_part2(run_script):
    r = run_script("PART 2\n4 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "412776\n"


@pytest.mark.part3
@pytest.mark.io
def test_io_part3(run_script):
    r = run_script("PART 3\naeiouu\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2\n"


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.edge
def test_io_part3_empty_payload_line(run_script):
    r = run_script("PART 3\n\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.edge
def test_io_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0
    assert r.stdout == ""
