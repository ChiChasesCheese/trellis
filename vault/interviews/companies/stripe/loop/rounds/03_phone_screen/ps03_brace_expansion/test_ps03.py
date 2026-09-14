import random

import pytest

PART1_IN = [
    "/2022/{jan,feb,march}/report",
    "over{crowd,eager,bold,fond}ness",
    "read.txt{,.bak}",
    "{z,a,z}",
    "no braces here",
]
PART1_OUT = [
    "/2022/jan/report,/2022/feb/report,/2022/march/report",
    "overcrowdness,overeagerness,overboldness,overfondness",
    "read.txt,read.txt.bak",
    "z,a,z",
    "no braces here",
]

PART2_IN = [
    "over{crowd,eager",
    "over}crowd",
    "{onlyone}",
    "{}",
    "a{b,{c,d}}e",
    "{a,b}x{1,2}",
    "read.txt{,.bak}",
]
PART2_OUT = [
    "over{crowd,eager",
    "over}crowd",
    "{onlyone}",
    "{}",
    "a{b,{c,d}}e",
    "{a,b}x{1,2}",
    "read.txt,read.txt.bak",
]

PART3_IN = [
    "{a,{b,c}}d",
    "{a,b}{1,2}",
    "a{b,{c,d}}e",
    "{a,{single}}",
    "x{a,b}y{1,2}z",
    "over{crowd",
]
PART3_OUT = [
    "ad,bd,cd",
    "a1,a2,b1,b2",
    "abe,ace,ade",
    "{a,{single}}",
    "xay1z,xay2z,xby1z,xby2z",
    "over{crowd",
]


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_worked_examples_part1(impl):
    assert impl.part1(PART1_IN) == PART1_OUT


@pytest.mark.part1
def test_expand_braces_direct(impl):
    assert impl.expand_braces("/2022/{jan,feb}/report") == ["/2022/jan/report", "/2022/feb/report"]
    assert impl.expand_braces("{a,b,c}") == ["a", "b", "c"]


@pytest.mark.part1
@pytest.mark.edge
def test_order_preserved_duplicates_kept_not_sorted(impl):
    # the whole point of this problem set vs. qA03's sorted+dedup LC 1087 contract
    assert impl.expand_braces("{z,a,z}") == ["z", "a", "z"]
    assert impl.expand_braces("{z,a,z}") != sorted(set(impl.expand_braces("{z,a,z}")))


@pytest.mark.part1
@pytest.mark.edge
def test_empty_token_and_group_at_edges(impl):
    assert impl.expand_braces("read.txt{,.bak}") == ["read.txt", "read.txt.bak"]
    assert impl.expand_braces("{a,b}suffix") == ["asuffix", "bsuffix"]
    assert impl.expand_braces("prefix{a,b}") == ["prefixa", "prefixb"]
    assert impl.expand_braces("{a,b,c}") == ["a", "b", "c"]


@pytest.mark.part1
@pytest.mark.edge
def test_no_braces_returns_pattern_unchanged(impl):
    assert impl.expand_braces("no braces here") == ["no braces here"]
    assert impl.expand_braces("") == [""]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_worked_examples_part2(impl):
    assert impl.part2(PART2_IN) == PART2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_unmatched_braces_echoed(impl):
    assert impl.expand_braces_safe("over{crowd,eager") == ["over{crowd,eager"]
    assert impl.expand_braces_safe("over}crowd") == ["over}crowd"]


@pytest.mark.part2
@pytest.mark.edge
def test_fewer_than_two_tokens_echoed(impl):
    assert impl.expand_braces_safe("{onlyone}") == ["{onlyone}"]
    assert impl.expand_braces_safe("{}") == ["{}"]


@pytest.mark.part2
@pytest.mark.edge
def test_second_or_nested_group_out_of_part2_scope_echoed(impl):
    assert impl.expand_braces_safe("a{b,{c,d}}e") == ["a{b,{c,d}}e"]
    assert impl.expand_braces_safe("{a,b}x{1,2}") == ["{a,b}x{1,2}"]


@pytest.mark.part2
def test_well_formed_still_expands_under_safe_variant(impl):
    assert impl.expand_braces_safe("read.txt{,.bak}") == ["read.txt", "read.txt.bak"]
    assert impl.expand_braces_safe("no braces here") == ["no braces here"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_worked_examples_part3(impl):
    assert impl.part3(PART3_IN) == PART3_OUT


@pytest.mark.part3
def test_nested_group_order(impl):
    assert impl.expand_braces_nested("{a,{b,c}}d") == ["ad", "bd", "cd"]


@pytest.mark.part3
def test_multi_group_cartesian_left_outer(impl):
    # bash order: echo {a,b}{1,2} -> a1 a2 b1 b2 (left group is the outer loop)
    assert impl.expand_braces_nested("{a,b}{1,2}") == ["a1", "a2", "b1", "b2"]
    assert impl.expand_braces_nested("{a,b}{1,2}") != ["a1", "b1", "a2", "b2"]


@pytest.mark.part3
@pytest.mark.edge
def test_malformed_recursive_at_any_depth(impl):
    # inner alternative {single} has 1 token -> whole pattern malformed, not just that piece
    assert impl.expand_braces_nested("{a,{single}}") == ["{a,{single}}"]
    assert impl.expand_braces_nested("over{crowd") == ["over{crowd"]


@pytest.mark.part3
@pytest.mark.edge
def test_three_level_nesting(impl):
    assert impl.expand_braces_nested("{a,{b,{c,d}}}") == ["a", "b", "c", "d"]


@pytest.mark.part3
@pytest.mark.edge
def test_stray_close_after_valid_group_and_no_braces_echoed(impl):
    assert impl.expand_braces_nested("{a,b}}") == ["{a,b}}"]
    assert impl.expand_braces_nested("no braces here") == ["no braces here"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("PART 3\n" + "\n".join(PART3_IN) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(PART3_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.fmt
def test_output_is_comma_joined_no_spaces(run_script):
    r = run_script("PART 1\n{a,b,c}\n")
    assert r.stdout == "a,b,c\n"


@pytest.mark.part3
@pytest.mark.perf
def test_perf_10k_patterns(run_script):
    rng = random.Random(0)
    words = ["jan", "feb", "march", "apr", "may", "june", "x", "yy", "zzz"]

    def mk_pattern():
        n_groups = rng.randrange(1, 4)
        parts = []
        for _ in range(n_groups):
            toks = rng.sample(words, rng.randrange(2, 5))
            parts.append("/" + "seg" + "{" + ",".join(toks) + "}")
        return "".join(parts) + "/end"

    lines = [mk_pattern() for _ in range(10_000)]
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 10_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
