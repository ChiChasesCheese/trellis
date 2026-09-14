import random

import pytest

DATA = ["a: c d", "b: d a c", "c: a b", "d: c a b"]                 # verbatim from MutualRank.java
DICT = {"a": ["c", "d"], "b": ["d", "a", "c"], "c": ["a", "b"], "d": ["c", "a", "b"]}


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_verbatim_has_mutual_first_choice(impl):
    w = impl.Wishlists(DICT)
    assert w.has_mutual_first_choice("a") is True
    assert w.has_mutual_first_choice("b") is False


@pytest.mark.part1
def test_verbatim_has_mutual_pair_for_rank(impl):
    w = impl.Wishlists(DICT)
    assert w.has_mutual_pair_for_rank("a", 0) is True
    assert w.has_mutual_pair_for_rank("a", 1) is True


@pytest.mark.part1
def test_part1_stdin_lines_example(impl):
    assert impl.part1(DATA + ["FIRST a", "FIRST b", "RANK a 0", "RANK a 1", "RANK b 2"]) == ["true", "false", "true", "true", "false"]


@pytest.mark.part1
@pytest.mark.edge
def test_rank_out_of_range_unknown_user_negative_rank(impl):
    w = impl.Wishlists(DICT)
    assert w.has_mutual_pair_for_rank("b", 2) is False        # c has no 3rd choice
    assert w.has_mutual_pair_for_rank("a", 2) is False        # a has only 2 entries
    assert w.has_mutual_pair_for_rank("zz", 0) is False
    assert w.has_mutual_pair_for_rank("a", -1) is False
    assert w.has_mutual_first_choice("zz") is False


@pytest.mark.part1
@pytest.mark.edge
def test_empty_list_self_wish_and_partner_without_list(impl):
    assert impl.part1(["a:", "b: a", "FIRST a", "FIRST b"]) == ["false", "false"]
    assert impl.part1(["a: a b", "b: a", "FIRST a", "FIRST b"]) == ["true", "true"]   # self-entry ignored
    assert impl.part1(["a: ghost", "FIRST a"]) == ["false"]                           # ghost never defined
    assert impl.part1([]) == []


@pytest.mark.part1
def test_same_partner_different_ranks_is_not_a_pair(impl):
    # x ranks y first, y ranks x second -> not mutually ranked at either rank
    assert impl.part1(["x: y", "y: z x", "z: y", "RANK x 0", "RANK y 1", "RANK y 0"]) == ["false", "false", "true"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_verbatim_changed_pairings(impl):
    w = impl.Wishlists(DICT)
    assert w.changed_pairings("d", 1) == ["a"]
    assert w.changed_pairings("b", 2) == ["c"]
    assert w.changed_pairings("b", 1) == []


@pytest.mark.part2
def test_part2_stdin_example(impl):
    assert impl.part2(DATA + ["BUMP d 1", "BUMP b 2", "BUMP b 1"]) == ["a", "c", "NONE"]


@pytest.mark.part2
@pytest.mark.edge
def test_bump_rank_zero_out_of_range_unknown(impl):
    w = impl.Wishlists(DICT)
    assert w.changed_pairings("a", 0) == []
    assert w.changed_pairings("a", 2) == []
    assert w.changed_pairings("zz", 1) == []


@pytest.mark.part2
@pytest.mark.edge
def test_bump_affects_both_entries_moved_up_first(impl):
    # x: [y, z]; y ranks x 2nd (would gain when z... ) -> build: z: [x, ...] loses, y: [q, x] gains
    data = {"x": ["z", "y"], "y": ["q", "x"], "z": ["x", "q"], "q": []}
    w = impl.Wishlists(data)
    # bump y (rank 1 -> 0): y.list[1]==x (mutual now) vs y.list[0]==q (not) -> y loses;
    # z (rank 0 -> 1): z.list[0]==x (mutual now) vs z.list[1]==q -> z loses
    assert w.changed_pairings("x", 1) == ["y", "z"]
    data2 = {"x": ["z", "y"], "y": ["x", "q"], "z": ["q", "x"], "q": []}
    # y: list[1]=q (not mutual) -> list[0]=x (gains); z: list[0]=q -> list[1]=x (gains)
    assert impl.Wishlists(data2).changed_pairings("x", 1) == ["y", "z"]


@pytest.mark.part2
@pytest.mark.edge
def test_bump_does_not_mutate_lists(impl):
    w = impl.Wishlists(DICT)
    w.changed_pairings("d", 1)
    assert w.has_mutual_pair_for_rank("a", 1) is True


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_pairs_example_sorted_by_score_then_names(impl):
    assert impl.part3(DATA + ["PAIRS"]) == ["a c 0", "a d 2", "b d 2", "b c 3"]


@pytest.mark.part3
def test_best_example_tie_break_by_own_rank(impl):
    assert impl.part3(DATA + ["BEST d", "BEST b", "BEST a", "BEST c"]) == ["a 2", "d 2", "c 0", "a 0"]


@pytest.mark.part3
@pytest.mark.edge
def test_pairs_none_and_best_unknown(impl):
    assert impl.part3(["a: b", "b: c", "c: a", "PAIRS", "BEST a", "BEST zz"]) == ["NONE", "NONE", "NONE"]


@pytest.mark.part3
@pytest.mark.fmt
def test_best_full_tie_breaks_by_name(impl):
    # both partners score 2 with the same own rank impossible; equal score, equal own rank can't happen
    # for the same user, so tie on score with different own ranks -> smaller own rank; then name
    data = {"u": ["b", "a"], "a": ["x", "u"], "b": ["x", "y", "u"], "x": [], "y": []}
    # a: 1 + 1 = 2 ; b: 0 + 2 = 2 -> b has smaller own rank (0) -> b
    assert impl.Wishlists(data).best_match("u") == ("b", 2)
    assert impl.Wishlists(data).mutual_pairs() == [("a", "u", 2), ("b", "u", 2)]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_cycles_example(impl):
    assert impl.part4(DATA + ["CYCLES 3"]) == ["a c b", "a d b", "a d c", "b d c"]
    assert impl.part4(DATA + ["CYCLES 2"]) == ["a c", "a d", "b c", "b d"]


@pytest.mark.part4
@pytest.mark.edge
def test_cycles_none_and_no_duplicate_rotations(impl):
    assert impl.part4(["a: b", "b: c", "c: a", "CYCLES 3", "CYCLES 2", "CYCLES 4"]) == ["a b c", "NONE", "NONE"]
    assert impl.part4(["a: b", "b: c", "c: d", "d: a", "CYCLES 4"]) == ["a b c d"]


@pytest.mark.part4
def test_earlier_commands_still_work_in_part4(impl):
    assert impl.part4(DATA + ["FIRST a", "BUMP d 1", "BEST a"]) == ["true", "a", "c 0"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 2\n" + "\n".join(DATA) + "\nBUMP d 1\nBUMP b 2\nBUMP b 1\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "a\nc\nNONE\n"
    r = run_script("PART 1\n" + "\n".join(DATA) + "\n\nFIRST a\nFIRST b\n")
    assert r.stdout == "true\nfalse\n"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_10k_users_100k_queries(run_script):
    rng = random.Random(0)
    n = 10_000
    lines = ["PART 4"]
    for i in range(n):
        ws = rng.sample(range(n), 10)
        lines.append(f"u{i}: " + " ".join(f"u{j}" for j in ws))
    for _ in range(100_000):
        lines.append(rng.choice([f"FIRST u{rng.randrange(n)}", f"RANK u{rng.randrange(n)} {rng.randrange(10)}",
                                 f"BUMP u{rng.randrange(n)} {rng.randrange(10)}", f"BEST u{rng.randrange(n)}"]))
    lines.append("PAIRS")
    lines.append("CYCLES 3")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= 100_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
