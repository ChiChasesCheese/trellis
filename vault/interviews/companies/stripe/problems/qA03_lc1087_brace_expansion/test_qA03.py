import random
import time

import pytest

MALFORMED = ["sun{mars}rotation", "minimum{}change", "hello-world", "hello-{-world", "hello-}-weird-{-world"]


# ---------------------------------------------------------------- Part 1: iterative
@pytest.mark.part1
def test_lc_examples(impl):
    assert impl.brace_expansion("{a,b}c{d,e}f") == ["acdf", "acef", "bcdf", "bcef"]
    assert impl.brace_expansion("abcd") == ["abcd"]


@pytest.mark.part1
def test_screening_examples(impl):
    assert impl.brace_expansion("/2022/{jan,feb,march}/report") == [
        "/2022/feb/report", "/2022/jan/report", "/2022/march/report"]
    assert impl.brace_expansion("over{crowd,eager,bold,fond}ness") == [
        "overboldness", "overcrowdness", "overeagerness", "overfondness"]
    assert impl.brace_expansion("read.txt{,.bak}") == ["read.txt", "read.txt.bak"]


@pytest.mark.part1
@pytest.mark.fmt
def test_global_sort_and_dedupe(impl):
    # options unsorted inside the group; duplicates collapse; sort is over whole words
    assert impl.brace_expansion("{b,a}{d,c}") == ["ac", "ad", "bc", "bd"]
    assert impl.brace_expansion("{a,a,b}") == ["a", "b"]
    assert impl.brace_expansion("{ab,a}{c,bc}") == ["abbc", "abc", "ac"]  # 'abc' twice -> once


@pytest.mark.part1
@pytest.mark.edge
def test_group_positions_and_empty_tokens(impl):
    assert impl.brace_expansion("{a,b}") == ["a", "b"]
    assert impl.brace_expansion("{a,b}x") == ["ax", "bx"]
    assert impl.brace_expansion("x{a,b}") == ["xa", "xb"]
    assert impl.brace_expansion("{a,b}{c,d}") == ["ac", "ad", "bc", "bd"]
    assert impl.brace_expansion("{,a}") == ["", "a"]
    assert impl.brace_expansion("x{y}z") == ["xyz"]


@pytest.mark.part1
@pytest.mark.edge
def test_echo_malformed_variant(impl):
    for s in MALFORMED:
        assert impl.brace_expansion(s, echo_malformed=True) == [s]
    assert impl.brace_expansion("a{b{c,d}}", echo_malformed=True) == ["a{b{c,d}}"]
    assert impl.brace_expansion("read.txt{,.bak}", echo_malformed=True) == ["read.txt", "read.txt.bak"]
    assert impl.brace_expansion("over{crowd,eager}ness", echo_malformed=True) == ["overcrowdness", "overeagerness"]


@pytest.mark.part1
@pytest.mark.edge
def test_strict_mode_raises_on_malformed(impl):
    for s in ["hello-{-world", "hello-}-weird-{-world", "a{b{c,d}}"]:
        with pytest.raises(ValueError):
            impl.brace_expansion(s)


# ---------------------------------------------------------------- Part 2: recursive
@pytest.mark.part2
def test_recursive_examples(impl):
    assert impl.brace_expansion_recursive("{a,b}c{d,e}f") == ["acdf", "acef", "bcdf", "bcef"]
    assert impl.brace_expansion_recursive("abcd") == ["abcd"]
    assert impl.brace_expansion_recursive("read.txt{,.bak}") == ["read.txt", "read.txt.bak"]


@pytest.mark.part2
def test_recursive_equals_iterative_random(impl):
    rng = random.Random(0)
    letters = "abc"
    for _ in range(300):
        parts = []
        for _ in range(rng.randrange(1, 5)):
            if rng.random() < 0.5:
                parts.append("".join(rng.choice(letters) for _ in range(rng.randrange(1, 3))))
            else:
                parts.append("{" + ",".join(rng.choice(letters) for _ in range(rng.randrange(1, 4))) + "}")
        s = "".join(parts)
        assert impl.brace_expansion_recursive(s) == impl.brace_expansion(s)


# ---------------------------------------------------------------- Part 3: nested
@pytest.mark.part3
def test_nested_examples(impl):
    assert impl.brace_expansion_nested("{a,b}{c,{d,e}}") == ["ac", "ad", "ae", "bc", "bd", "be"]
    assert impl.brace_expansion_nested("{{a,z},a{b,c},{ab,z}}") == ["a", "ab", "ac", "z"]


@pytest.mark.part3
@pytest.mark.edge
def test_nested_edge_cases(impl):
    assert impl.brace_expansion_nested("abcd") == ["abcd"]
    assert impl.brace_expansion_nested("{a,}") == ["", "a"]
    assert impl.brace_expansion_nested("{a,b}c{d,e}f") == ["acdf", "acef", "bcdf", "bcef"]  # flat input still works
    assert impl.brace_expansion_nested("{{{a}}}") == ["a"]
    assert impl.brace_expansion_nested("{a,b}{a,b}") == ["aa", "ab", "ba", "bb"]
    with pytest.raises(ValueError):
        impl.brace_expansion_nested("{a,b")


@pytest.mark.part3
def test_nested_agrees_with_flat_on_lc1087_inputs(impl):
    rng = random.Random(3)
    for _ in range(100):
        s = "".join(
            "{" + ",".join(rng.sample("abcd", rng.randrange(1, 4))) + "}" if rng.random() < 0.6 else rng.choice("xy")
            for _ in range(rng.randrange(1, 5))
        )
        assert impl.brace_expansion_nested(s) == impl.brace_expansion(s)


# ---------------------------------------------------------------- Part 4: count / kth
@pytest.mark.part4
def test_count_and_kth_examples(impl):
    s = "{a,b}c{d,e}f"
    assert impl.count_expansions(s) == 4
    assert impl.kth_expansion(s, 1) == "acdf"
    assert impl.kth_expansion(s, 4) == "bcef"
    assert impl.kth_expansion(s, 5) is None
    assert impl.kth_expansion(s, 0) is None
    assert impl.count_expansions("{a,b,c}{a,b,c}{a,b,c}") == 27
    assert impl.kth_expansion("{a,b,c}{a,b,c}{a,b,c}", 14) == "bbb"
    assert impl.count_expansions("abcd") == 1 and impl.kth_expansion("abcd", 1) == "abcd"


@pytest.mark.part4
@pytest.mark.edge
def test_count_dedupes_and_kth_matches_part1(impl):
    assert impl.count_expansions("{a,a,b}{c,c}") == 2
    rng = random.Random(4)
    for _ in range(100):
        s = "".join(
            "{" + ",".join(rng.choice("abcd") for _ in range(rng.randrange(1, 5))) + "}" if rng.random() < 0.7 else "x"
            for _ in range(rng.randrange(1, 5))
        )
        words = impl.brace_expansion(s)
        assert impl.count_expansions(s) == len(words)
        for k in range(1, len(words) + 1):
            assert impl.kth_expansion(s, k) == words[k - 1]


@pytest.mark.part4
@pytest.mark.edge
def test_count_without_materializing(impl):
    s = "{a,b,c,d,e,f,g,h,i,j}" * 20  # 10^20 words
    assert impl.count_expansions(s) == 10**20
    assert impl.kth_expansion(s, 1) == "a" * 20
    assert impl.kth_expansion(s, 10**20) == "j" * 20
    assert impl.kth_expansion(s, 10**20 + 1) is None
    assert impl.kth_expansion(s, 12) == "a" * 18 + "bb"  # k-1 = 11 = digits ...0,1,1


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_all_parts(run_script):
    r = run_script("PART 1\n{a,b}c{d,e}f\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "acdf\nacef\nbcdf\nbcef\n"
    assert run_script("PART 2\nread.txt{,.bak}\n").stdout == "read.txt\nread.txt.bak\n"
    assert run_script("PART 3\n{{a,z},a{b,c},{ab,z}}\n\n").stdout == "a\nab\nac\nz\n"
    assert run_script("PART 4\n{a,b,c}{a,b,c}{a,b,c}\n14\n").stdout == "27\nbbb\n"
    assert run_script("PART 4\n{a,b}\n3\n").stdout == "2\nNONE\n"
    assert run_script("PART 4\n{a,b}\n").stdout == "2\n"
    assert run_script("").stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_lc_max_and_stress(impl, run_script):
    # LC max: 50 chars -> "{a,b,c}" x 7 = 2187 words; plus a 10^5-word stress for both algorithms
    s50 = "{a,b,c}" * 7 + "x"
    assert len(s50) == 50
    t0 = time.perf_counter()
    for _ in range(20):
        assert len(impl.brace_expansion(s50)) == 2187
        assert len(impl.brace_expansion_recursive(s50)) == 2187
        assert len(impl.brace_expansion_nested(s50)) == 2187
    big = "{a,b,c,d,e,f,g,h,i,j}" * 5  # 10^5 words
    assert len(impl.brace_expansion(big)) == 100_000
    assert len(impl.brace_expansion_recursive(big)) == 100_000
    assert time.perf_counter() - t0 < 2.0
    r = run_script("PART 1\n" + s50 + "\n")
    assert r.returncode == 0 and r.stdout.count("\n") == 2187
    assert r.seconds < 2.0 and r.max_rss_mb < 256
