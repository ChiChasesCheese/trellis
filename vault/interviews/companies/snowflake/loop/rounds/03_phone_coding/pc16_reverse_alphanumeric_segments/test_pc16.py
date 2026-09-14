import itertools
import random
import string

import pytest


def _brute(s: str) -> str:
    """Independent reference: group by the isalnum() predicate with itertools.groupby, reverse
    every alnum group, leave every non-alnum group untouched, then reassemble."""
    out = []
    for is_alnum, group in itertools.groupby(s, key=str.isalnum):
        chunk = list(group)
        if is_alnum:
            chunk.reverse()
        out.extend(chunk)
    return "".join(out)


RANDOM_ALPHABET = string.ascii_letters + string.digits + " .,!?'-_/éü漢字" + "\t"


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
@pytest.mark.parametrize(
    "s,expected",
    [
        ("We're", "eW'er"),
        ("abc", "cba"),
        ("", ""),
        ("!!!", "!!!"),
        ("a", "a"),
        ("12-34", "21-43"),
        ("hello, world!", "olleh, dlrow!"),
    ],
)
def test_worked_examples(impl, s, expected):
    assert impl.reverse_alnum_segments(s) == expected


@pytest.mark.part1
@pytest.mark.edge
def test_single_run_whole_string(impl):
    assert impl.reverse_alnum_segments("abcdef123") == "321fedcba"


@pytest.mark.part1
@pytest.mark.edge
def test_only_boundaries(impl):
    assert impl.reverse_alnum_segments("   ...   ") == "   ...   "


@pytest.mark.part1
@pytest.mark.edge
def test_leading_and_trailing_boundaries(impl):
    assert impl.reverse_alnum_segments("!ab12!") == "!21ba!"


@pytest.mark.part1
@pytest.mark.edge
def test_unicode_letters_form_one_run(impl):
    # 'é' is alphanumeric under Python's Unicode-aware str.isalnum().
    assert impl.reverse_alnum_segments("café1") == "1éfac"


@pytest.mark.part1
@pytest.mark.edge
def test_against_brute_force_random(impl):
    rng = random.Random(0)
    for _ in range(500):
        length = rng.randint(0, 30)
        s = "".join(rng.choice(RANDOM_ALPHABET) for _ in range(length))
        assert impl.reverse_alnum_segments(s) == _brute(s), repr(s)


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
@pytest.mark.parametrize(
    "s,expected",
    [("We're", "eW'er"), ("abc", "cba"), ("", ""), ("a1!b2", "1a!2b")],
)
def test_inplace_worked_examples(impl, s, expected):
    chars = list(s)
    impl.reverse_alnum_segments_inplace(chars)
    assert "".join(chars) == expected


@pytest.mark.part2
@pytest.mark.edge
def test_inplace_mutates_the_same_list_object(impl):
    chars = list("We're")
    ref = chars
    impl.reverse_alnum_segments_inplace(chars)
    assert ref is chars  # no new list was substituted
    assert "".join(chars) == "eW'er"


@pytest.mark.part2
@pytest.mark.edge
def test_inplace_agrees_with_part1_random(impl):
    rng = random.Random(1)
    for _ in range(500):
        length = rng.randint(0, 30)
        s = "".join(rng.choice(RANDOM_ALPHABET) for _ in range(length))
        chars = list(s)
        impl.reverse_alnum_segments_inplace(chars)
        assert "".join(chars) == impl.reverse_alnum_segments(s), repr(s)


@pytest.mark.part2
@pytest.mark.edge
def test_inplace_unicode(impl):
    chars = list("café123!déjà")
    impl.reverse_alnum_segments_inplace(chars)
    assert "".join(chars) == _brute("café123!déjà")


# ------------------------------------------------------------------------ perf / io
@pytest.mark.part1
@pytest.mark.perf
def test_perf_large_string(run_script):
    rng = random.Random(0)
    s = "".join(rng.choice(RANDOM_ALPHABET) for _ in range(200_000))
    r = run_script("PART 1\n" + s + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.rstrip("\n") == _brute(s)
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nWe're\nabc\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "eW'er\ncba\n"


@pytest.mark.part1
@pytest.mark.io
@pytest.mark.fmt
def test_stdin_stdout_part1_blank_line_is_significant(run_script):
    r = run_script("PART 1\nab\n\ncd\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "ba\n\ndc\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nWe're\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "eW'er\n"
