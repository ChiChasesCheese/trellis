import random

import pytest

SUP3 = ["en-US", "fr-CA", "fr-FR"]


def pal(impl, header, supported, **kw):
    return impl.parse_accept_language(header, supported, **kw)


# ---------------------------------------------------------------- Part 1: exact tags
@pytest.mark.part1
def test_part1_verbatim_examples(impl):
    assert pal(impl, "en-US, fr-CA, fr-FR", ["fr-FR", "en-US"]) == ["en-US", "fr-FR"]
    assert pal(impl, "fr-CA, fr-FR", ["en-US", "fr-FR"]) == ["fr-FR"]
    assert pal(impl, "en-US", ["en-US", "fr-CA"]) == ["en-US"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_inputs(impl):
    assert pal(impl, "", SUP3) == []
    assert pal(impl, "  , ,  ", SUP3) == []
    assert pal(impl, "en-US", []) == []
    assert pal(impl, "de-DE", SUP3) == []


@pytest.mark.part1
@pytest.mark.edge
def test_case_insensitive_output_in_supported_spelling(impl):
    assert pal(impl, "EN-us, FR-fr", SUP3) == ["en-US", "fr-FR"]
    assert pal(impl, "en-US", ["en-us"]) == ["en-us"]


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_and_duplicates(impl):
    assert pal(impl, "  fr-FR ,en-US,  fr-FR ,en-US", SUP3) == ["fr-FR", "en-US"]
    assert pal(impl, "en-US", ["en-US", "en-US", "fr-FR"]) == ["en-US"]


@pytest.mark.part1
@pytest.mark.fmt
def test_header_order_not_supported_order(impl):
    assert pal(impl, "fr-FR, fr-CA, en-US", SUP3) == ["fr-FR", "fr-CA", "en-US"]


# ---------------------------------------------------------------- Part 2: language-only
@pytest.mark.part2
def test_part2_verbatim_examples(impl):
    assert pal(impl, "en", SUP3) == ["en-US"]
    assert pal(impl, "fr", SUP3) == ["fr-CA", "fr-FR"]
    assert pal(impl, "fr-FR, fr", SUP3) == ["fr-FR", "fr-CA"]


@pytest.mark.part2
@pytest.mark.edge
def test_language_then_region_and_bare_supported_language(impl):
    assert pal(impl, "fr, fr-FR", SUP3) == ["fr-CA", "fr-FR"]  # fr-FR already emitted by fr
    assert pal(impl, "en", ["en", "en-US", "fr"]) == ["en", "en-US"]
    assert pal(impl, "de", SUP3) == []
    assert pal(impl, "e", ["en-US"]) == []  # prefix must be the whole language part


@pytest.mark.part2
@pytest.mark.edge
def test_language_only_case_and_supported_order(impl):
    assert pal(impl, "FR", ["fr-FR", "en-US", "fr-CA", "fr-fr"]) == ["fr-FR", "fr-CA"]


# ---------------------------------------------------------------- Part 3: wildcard
@pytest.mark.part3
def test_part3_verbatim_examples(impl):
    assert pal(impl, "en-US, *", SUP3) == ["en-US", "fr-CA", "fr-FR"]
    assert pal(impl, "fr-FR, fr, *", SUP3) == ["fr-FR", "fr-CA", "en-US"]


@pytest.mark.part3
@pytest.mark.edge
def test_wildcard_alone_double_and_with_unsupported(impl):
    assert pal(impl, "*", SUP3) == SUP3
    assert pal(impl, "*, *", SUP3) == SUP3
    assert pal(impl, "de, *", SUP3) == SUP3
    assert pal(impl, "*", []) == []


@pytest.mark.part3
@pytest.mark.edge
def test_wildcard_first_then_explicit_tag_still_ordered_by_position(impl):
    # '*' at position 0 claims nothing explicitly; en-US is claimed by the later entry so
    # the wildcard yields the French tags first, then en-US
    assert pal(impl, "*, en-US", SUP3) == ["fr-CA", "fr-FR", "en-US"]


# ---------------------------------------------------------------- Part 4: q-values
@pytest.mark.part4
def test_part4_programhelp_example(impl):
    assert pal(impl, "en-US,en;q=0.8,fr;q=0.9,de;q=0.7", ["en-US", "en-GB", "fr", "de"]) == ["en-US", "fr", "en-GB", "de"]


@pytest.mark.part4
def test_part4_q_zero_excluded_but_claims_tag(impl):
    sup = ["fr-FR", "fr-CA", "fr-BG", "en-US"]
    assert pal(impl, "fr-FR;q=1, fr-CA;q=0, *;q=0.5", sup) == ["fr-FR", "fr-BG", "en-US"]
    assert pal(impl, "fr-FR;q=1, fr-CA;q=0, fr;q=0.5", ["fr-FR", "fr-CA", "fr-BG"]) == ["fr-FR", "fr-BG"]
    out = pal(impl, "fr-FR;q=1, fr-CA;q=0.8, *;q=0.5", sup)
    assert out[:2] == ["fr-FR", "fr-CA"] and sorted(out[2:]) == ["en-US", "fr-BG"]


@pytest.mark.part4
def test_variant_zero_q_last_matches_programhelp(impl):
    sup = ["fr-FR", "fr-CA", "fr-BG", "en-US"]
    assert pal(impl, "fr-FR;q=1, fr-CA;q=0, *;q=0.5", sup, zero_q="last") == ["fr-FR", "fr-BG", "en-US", "fr-CA"]
    assert pal(impl, "fr-FR;q=1, fr-CA;q=0, fr;q=0.5", ["fr-FR", "fr-CA", "fr-BG"], zero_q="last") == ["fr-FR", "fr-BG", "fr-CA"]


@pytest.mark.part4
@pytest.mark.edge
def test_q_ties_default_and_equal_values(impl):
    assert pal(impl, "fr-FR;q=0.5, en-US;q=0.50, fr-CA;q=1.0", SUP3) == ["fr-CA", "fr-FR", "en-US"]
    assert pal(impl, "fr-FR;q=0.9, en-US", SUP3) == ["en-US", "fr-FR"]  # default 1.0 beats 0.9
    assert pal(impl, "fr-FR;q=0.001, en-US;q=0", SUP3) == ["fr-FR"]  # one above zero vs zero


@pytest.mark.part4
@pytest.mark.edge
def test_q_whitespace_bad_values_and_other_params(impl):
    assert pal(impl, " fr-FR ; q=0.5 , en-US ; level=1 ; q = 0.7 ", SUP3) == ["en-US", "fr-FR"]
    assert pal(impl, "fr-FR;q=abc, en-US;q=0.9", SUP3) == ["fr-FR", "en-US"]  # bad q -> 1.0
    assert pal(impl, "fr-FR;Q=0.1, en-US", SUP3) == ["en-US", "fr-FR"]


@pytest.mark.part4
@pytest.mark.edge
def test_language_only_with_q_and_wildcard_ordering(impl):
    sup = ["en-US", "en-GB", "fr-FR", "de-DE"]
    assert pal(impl, "*;q=0.9, en;q=0.5", sup) == ["fr-FR", "de-DE", "en-US", "en-GB"]
    assert pal(impl, "en-GB;q=0.2, en;q=0.9", sup) == ["en-US", "en-GB"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("en-US, fr-CA, fr-FR\nfr-FR,en-US\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "en-US\nfr-FR\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_none_and_wildcard(run_script):
    assert run_script("de-DE\nen-US,fr-FR\n").stdout == "NONE\n"
    assert run_script("\nen-US\n").stdout == "NONE\n"
    assert run_script("").stdout == "NONE\n"
    assert run_script("fr;q=0.5, *\nen-US, fr-CA, fr-FR\n").stdout == "en-US\nfr-CA\nfr-FR\n"


@pytest.mark.part4
@pytest.mark.perf
def test_perf_10k_entries_1k_supported(run_script):
    rng = random.Random(0)
    langs = [f"l{i}" for i in range(300)]
    supported = [f"{rng.choice(langs)}-R{rng.randrange(20)}" for _ in range(1000)]
    entries = []
    for _ in range(10_000):
        k = rng.random()
        tag = rng.choice(langs) if k < 0.3 else (rng.choice(supported) if k < 0.98 else "*")
        entries.append(f"{tag};q={rng.randrange(0, 11) / 10:.1f}" if rng.random() < 0.5 else tag)
    r = run_script(", ".join(entries) + "\n" + ",".join(supported) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= 1
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
