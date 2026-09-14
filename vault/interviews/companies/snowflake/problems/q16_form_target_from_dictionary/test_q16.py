import random
import string
from itertools import combinations

import pytest

MOD = 1_000_000_007


def _brute_count(words, target):
    """Enumerate every strictly-increasing choice of n columns out of m via
    itertools.combinations and multiply per-column character counts -- pure
    combinatorics, independent of the DP recurrence under test."""
    m = len(words[0])
    n = len(target)
    cnt = [[0] * 26 for _ in range(m)]
    for w in words:
        for j, ch in enumerate(w):
            cnt[j][ord(ch) - 97] += 1
    total = 0
    for combo in combinations(range(m), n):
        ways = 1
        for i, col in enumerate(combo):
            c = cnt[col][ord(target[i]) - 97]
            if c == 0:
                ways = 0
                break
            ways *= c
        total += ways
    return total % MOD


def _brute_assignment(words, target):
    """itertools.combinations(range(m), n) yields index tuples in lexicographic
    order, so the first combo whose columns all contain the needed character is
    the lexicographically smallest -- an independent check of the greedy."""
    m = len(words[0])
    n = len(target)
    col_chars = [set(w[j] for w in words) for j in range(m)]
    for combo in combinations(range(m), n):
        if all(target[i] in col_chars[combo[i]] for i in range(n)):
            return list(combo)
    return []


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "words,target,expected",
    [
        (["acca", "bbbb", "caca"], "aba", 6),          # LC1639 example 1
        (["abba", "baab"], "bab", 4),                  # LC1639 example 2
        (["abcd"], "abcd", 1),                         # LC1639 example 3
        (["abab", "baba", "abba", "baab"], "abba", 16),  # LC1639 example 4
    ],
)
def test_worked_examples(impl, words, target, expected):
    assert impl.num_ways_to_form_target(words, target) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_target_shorter_than_words(impl):
    # words are length 4, target length 1: any column with a 'z' anywhere works
    assert impl.num_ways_to_form_target(["zzzz"], "z") == 4


@pytest.mark.part1
@pytest.mark.edge
def test_no_way_to_form_target(impl):
    assert impl.num_ways_to_form_target(["aaa"], "b") == 0


@pytest.mark.part1
@pytest.mark.edge
def test_single_word_single_char(impl):
    assert impl.num_ways_to_form_target(["a"], "a") == 1


@pytest.mark.part1
@pytest.mark.edge
def test_column_reuse_is_forbidden(impl):
    # "aaa" has 3 columns all 'a'; forming "aa" must use two DISTINCT columns, so
    # it's C(3,2) = 3 ways, not (say) 3*3=9 if a column could be reused for both
    # positions of the target.
    assert impl.num_ways_to_form_target(["aaa"], "aa") == 3


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize(
    "words,target",
    [
        ([], "a"),           # empty words
        (["ab"], ""),        # empty target
        (["ab", "abc"], "a"),  # words not all the same length
        (["ab"], "abc"),     # target longer than words
        (["Ab"], "a"),        # non-lowercase word
        (["ab"], "A"),        # non-lowercase target
    ],
)
def test_invalid_input_raises(impl, words, target):
    with pytest.raises(ValueError):
        impl.num_ways_to_form_target(words, target)


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_combinatorial_brute_force(impl):
    rng = random.Random(0)
    alphabet = "ab"
    for _ in range(150):
        m = rng.randint(1, 6)
        n = rng.randint(1, m)
        num_words = rng.randint(1, 4)
        words = ["".join(rng.choice(alphabet) for _ in range(m)) for _ in range(num_words)]
        target = "".join(rng.choice(alphabet) for _ in range(n))
        assert impl.num_ways_to_form_target(words, target) == _brute_count(words, target), (
            words,
            target,
        )


@pytest.mark.part1
@pytest.mark.perf
def test_perf_part1_1000(run_script):
    rng = random.Random(0)
    m = 1000
    words = ["".join(rng.choice(string.ascii_lowercase[:4]) for _ in range(m)) for _ in range(1000)]
    target = "".join(rng.choice(string.ascii_lowercase[:4]) for _ in range(m))
    body = "\n".join(words)
    r = run_script(f"PART 1\n{len(words)}\n{body}\n{target}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert 0 <= int(r.stdout) < MOD
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize(
    "words,target,expected",
    [
        (["acca", "bbbb", "caca"], "aba", [0, 1, 3]),
        (["abba", "baab"], "bab", [0, 1, 2]),
        (["abcd"], "abcd", [0, 1, 2, 3]),
    ],
)
def test_part2_worked_examples(impl, words, target, expected):
    assert impl.smallest_column_assignment(words, target) == expected


@pytest.mark.part2
@pytest.mark.edge
def test_part2_impossible_returns_empty(impl):
    assert impl.smallest_column_assignment(["aaa"], "aab") == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_ties_prefer_smallest_columns(impl):
    # "z" appears at every column of "zzzz" -- must pick column 0, the smallest.
    assert impl.smallest_column_assignment(["zzzz"], "zz") == [0, 1]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_random_against_combinatorial_brute_force(impl):
    rng = random.Random(1)
    alphabet = "ab"
    for _ in range(150):
        m = rng.randint(1, 6)
        n = rng.randint(1, m)
        num_words = rng.randint(1, 4)
        words = ["".join(rng.choice(alphabet) for _ in range(m)) for _ in range(num_words)]
        target = "".join(rng.choice(alphabet) for _ in range(n))
        assert impl.smallest_column_assignment(words, target) == _brute_assignment(words, target), (
            words,
            target,
        )


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_1000(run_script):
    rng = random.Random(1)
    m = 1000
    words = ["".join(rng.choice(string.ascii_lowercase[:4]) for _ in range(m)) for _ in range(1000)]
    target = "".join(rng.choice(string.ascii_lowercase[:4]) for _ in range(m))
    body = "\n".join(words)
    r = run_script(f"PART 2\n{len(words)}\n{body}\n{target}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n3\nacca\nbbbb\ncaca\naba\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "6\n"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n3\nacca\nbbbb\ncaca\naba\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0,1,3\n"
