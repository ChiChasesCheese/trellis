"""q42 Loose-Schema Record Aggregation — tests. RECONSTRUCTED TRAINING PROBLEM (two-hop: 1p3a
transcript that self-describes as an interviewer reconstruction) -- see problem.md's warning
block. Part 1/2 worked examples are the upstream's own numbers; everything else here is this
repo's own, produced by running solution.py.
"""

import random

import pytest

# ---------------------------------------------------------------- shared examples (upstream)

P1_EXAMPLE = [
    "4",
    "id=1 amount=10 currency=USD",
    "id=2 amount=5 currency=USD",
    "id=3 amount=7 currency=EUR",
    "id=4 currency=USD",
]
P1_EXAMPLE_OUT = ["EUR 7", "USD 15"]

P2_EXAMPLE = [
    "5 region",
    "id=1 amount=10 currency=USD region=NA",
    "id=2 amount=5 currency=USD region=NA",
    "id=3 amount=7 currency=EUR region=EU",
    "id=4 amount=4 currency=USD",
    "id=5 amount=3 currency=USD region=EU",
]
P2_EXAMPLE_OUT = ["EU EUR 7", "EU USD 3", "NA USD 15", "__none__ USD 4"]

P3_EXAMPLE = [
    "3",
    "id=1 amount=10 currency=USD",
    "id=2 amount=5 currency=USD extra=x",
    "id=3 currency=EUR",
]
P3_EXAMPLE_OUT = ["USD 15", "SCHEMA", "amount 2", "currency 3", "extra 1", "id 3"]


# ---------------------------------------------------------------- Part 1: total per currency
@pytest.mark.part1
def test_example_part1(impl):
    assert impl.part1(P1_EXAMPLE) == P1_EXAMPLE_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_zero_records(impl):
    assert impl.part1(["0"]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_single_record(impl):
    assert impl.part1(["1", "id=1 amount=42 currency=JPY"]) == ["JPY 42"]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_key_last_wins(impl):
    lines = ["1", "id=1 amount=5 amount=9 currency=USD"]
    assert impl.part1(lines) == ["USD 9"]


@pytest.mark.part1
@pytest.mark.edge
def test_field_order_not_guaranteed_still_merges(impl):
    lines = ["2", "currency=USD amount=10 id=1", "amount=5 id=2 currency=USD"]
    assert impl.part1(lines) == ["USD 15"]


@pytest.mark.part1
@pytest.mark.edge
def test_zero_and_negative_amount(impl):
    lines = ["2", "amount=0 currency=USD", "amount=-1 currency=USD"]
    # amount=0 is valid (non-negative includes zero); amount=-1 is invalid (skipped, no crash)
    assert impl.part1(lines) == ["USD 0"]


@pytest.mark.part1
@pytest.mark.edge
def test_malformed_amount_values_skipped(impl):
    lines = [
        "4",
        "amount=abc currency=USD",
        "amount= currency=USD",
        "currency=USD",
        "amount=+5 currency=USD",  # leading '+' is not a bare digit string -> invalid
    ]
    assert impl.part1(lines) == []


@pytest.mark.part1
@pytest.mark.edge
def test_empty_currency_treated_as_missing(impl):
    lines = ["1", "amount=5 currency="]
    assert impl.part1(lines) == []


@pytest.mark.part1
@pytest.mark.edge
def test_malformed_token_dropped_rest_of_record_still_valid(impl):
    lines = ["1", "amount=10 =badkey currency=USD justtext"]
    assert impl.part1(lines) == ["USD 10"]


@pytest.mark.part1
@pytest.mark.fmt
def test_currencies_sorted_alphabetically(impl):
    lines = ["3", "amount=1 currency=USD", "amount=1 currency=AUD", "amount=1 currency=EUR"]
    assert impl.part1(lines) == ["AUD 1", "EUR 1", "USD 1"]


@pytest.mark.part1
def test_very_large_amount_no_precision_loss(impl):
    lines = ["2", f"amount={10**15} currency=USD", f"amount={10**15} currency=USD"]
    assert impl.part1(lines) == [f"USD {2 * 10**15}"]


# ---------------------------------------------------------------- Part 2: group by arbitrary key
@pytest.mark.part2
def test_example_part2(impl):
    assert impl.part2(P2_EXAMPLE) == P2_EXAMPLE_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_missing_group_key_buckets_under_none_sentinel(impl):
    lines = ["1 region", "amount=5 currency=USD"]
    assert impl.part2(lines) == ["__none__ USD 5"]


@pytest.mark.part2
@pytest.mark.edge
def test_present_but_empty_group_value_is_distinct_from_none_sentinel(impl):
    lines = ["2 region", "amount=5 currency=USD region=", "amount=3 currency=USD"]
    out = impl.part2(lines)
    assert " USD 5" in out  # group is the literal empty string, not '__none__'
    assert "__none__ USD 3" in out
    assert out == sorted(out)


@pytest.mark.part2
@pytest.mark.edge
def test_zero_records_with_group_key(impl):
    assert impl.part2(["0 region"]) == []


@pytest.mark.part2
@pytest.mark.fmt
def test_group_currency_pairs_sorted_lexicographically(impl):
    lines = [
        "3 region",
        "amount=1 currency=USD region=NA",
        "amount=1 currency=USD region=EU",
        "amount=1 currency=EUR region=EU",
    ]
    assert impl.part2(lines) == ["EU EUR 1", "EU USD 1", "NA USD 1"]


@pytest.mark.part2
@pytest.mark.edge
def test_invalid_records_excluded_from_group_totals(impl):
    lines = ["2 region", "amount=abc currency=USD region=NA", "amount=5 currency=USD region=NA"]
    assert impl.part2(lines) == ["NA USD 5"]


# ---------------------------------------------------------------- Part 3: schema inference
@pytest.mark.part3
def test_example_part3(impl):
    assert impl.part3(P3_EXAMPLE) == P3_EXAMPLE_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_zero_records_schema_is_just_header(impl):
    assert impl.part3(["0"]) == ["SCHEMA"]


@pytest.mark.part3
@pytest.mark.edge
def test_schema_counts_invalid_records_too(impl):
    lines = ["2", "amount=5 currency=USD", "amount=abc weirdfield=1"]
    out = impl.part3(lines)
    assert out[0] == "USD 5"
    assert "SCHEMA" in out
    schema = out[out.index("SCHEMA") + 1:]
    assert "amount 2" in schema
    assert "currency 1" in schema
    assert "weirdfield 1" in schema


@pytest.mark.part3
@pytest.mark.edge
def test_schema_dedupes_repeated_key_within_one_record(impl):
    lines = ["1", "amount=1 amount=2 amount=3 currency=USD"]
    out = impl.part3(lines)
    schema = out[out.index("SCHEMA") + 1:]
    assert "amount 1" in schema  # one record, key appears 3x on the line -> counted once


@pytest.mark.part3
@pytest.mark.edge
def test_part3_with_group_by_key_header(impl):
    lines = ["2 region", "amount=5 currency=USD region=NA", "amount=3 currency=USD"]
    out = impl.part3(lines)
    assert out[0] == "NA USD 5"
    assert out[1] == "__none__ USD 3"
    assert out[2] == "SCHEMA"


@pytest.mark.part3
@pytest.mark.fmt
def test_schema_keys_sorted_alphabetically(impl):
    lines = ["1", "zeta=1 alpha=2 mu=3 currency=USD amount=1"]
    out = impl.part3(lines)
    schema = out[out.index("SCHEMA") + 1:]
    keys = [line.split()[0] for line in schema]
    assert keys == sorted(keys)


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(P1_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_EXAMPLE_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_part2(run_script):
    r = run_script("PART 2\n" + "\n".join(P2_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P2_EXAMPLE_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    r = run_script("PART 3\n" + "\n".join(P3_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P3_EXAMPLE_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_2e5_records(run_script):
    rng = random.Random(0)
    n = 200_000
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD"]
    regions = ["NA", "EU", "AP", None]  # None -> field omitted
    lines = [f"{n} region"]
    for i in range(n):
        tokens = [f"id={i}", f"amount={rng.randrange(0, 10**9)}", f"currency={rng.choice(currencies)}"]
        region = rng.choice(regions)
        if region is not None:
            tokens.append(f"region={region}")
        rng.shuffle(tokens)
        lines.append(" ".join(tokens))
    r = run_script("PART 3\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert "SCHEMA" in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
