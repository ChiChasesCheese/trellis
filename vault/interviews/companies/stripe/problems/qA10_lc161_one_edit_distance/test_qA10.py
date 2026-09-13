import random
import time

import pytest


def _levenshtein(a, b):
    """Full O(n*m) reference (small strings only)."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _rand(rng, alphabet="ab", hi=7):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, hi)))


# ---------------------------------------------------------------- Part 1: LC 161
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.is_one_edit_distance("ab", "acb") is True
    assert impl.is_one_edit_distance("", "") is False
    assert impl.is_one_edit_distance("a", "") is True
    assert impl.is_one_edit_distance("cab", "ad") is False


@pytest.mark.part1
@pytest.mark.edge
def test_identical_and_length_boundaries(impl):
    assert impl.is_one_edit_distance("abc", "abc") is False   # zero edits
    assert impl.is_one_edit_distance("abc", "abcd") is True   # length diff 1
    assert impl.is_one_edit_distance("abc", "abcde") is False  # length diff 2
    assert impl.is_one_edit_distance("", "a") is True
    assert impl.is_one_edit_distance("", "ab") is False
    assert impl.is_one_edit_distance("a", "b") is True


@pytest.mark.part1
@pytest.mark.edge
def test_mismatch_positions(impl):
    assert impl.is_one_edit_distance("abc", "abx") is True    # last char replaced
    assert impl.is_one_edit_distance("abc", "xbc") is True    # first char replaced
    assert impl.is_one_edit_distance("abc", "axx") is False   # two replaced
    assert impl.is_one_edit_distance("abc", "xabc") is True   # inserted at the front
    assert impl.is_one_edit_distance("abc", "abxc") is True   # inserted in the middle
    assert impl.is_one_edit_distance("abc", "acbd") is False  # extra char not at the first mismatch
    assert impl.is_one_edit_distance("ab", "ba") is False     # a swap is two replaces in Part 1


@pytest.mark.part1
def test_part1_matches_levenshtein_eq_1(impl):
    rng = random.Random(0)
    for _ in range(2000):
        a, b = _rand(rng), _rand(rng)
        assert impl.is_one_edit_distance(a, b) is (_levenshtein(a, b) == 1), (a, b)


# ---------------------------------------------------------------- Part 2: swap
@pytest.mark.part2
def test_swap_examples(impl):
    assert impl.is_one_edit_or_swap("ab", "ba") is True
    assert impl.is_one_edit_or_swap("abcd", "abdc") is True
    assert impl.is_one_edit_or_swap("aa", "aa") is False
    assert impl.is_one_edit_or_swap("abc", "bca") is False
    assert impl.is_one_edit_or_swap("ab", "acb") is True


@pytest.mark.part2
@pytest.mark.edge
def test_swap_boundaries(impl):
    assert impl.is_one_edit_or_swap("abcd", "bacd") is True    # swap at the front
    assert impl.is_one_edit_or_swap("abcd", "abdc") is True    # swap at the end
    assert impl.is_one_edit_or_swap("abcd", "badc") is False   # two swaps
    assert impl.is_one_edit_or_swap("abcd", "acbd") is True
    assert impl.is_one_edit_or_swap("abcd", "cbad") is False   # non-adjacent transposition
    assert impl.is_one_edit_or_swap("", "") is False
    assert impl.is_one_edit_or_swap("a", "a") is False


@pytest.mark.part2
def test_swap_is_card_typo_rule(impl):
    # q05 Part 4: 4111111111111111 with two adjacent digits swapped or one digit changed
    card = "4111111111111111"
    assert impl.is_one_edit_or_swap(card, "4111111111111112") is True
    assert impl.is_one_edit_or_swap(card, "1411111111111111") is True   # '4','1' swapped
    assert impl.is_one_edit_or_swap(card, "1141111111111111") is False  # moved two places
    assert impl.is_one_edit_or_swap(card, card) is False


# ---------------------------------------------------------------- Part 3: name the edit
@pytest.mark.part3
def test_find_edit_examples(impl):
    E = impl.Edit
    assert impl.find_edit("ab", "acb") == E("insert", 1, "c")
    assert impl.find_edit("acb", "ab") == E("delete", 1, "")
    assert impl.find_edit("abc", "axc") == E("replace", 1, "x")
    assert impl.find_edit("abc", "bac") == E("swap", 0, "")
    assert impl.find_edit("aa", "aaa") == E("insert", 2, "a")
    assert impl.find_edit("abc", "abc") is None
    assert impl.find_edit("abc", "bca") is None


@pytest.mark.part3
@pytest.mark.edge
def test_find_edit_first_mismatch_and_ends(impl):
    E = impl.Edit
    assert impl.find_edit("", "a") == E("insert", 0, "a")
    assert impl.find_edit("a", "") == E("delete", 0, "")
    assert impl.find_edit("aaa", "aa") == E("delete", 2, "")     # first mismatch is the end
    assert impl.find_edit("abc", "abcd") == E("insert", 3, "d")
    assert impl.find_edit("abc", "zabc") == E("insert", 0, "z")
    assert impl.find_edit("abcd", "abdc") == E("swap", 2, "")
    assert impl.find_edit("", "") is None
    assert impl.find_edit("ab", "abcd") is None


@pytest.mark.part3
def test_find_edit_applies_back_to_t(impl):
    def apply(s, e):
        if e.kind == "insert":
            return s[: e.index] + e.char + s[e.index:]
        if e.kind == "delete":
            return s[: e.index] + s[e.index + 1:]
        if e.kind == "replace":
            return s[: e.index] + e.char + s[e.index + 1:]
        return s[: e.index] + s[e.index + 1] + s[e.index] + s[e.index + 2:]

    rng = random.Random(1)
    for _ in range(2000):
        a, b = _rand(rng, "abc"), _rand(rng, "abc")
        e = impl.find_edit(a, b)
        assert (e is not None) is impl.is_one_edit_or_swap(a, b)
        if e is not None:
            assert apply(a, e) == b, (a, b, e)


# ---------------------------------------------------------------- Part 4: within k
@pytest.mark.part4
def test_within_k_examples(impl):
    assert impl.within_k_edits("kitten", "sitting", 3) is True
    assert impl.within_k_edits("kitten", "sitting", 2) is False
    assert impl.within_k_edits("abc", "abc", 0) is True
    assert impl.within_k_edits("abc", "abd", 0) is False
    assert impl.within_k_edits("flaw", "lawn", 2) is True
    assert impl.within_k_edits("flaw", "lawn", 1) is False


@pytest.mark.part4
@pytest.mark.edge
def test_within_k_boundaries(impl):
    assert impl.within_k_edits("", "", 0) is True
    assert impl.within_k_edits("", "abc", 3) is True
    assert impl.within_k_edits("", "abc", 2) is False        # length difference > k
    assert impl.within_k_edits("abc", "", 3) is True
    assert impl.within_k_edits("abcdef", "abcdef", 0) is True
    # k = 1 is exactly "equal or one edit"
    for a, b in [("ab", "acb"), ("ab", "ab"), ("ab", "ba"), ("a", ""), ("cab", "ad")]:
        assert impl.within_k_edits(a, b, 1) is (a == b or impl.is_one_edit_distance(a, b))


@pytest.mark.part4
def test_within_k_matches_full_levenshtein(impl):
    rng = random.Random(2)
    for _ in range(3000):
        a, b = _rand(rng, "abc", 8), _rand(rng, "abc", 8)
        k = rng.randint(0, 5)
        assert impl.within_k_edits(a, b, k) is (_levenshtein(a, b) <= k), (a, b, k)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\nab\nacb\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "true\n"
    assert run_script("PART 1\n\n\n").stdout == "false\n"      # two empty strings
    assert run_script("PART 1\na\n").stdout == "true\n"         # absent line = empty t
    assert run_script("PART 2\nab\nba\n").stdout == "true\n"
    assert run_script("PART 3\nab\nacb\n").stdout == "insert 1 c\n"
    assert run_script("PART 3\nacb\nab\n").stdout == "delete 1\n"
    assert run_script("PART 3\nabc\nbac\n").stdout == "swap 0\n"
    assert run_script("PART 3\nabc\nabc\n").stdout == "none\n"
    assert run_script("PART 4\nK 2\nkitten\nsitting\n").stdout == "false\n"
    assert run_script("PART 4\nK 3\nkitten\nsitting\n").stdout == "true\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max(impl, run_script):
    rng = random.Random(0)
    base = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(10_000))
    edited = base[:5000] + "Z" + base[5001:]
    t0 = time.perf_counter()
    for _ in range(50):
        assert impl.is_one_edit_distance(base, edited) is True
        assert impl.is_one_edit_or_swap(base, base[:5000] + base[5001] + base[5000] + base[5002:]) is (base[5000] != base[5001])
        assert impl.find_edit(base, edited).index == 5000
    # banded DP worst case: identical strings (no early exit), k = 50 -> ~10^6 cells
    assert impl.within_k_edits(base, base, 50) is True
    assert impl.within_k_edits(base, base[:3000] + base[3010:] + "xyz", 13) is True
    assert impl.within_k_edits(base, base[:3000] + base[3010:] + "xyz", 12) is False
    assert time.perf_counter() - t0 < 2.0
    r = run_script(f"PART 4\nK 50\n{base}\n{base}\n")
    assert r.returncode == 0 and r.stdout == "true\n" and r.seconds < 2.0 and r.max_rss_mb < 256
