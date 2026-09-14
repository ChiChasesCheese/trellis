import random
import sys

import pytest


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_roundtrip(impl):
    data = impl.serialize(["a", "ab", "b"])
    assert data == "0a1b1##b1##"
    assert impl.deserialize(data) == ["a", "ab", "b"]


@pytest.mark.part1
def test_command_stream(impl):
    out = impl.part1(["SERIALIZE 3 a ab b", "DESERIALIZE 0a1b1##b1##"])
    assert out == ["0a1b1##b1##", "a ab b"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_word_list(impl):
    data = impl.serialize([])
    assert data == "0#"
    assert impl.deserialize(data) == []


@pytest.mark.part1
@pytest.mark.edge
def test_empty_string_as_a_word(impl):
    data = impl.serialize([""])
    assert data == "1#"
    assert impl.deserialize(data) == [""]


@pytest.mark.part1
@pytest.mark.edge
def test_deserialize_result_is_lexicographic_regardless_of_insertion_order(impl):
    data = impl.serialize(["zebra", "apple", "mango"])
    assert impl.deserialize(data) == ["apple", "mango", "zebra"]


@pytest.mark.part1
@pytest.mark.edge
def test_single_word(impl):
    data = impl.serialize(["hello"])
    assert impl.deserialize(data) == ["hello"]


@pytest.mark.part1
@pytest.mark.edge
def test_word_with_invalid_characters_raises(impl):
    with pytest.raises(ValueError):
        impl.serialize(["Hello"])
    with pytest.raises(ValueError):
        impl.serialize(["ab1c"])
    with pytest.raises(ValueError):
        impl.serialize(["a b"])


@pytest.mark.part1
@pytest.mark.edge
def test_shared_prefix_words(impl):
    words = ["car", "card", "care", "careful", "cats"]
    data = impl.serialize(words)
    assert impl.deserialize(data) == sorted(words)


# ------------------------------------------------------------------------ Part 2 (compactness)
@pytest.mark.part2
def test_length_bound_holds_for_several_word_sets(impl):
    cases = [
        ["a", "ab", "b"],
        ["car", "card", "care", "careful", "cats"],
        [f"word{chr(ord('a') + (i % 26))}{chr(ord('a') + (i // 26))}" for i in range(50)],
        ["same", "sameprefixa", "sameprefixb", "sameprefixc"],
        [],
        [""],
    ]
    for words in cases:
        data = impl.serialize(words)
        num_nodes = sum(1 for c in data if c in "01")
        bound = sum(len(w) for w in words) + 2 * num_nodes
        assert len(data) <= bound, f"{words!r}: {len(data)} > {bound}"


@pytest.mark.part2
@pytest.mark.edge
def test_length_bound_no_shared_prefixes_worst_case(impl):
    """Completely disjoint first letters: every word is its own branch from the root, minimal
    sharing -- the bound must still hold even at this near-worst case for compression."""
    words = [chr(ord("a") + i) * 3 for i in range(20)]  # "aaa", "bbb", "ccc", ...
    data = impl.serialize(words)
    num_nodes = sum(1 for c in data if c in "01")
    bound = sum(len(w) for w in words) + 2 * num_nodes
    assert len(data) <= bound


@pytest.mark.part2
@pytest.mark.perf
def test_deep_chain_10000_no_recursion(impl):
    word = "a" * 10_000
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(200)
    try:
        data = impl.serialize([word])
        words = impl.deserialize(data)
    finally:
        sys.setrecursionlimit(old_limit)
    assert words == [word]


@pytest.mark.part2
@pytest.mark.perf
def test_perf_many_words_roundtrip(run_script):
    rng = random.Random(0)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    words = sorted({"".join(rng.choice(alphabet) for _ in range(rng.randint(1, 12))) for _ in range(3000)})
    line = f"SERIALIZE {len(words)} " + " ".join(words)
    r = run_script("PART 2\n" + line + "\n", timeout=15)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ Part 3 (malformed, starts_with)
@pytest.mark.part3
def test_worked_example_starts_with_and_error(impl):
    out = impl.part3(
        [
            "SERIALIZE 3 a ab b",
            "STARTSWITH 0a1b1##b1## a",
            "STARTSWITH 0a1b1##b1## c",
            "DESERIALIZE bad",
        ]
    )
    assert out == ["0a1b1##b1##", "true", "false", "ERROR"]


@pytest.mark.part3
@pytest.mark.edge
def test_starts_with_empty_prefix_always_true(impl):
    data = impl.serialize(["a", "b"])
    assert impl.starts_with(data, "") is True


@pytest.mark.part3
@pytest.mark.edge
def test_starts_with_full_word_and_true_prefix(impl):
    data = impl.serialize(["apple", "app"])
    assert impl.starts_with(data, "app") is True
    assert impl.starts_with(data, "apple") is True
    assert impl.starts_with(data, "ap") is True


@pytest.mark.part3
@pytest.mark.edge
def test_starts_with_nonexistent_prefix(impl):
    data = impl.serialize(["apple", "app"])
    assert impl.starts_with(data, "b") is False
    assert impl.starts_with(data, "appx") is False
    assert impl.starts_with(data, "applesauce") is False


@pytest.mark.part3
@pytest.mark.edge
def test_starts_with_must_skip_non_matching_siblings_correctly(impl):
    """Regression for the skip-subtree bracket counter: a wide fan-out at the root where the
    desired letter is NOT first alphabetically must still be found after skipping earlier
    siblings' full subtrees."""
    data = impl.serialize(["zzz", "yyy", "target", "aaa"])
    assert impl.starts_with(data, "target") is True
    assert impl.starts_with(data, "targetx") is False
    assert impl.starts_with(data, "aaa") is True
    assert impl.starts_with(data, "zzz") is True


@pytest.mark.part3
@pytest.mark.edge
@pytest.mark.parametrize(
    "bad",
    ["", "2#", "0a", "0a1", "0a1#", "x", "0#x", "0a1##extra", "01#", "0##"],
)
def test_deserialize_rejects_malformed_input(impl, bad):
    with pytest.raises(ValueError):
        impl.deserialize(bad)


@pytest.mark.part3
@pytest.mark.edge
def test_command_stream_wraps_malformed_as_error(impl):
    out = impl.part3(["DESERIALIZE 2#", "STARTSWITH 2# a"])
    assert out == ["ERROR", "ERROR"]


@pytest.mark.part3
def test_random_cross_check_roundtrip_and_prefix(impl):
    rng = random.Random(1)
    alphabet = "abcdefg"
    for _trial in range(20):
        words = sorted({"".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6))) for _ in range(15)})
        data = impl.serialize(words)
        assert impl.deserialize(data) == words
        for w in words:
            for cut in range(len(w) + 1):
                assert impl.starts_with(data, w[:cut]) is True
        assert impl.starts_with(data, "zzzzzzz") is False


# ------------------------------------------------------------------------ fmt / io
@pytest.mark.part1
@pytest.mark.fmt
def test_deserialize_empty_output_is_dash(impl):
    out = impl.part1(["SERIALIZE 0", "DESERIALIZE 0#"])
    assert out == ["0#", "-"]


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nSERIALIZE 3 a ab b\nDESERIALIZE 0a1b1##b1##\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0a1b1##b1##\na ab b\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script(
        "PART 3\nSERIALIZE 3 a ab b\nSTARTSWITH 0a1b1##b1## a\nSTARTSWITH 0a1b1##b1## c\nDESERIALIZE bad\n"
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout == "0a1b1##b1##\ntrue\nfalse\nERROR\n"
