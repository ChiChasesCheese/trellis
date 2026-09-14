import random
import string

import pytest

PART1_EXAMPLE = ["i18n", "a11y", "k8s", "i018n", "I18n", "i18N", "i0n", "in", "i1", "ab12cd"]
PART1_EXAMPLE_OUT = [
    "VALID",
    "VALID",
    "VALID",
    "INVALID",
    "INVALID",
    "INVALID",
    "INVALID",
    "INVALID",
    "INVALID",
    "INVALID",
]

PART3_EXAMPLE = ["cart", "cost", "cyst", "few", "internationalization"]
PART3_EXAMPLE_OUT = [
    "cart -> ca1t",
    "cost -> co1t",
    "cyst -> cy1t",
    "few -> f1w",
    "internationalization -> i18n",
]


# ---------------------------------------------------------------- Part 1: is_valid / structure
@pytest.mark.part1
def test_example_valid_forms(impl):
    assert impl.part1(PART1_EXAMPLE) == PART1_EXAMPLE_OUT


@pytest.mark.part1
def test_is_valid_direct(impl):
    assert impl.is_valid("i18n") is True
    assert impl.is_valid("k8s") is True
    assert impl.is_valid("i018n") is False


@pytest.mark.part1
@pytest.mark.edge
def test_leading_zero_and_zero_digit_are_invalid(impl):
    # leading zero: numeric value fine (18 == 018) but string must not start with '0'
    assert impl.part1(["i018n"]) == ["INVALID"]
    # digit count exactly 0 is not "0 omitted letters", it's not a numeronym at all
    assert impl.part1(["i0n"]) == ["INVALID"]


@pytest.mark.part1
@pytest.mark.edge
def test_case_sensitivity(impl):
    assert impl.part1(["I18n", "i18N", "I18N"]) == ["INVALID", "INVALID", "INVALID"]


@pytest.mark.part1
@pytest.mark.fmt
def test_structural_shapes(impl):
    # missing digits, missing trailing letter, more than one leading letter
    assert impl.part1(["in", "i1", "ab12cd", ""]) == ["INVALID", "INVALID", "INVALID"]


@pytest.mark.part1
def test_blank_lines_ignored(impl):
    assert impl.part1(["", "i18n", "  ", "k8s"]) == ["VALID", "VALID"]


# ---------------------------------------------------------------- Part 2: dictionary expansion
@pytest.mark.part2
def test_example_expansion_match(impl):
    out = impl.part2(["i18n", "internationalization", "international", "interpretation"])
    assert out == ["internationalization"]


@pytest.mark.part2
def test_example_expansion_none(impl):
    assert impl.part2(["k8s", "kilobytes"]) == ["NONE"]


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_numeronym_yields_none(impl):
    assert impl.part2(["i018n", "internationalization"]) == ["NONE"]


@pytest.mark.part2
@pytest.mark.edge
def test_empty_dictionary_yields_none(impl):
    assert impl.part2(["i18n"]) == ["NONE"]


@pytest.mark.part2
@pytest.mark.fmt
def test_multiple_matches_sorted_lexicographically(impl):
    # two different words with the same length + first/last letter both match
    out = impl.part2(["a3n", "arban", "avian", "abandon"])
    # arban: a-r-b-a-n len5 -> 3 digits + 2 letters = matches ; avian: len5 matches too
    # abandon len7 does not match
    assert out == ["arban", "avian"]


@pytest.mark.part2
def test_malformed_dictionary_lines_skipped(impl):
    out = impl.part2(["i18n", "Internationalization", "i18n2000", "internationalization"])
    assert out == ["internationalization"]


@pytest.mark.part2
@pytest.mark.edge
def test_duplicate_dictionary_word_printed_once(impl):
    assert impl.part2(["a3n", "arban", "arban", "avian"]) == ["arban", "avian"]


# ---------------------------------------------------------------- Part 3: generate + collisions
@pytest.mark.part3
def test_example_generation_with_collision(impl):
    assert impl.part3(PART3_EXAMPLE) == PART3_EXAMPLE_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_short_words_map_to_themselves(impl):
    assert impl.part3(["ok"]) == ["ok -> ok"]
    assert impl.part3(["a"]) == ["a -> a"]


@pytest.mark.part3
@pytest.mark.edge
def test_irreducible_collision_falls_back_to_literal(impl):
    # flap/flip: base f2p for both; only prefix length available before digit hits 0 is 2 ("fl"
    # for both) -- still colliding, so both fall back to their full spelling.
    assert impl.part3(["flap", "flip"]) == ["flap -> flap", "flip -> flip"]


@pytest.mark.part3
@pytest.mark.edge
def test_length_three_collision_has_no_room_to_disambiguate(impl):
    # cat/cot: length 3, cap on prefix length is 1 (digit floor), so no prefix growth is even
    # possible -- immediate fallback to literal spelling.
    assert impl.part3(["cat", "cot"]) == ["cat -> cat", "cot -> cot"]


@pytest.mark.part3
def test_duplicate_words_collapse_to_one_entry(impl):
    assert impl.part3(["few", "few", "few"]) == ["few -> f1w"]


@pytest.mark.part3
@pytest.mark.fmt
def test_output_sorted_by_word_not_input_order(impl):
    out = impl.part3(["zebra", "apple", "mango"])
    assert out == ["apple -> a3e", "mango -> m3o", "zebra -> z3a"]


@pytest.mark.part3
def test_malformed_dictionary_lines_skipped_in_part3(impl):
    assert impl.part3(["few", "F00", "123", ""]) == ["few -> f1w"]


@pytest.mark.part3
@pytest.mark.edge
def test_three_way_collision_needs_longer_prefix(impl):
    # all base to s4y; prefix 2 gives st/st/sh -> still clashing; prefix 3 gives sto/sta/sha -> distinct
    out = impl.part3(["stormy", "starry", "shabby"])
    assert out == ["shabby -> sha2y", "starry -> sta2y", "stormy -> sto2y"]


@pytest.mark.part3
@pytest.mark.edge
def test_example_irreducible_collision_is_group_wide(impl):
    # fnap would be distinct at prefix 2 (fn1p) but flap/flip are not, so the whole group falls back
    out = impl.part3(["flap", "flip", "fnap"])
    assert out == ["flap -> flap", "flip -> flip", "fnap -> fnap"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(PART1_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(PART1_EXAMPLE_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n" + "\n".join(PART3_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(PART3_EXAMPLE_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_empty(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_words(run_script):
    rng = random.Random(0)
    alphabet = string.ascii_lowercase
    words: set[str] = set()
    while len(words) < 100_000:
        length = rng.randrange(3, 16)
        words.add("".join(rng.choice(alphabet) for _ in range(length)))
    body = "\n".join(words)
    r = run_script(f"PART 3\n{body}\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == len(words)
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
