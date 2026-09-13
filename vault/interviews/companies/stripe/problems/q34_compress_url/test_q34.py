import random

import pytest

STRIPE = "stripe.com/payments/checkout/customer.maria"
SECTION = "section/how.to.write.a.java.program.in.one.day"


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_verbatim(impl):
    assert impl.compress(STRIPE) == "s4e.c1m/p6s/c6t/c6r.m3a"


@pytest.mark.part1
def test_single_words(impl):
    assert impl.compress("internationalization") == "i18n"
    assert impl.compress("localization") == "l10n"
    assert impl.numeronym("stripe") == "s4e"


@pytest.mark.part1
@pytest.mark.edge
def test_three_letter_word_and_only_dots(impl):
    assert impl.compress("abc") == "a1c"
    assert impl.compress("abc.def.ghi") == "a1c.d1f.g1i"
    assert impl.compress("abc/def") == "a1c/d1f"


@pytest.mark.part1
@pytest.mark.edge
def test_many_minor_parts_uncapped(impl):
    assert impl.compress(SECTION) == "s5n/h1w.t0o.w3e.a-1a.j2a.p5m.i0n.o1e.d1y"


@pytest.mark.part1
def test_part1_lines(impl):
    assert impl.part1([STRIPE, "abc"]) == ["s4e.c1m/p6s/c6t/c6r.m3a", "a1c"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_m1_verbatim(impl):
    assert impl.compress(STRIPE, 1) == "s8m/p6s/c6t/c12a"


@pytest.mark.part2
def test_example_m3_verbatim(impl):
    assert impl.compress(SECTION, 3) == "s5n/h1w.t0o.w29y"


@pytest.mark.part2
@pytest.mark.edge
def test_m_boundary_exactly_m_not_folded(impl):
    # customer.maria has 2 minor parts: m=2 untouched, m=1 folded, m=3 untouched
    assert impl.compress("customer.maria", 2) == "c6r.m3a"
    assert impl.compress("customer.maria", 1) == "c12a"
    assert impl.compress("customer.maria", 3) == "c6r.m3a"
    # m=2 on 3 minor parts: keep 1, fold 'to.write' (8 chars) -> t6e
    assert impl.compress("how.to.write", 2) == "h1w.t6e"


@pytest.mark.part2
def test_part2_lines_parse_comma(impl):
    assert impl.part2([f"{STRIPE},1", f"{SECTION},3"]) == ["s8m/p6s/c6t/c12a", "s5n/h1w.t0o.w29y"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example_min_len(impl):
    assert impl.compress("docs/a.b.to.api", None, 3) == "d2s/a.b.to.a1i"
    assert impl.compress("docs/a.b.to.api", None, 4) == "d2s/a.b.to.api"
    assert impl.compress("docs/a.b.to.api") == "d2s/a-1a.b-1b.t0o.a1i"  # no threshold in Parts 1-2


@pytest.mark.part3
@pytest.mark.edge
def test_min_len_boundary(impl):
    # len < min_len unchanged, len == min_len compressed, len > min_len compressed
    assert impl.numeronym("ab", 3) == "ab"
    assert impl.numeronym("abc", 3) == "a1c"
    assert impl.numeronym("abcd", 3) == "a2d"
    assert impl.numeronym("", 3) == ""
    assert impl.numeronym("a") == "a-1a"     # no threshold: the naive rule of the source
    assert impl.numeronym("to") == "t0o"


@pytest.mark.part3
@pytest.mark.edge
def test_min_len_applies_to_folded_tail(impl):
    # tail 'a.b' is 3 characters -> compressed at min_len 3, unchanged at 4
    assert impl.compress("x/a.b", 1, 3) == "x/a1b"
    assert impl.compress("x/a.b", 1, 4) == "x/a.b"
    assert impl.part3(["docs/a.b.to.api,4"]) == ["d2s/a.b.to.api"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_ambiguous(impl):
    urls = ["payments/checkout", "pastries/checkout", "payments/checkout", "pay/checkout"]
    assert impl.ambiguous(urls) == ["p6s/c6t: 2"]


@pytest.mark.part4
@pytest.mark.edge
def test_ambiguous_empty_single_and_duplicates(impl):
    assert impl.ambiguous([]) == []
    assert impl.ambiguous(["payments"]) == []
    assert impl.ambiguous(["payments", "payments", "payments"]) == []  # duplicates count once


@pytest.mark.part4
@pytest.mark.fmt
def test_ambiguous_sorted_and_counts(impl):
    urls = ["zebra", "zooma", "apple", "azure", "ample", "apple"]
    assert impl.ambiguous(urls) == ["a3e: 3", "z3a: 2"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script(f"PART 2\n{STRIPE},1\n\n{SECTION},3\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "s8m/p6s/c6t/c12a\ns5n/h1w.t0o.w29y\n"
    r = run_script("PART 4\npayments/checkout\npastries/checkout\n")
    assert r.stdout == "p6s/c6t: 2\n"
    assert run_script("").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_urls(run_script):
    rng = random.Random(0)
    letters = "abcdefghijklmnopqrstuvwxyz"

    def word():
        return "".join(rng.choice(letters) for _ in range(rng.randint(3, 12)))

    lines = ["/".join(".".join(word() for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 6)))
             for _ in range(100_000)]
    r = run_script("PART 4\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
    r = run_script("PART 1\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.stdout.count("\n") == 100_000 and r.seconds < 2.0
