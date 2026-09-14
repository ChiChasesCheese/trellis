import random
from collections import Counter

import pytest


def _brute(strings):
    c = Counter()
    for s in strings:
        c.update(s)
    return sorted(c.items(), key=lambda p: (-p[1], p[0]))


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.char_frequencies(["abb", "bcc"]) == [("b", 3), ("c", 2), ("a", 1)]


@pytest.mark.part1
def test_worked_example_2_spaces_and_punctuation_count(impl):
    assert impl.char_frequencies(["a a!", "a!"]) == [("a", 3), ("!", 2), (" ", 1)]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_list(impl):
    assert impl.char_frequencies([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_empty_strings(impl):
    assert impl.char_frequencies(["", "", ""]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_unicode_characters(impl):
    assert impl.char_frequencies(["你好", "你"]) == [("你", 2), ("好", 1)]


@pytest.mark.part1
@pytest.mark.edge
def test_nested_input_rejected(impl):
    with pytest.raises(ValueError):
        impl.char_frequencies(["ab", ["cd"]])


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_counter(impl):
    rng = random.Random(0)
    for _ in range(200):
        strings = ["".join(rng.choice("ab c!") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 5))]
        assert impl.char_frequencies(strings) == _brute(strings), strings


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example(impl):
    data = ["ab", ["cd", ["ef", "gh"]], "ij"]
    assert impl.char_frequencies_nested(data) == [
        (c, 1) for c in "abcdefghij"
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_empty_nested(impl):
    assert impl.char_frequencies_nested([]) == []
    assert impl.char_frequencies_nested([[], [[]], []]) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_matches_part1_on_flat_input(impl):
    assert impl.char_frequencies_nested(["abb", "bcc"]) == [("b", 3), ("c", 2), ("a", 1)]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_non_list_top_level_raises(impl):
    with pytest.raises(ValueError):
        impl.char_frequencies_nested("abc")


@pytest.mark.part2
@pytest.mark.edge
def test_part2_invalid_leaf_raises(impl):
    with pytest.raises(ValueError):
        impl.char_frequencies_nested([1, 2])


@pytest.mark.part2
@pytest.mark.edge
def test_part2_deep_nesting_no_recursion_error(impl):
    data = "x"
    for _ in range(20_000):
        data = [data]
    assert impl.char_frequencies_nested(data) == [("x", 1)]


@pytest.mark.part2
@pytest.mark.perf
def test_perf_part2_deep_and_wide(run_script):
    # 5000 leaves inside a 400-deep nesting chain, serialized with json.dumps (itself recursive,
    # so depth is kept well under sys.getrecursionlimit()); true unbounded-depth safety is proven
    # directly against the in-process API by test_part2_deep_nesting_no_recursion_error above,
    # which builds the 20000-deep object with a loop instead of a recursive serializer.
    import json

    rng = random.Random(0)
    leaves = ["".join(rng.choice("abcdef") for _ in range(4)) for _ in range(5000)]
    data = leaves
    for _ in range(400):
        data = [data]
    line = json.dumps(data)
    r = run_script("PART 2\n" + line + "\n", timeout=10)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_examples(impl):
    assert impl.top_k_chars(["aabbcc"], 1) == [("a", 2), ("b", 2), ("c", 2)]
    assert impl.top_k_chars(["aabbbcc"], 2) == [("b", 3), ("a", 2), ("c", 2)]
    assert impl.top_k_chars(["ab"], 10) == [("a", 1), ("b", 1)]
    assert impl.top_k_chars(["aabbcc"], 0) == []


@pytest.mark.part3
@pytest.mark.edge
def test_part3_k_negative_raises(impl):
    with pytest.raises(ValueError):
        impl.top_k_chars(["ab"], -1)


@pytest.mark.part3
@pytest.mark.edge
def test_part3_empty_data(impl):
    assert impl.top_k_chars([], 5) == []


@pytest.mark.part3
@pytest.mark.edge
def test_part3_no_ties_exact_k(impl):
    assert impl.top_k_chars(["aaabbc"], 2) == [("a", 3), ("b", 2)]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_random_matches_full_ranking_with_ties(impl):
    rng = random.Random(1)
    for _ in range(150):
        strings = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 4))]
        k = rng.randint(0, 4)
        full = _brute(strings)
        result = impl.top_k_chars(strings, k)
        if k == 0 or not full:
            assert result == []
            continue
        cutoff = full[min(k, len(full)) - 1][1]
        expected = [p for p in full if p[1] >= cutoff]
        assert result == expected, (strings, k)


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_part1_output_lines(impl):
    assert impl.part1(["N 2", "abb", "bcc"]) == ["b 3", "c 2", "a 1"]
    assert impl.part1(["N 1", ""]) == ["-"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script('PART 2\n["ab", ["cd"], "ab"]\n')
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a 2\nb 2\nc 1\nd 1\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script('PART 3\nK 1\n["aabbcc"]\n')
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a 2\nb 2\nc 2\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nN 2\nabb\nbcc\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "b 3\nc 2\na 1\n"
