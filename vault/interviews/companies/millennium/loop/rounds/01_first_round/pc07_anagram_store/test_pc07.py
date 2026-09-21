import random

import pytest


# ------------------------------------------------------------------------ warm-up / Part 1
@pytest.mark.part1
def test_warmup_worked_examples(impl):
    assert impl.is_valid_parentheses("()[]{}") is True
    assert impl.is_valid_parentheses("(]") is False
    assert impl.is_valid_parentheses("([)]") is False
    assert impl.is_valid_parentheses("{[]}") is True
    assert impl.is_valid_parentheses("") is True


@pytest.mark.part1
@pytest.mark.edge
def test_warmup_unmatched_and_non_bracket(impl):
    assert impl.is_valid_parentheses(")") is False
    assert impl.is_valid_parentheses("(((") is False
    with pytest.raises(ValueError):
        impl.is_valid_parentheses("(a)")
    with pytest.raises(ValueError):
        impl.is_valid_parentheses(123)


@pytest.mark.part1
def test_canonical_key_worked_examples(impl):
    assert impl.canonical_key_sorted("eat") == "aet"
    assert impl.canonical_key_counts("eat") == (
        1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    )


@pytest.mark.part1
@pytest.mark.edge
def test_canonical_key_counts_rejects_non_lowercase(impl):
    with pytest.raises(ValueError):
        impl.canonical_key_counts("Eat")
    with pytest.raises(ValueError):
        impl.canonical_key_counts("ea1")
    with pytest.raises(ValueError):
        impl.canonical_key_counts("café")  # non-ASCII 'e'
    # canonical_key_sorted has no such restriction (ascending by code point: 'é' = U+00E9 sorts
    # after the ASCII letters)
    assert impl.canonical_key_sorted("café") == "acfé"


@pytest.mark.part1
@pytest.mark.edge
def test_two_key_strategies_agree_on_grouping(impl):
    rng = random.Random(0)
    alphabet = "abcde"
    words = ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, 6))) for _ in range(200)]
    by_sorted: dict[str, list[str]] = {}
    by_counts: dict[tuple, list[str]] = {}
    for w in words:
        by_sorted.setdefault(impl.canonical_key_sorted(w), []).append(w)
        by_counts.setdefault(impl.canonical_key_counts(w), []).append(w)
    # same partition of `words`, just keyed differently -> the two strategies must produce the
    # same multiset of groups (compare as sorted-of-sorted to ignore key representation).
    groups_sorted = sorted(sorted(g) for g in by_sorted.values())
    groups_counts = sorted(sorted(g) for g in by_counts.values())
    assert groups_sorted == groups_counts


@pytest.mark.part1
def test_add_group_count_worked_example(impl):
    store = impl.AnagramStore()
    for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
        store.add(w)
    assert store.group_of("eat") == ["eat", "tea", "ate"]
    assert store.count("eat") == 3
    assert store.group_of("bat") == ["bat"]
    assert store.count("bat") == 1
    assert store.group_of("xyz") == []


@pytest.mark.part1
@pytest.mark.edge
def test_group_of_never_added_is_empty_not_error(impl):
    store = impl.AnagramStore()
    assert store.group_of("anything") == []
    assert store.count("anything") == 0


@pytest.mark.part1
@pytest.mark.edge
def test_add_duplicate_word_appears_twice(impl):
    store = impl.AnagramStore()
    store.add("eat")
    store.add("eat")
    store.add("tea")
    assert store.group_of("eat") == ["eat", "eat", "tea"]
    assert store.count("eat") == 3


@pytest.mark.part1
@pytest.mark.edge
def test_add_non_str_raises(impl):
    store = impl.AnagramStore()
    with pytest.raises(ValueError):
        store.add(123)
    with pytest.raises(ValueError):
        store.group_of(None)


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    stdin = (
        "PART 1\n"
        "ADD eat\nADD tea\nADD tan\nADD ate\nADD nat\nADD bat\n"
        "GROUP eat\nCOUNT eat\nGROUP bat\n"
    )
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "eat tea ate\n3\nbat\n"


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_most_common_group_worked_example(impl):
    store = impl.AnagramStore()
    for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
        store.add(w)
    assert store.most_common_group() == ["eat", "tea", "ate"]


@pytest.mark.part2
def test_remove_worked_example(impl):
    store = impl.AnagramStore()
    for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
        store.add(w)
    store.remove("eat")
    assert store.group_of("tea") == ["tea", "ate"]
    assert store.most_common_group() == ["tea", "ate"]


@pytest.mark.part2
@pytest.mark.edge
def test_remove_missing_word_raises(impl):
    store = impl.AnagramStore()
    store.add("eat")
    with pytest.raises(ValueError):
        store.remove("tea")  # never added
    store.remove("eat")
    with pytest.raises(ValueError):
        store.remove("eat")  # already removed


@pytest.mark.part2
@pytest.mark.edge
def test_remove_deletes_only_one_instance(impl):
    store = impl.AnagramStore()
    store.add("eat")
    store.add("eat")
    store.remove("eat")
    assert store.group_of("eat") == ["eat"]
    store.remove("eat")
    assert store.group_of("eat") == []  # group emptied and dropped, not an error to query it


@pytest.mark.part2
@pytest.mark.edge
def test_most_common_group_empty_store(impl):
    store = impl.AnagramStore()
    assert store.most_common_group() == []


@pytest.mark.part2
@pytest.mark.edge
def test_most_common_group_tie_break_is_key_lexicographic(impl):
    store = impl.AnagramStore()
    for w in ["zz", "aa"]:  # both size-1 groups, "aa" < "zz"
        store.add(w)
    assert store.most_common_group() == ["aa"]


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    stdin = (
        "PART 2\n"
        "ADD eat\nADD tea\nADD tan\nADD ate\nADD nat\nADD bat\n"
        "REMOVE eat\nMOSTCOMMON\n"
    )
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "tea ate\n"


# ------------------------------------------------------------------------ Part 3 (reconstructed)
@pytest.mark.part3
def test_case_insensitive_worked_example(impl):
    store = impl.AnagramStore(case_sensitive=False)
    for w in ["Eat", "tea", "TAN", "ate", "Nat", "bat", "listen", "silent", "enlist"]:
        store.add(w)
    assert store.group_of("eat") == ["Eat", "tea", "ate"]


@pytest.mark.part3
def test_top_k_worked_example(impl):
    store = impl.AnagramStore(case_sensitive=False)
    for w in ["Eat", "tea", "TAN", "ate", "Nat", "bat", "listen", "silent", "enlist"]:
        store.add(w)
    assert store.top_k_groups(2) == [["Eat", "tea", "ate"], ["listen", "silent", "enlist"]]


@pytest.mark.part3
@pytest.mark.edge
def test_top_k_fewer_groups_than_requested(impl):
    store = impl.AnagramStore()
    store.add("a")
    store.add("b")
    assert store.top_k_groups(10) == [["a"], ["b"]]
    assert impl.AnagramStore().top_k_groups(5) == []


@pytest.mark.part3
@pytest.mark.edge
def test_top_k_invalid_k_raises(impl):
    store = impl.AnagramStore()
    store.add("a")
    with pytest.raises(ValueError):
        store.top_k_groups(0)
    with pytest.raises(ValueError):
        store.top_k_groups(-1)
    with pytest.raises(ValueError):
        store.top_k_groups(1.5)


@pytest.mark.part3
@pytest.mark.edge
def test_default_is_case_sensitive_no_merge(impl):
    store = impl.AnagramStore()  # default case_sensitive=True
    store.add("Eat")
    store.add("eat")
    assert store.group_of("Eat") == ["Eat"]
    assert store.group_of("eat") == ["eat"]


@pytest.mark.part3
@pytest.mark.edge
def test_unicode_words_group_by_sorted_codepoints(impl):
    store = impl.AnagramStore()
    store.add("naïve")  # naïve
    store.add("ïanev")  # same multiset of codepoints, scrambled
    assert store.count("naïve") == 2


@pytest.mark.part3
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part3(run_script):
    stdin = (
        "PART 3\n"
        "CASE INSENSITIVE\n"
        "ADD Eat\nADD tea\nADD TAN\nADD ate\nADD Nat\nADD bat\n"
        "ADD listen\nADD silent\nADD enlist\n"
        "TOPK 2\n"
    )
    r = run_script(stdin)
    assert r.returncode == 0, r.stderr
    assert r.stdout == "Eat tea ate|listen silent enlist\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_many_adds_then_topk(run_script):
    rng = random.Random(0)
    alphabet = "abcdefghij"
    words = ["".join(rng.choice(alphabet) for _ in range(5)) for _ in range(20_000)]
    body = "CASE SENSITIVE\n" + "\n".join(f"ADD {w}" for w in words) + "\nTOPK 5\n"
    r = run_script("PART 3\n" + body, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"
