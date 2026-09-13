import random
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

RECORDS = [
    "r1,100.00,2024-01-10T10:00:00Z,US",
    "r2,50.00,2024-01-05T09:00:00Z,CA",
    "r3,50.00,2024-01-01T08:00:00Z,DE",
    "r4,200.00,2024-02-01T00:00:00Z,US",
]


# ---------------------------------------------------------------- Part 1: min_by_amount
@pytest.mark.part1
def test_example_min_by_amount(impl):
    records = impl.parse_records(RECORDS)
    assert impl.min_by_amount(records) == "r2"


@pytest.mark.part1
def test_part1_via_lines(impl):
    assert impl.part1(RECORDS) == ["r2"]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_input_is_none(impl):
    assert impl.min_by_amount([]) is None
    assert impl.part1([]) == ["NONE"]


@pytest.mark.part1
@pytest.mark.edge
def test_single_record(impl):
    records = impl.parse_records(["only,10.00,2024-01-01T00:00:00Z,US"])
    assert impl.min_by_amount(records) == "only"


@pytest.mark.part1
@pytest.mark.edge
def test_negative_amount_wins(impl):
    lines = ["a,10.00,2024-01-01T00:00:00Z,US", "b,-5.00,2024-01-01T00:00:00Z,US"]
    assert impl.part1(lines) == ["b"]


@pytest.mark.part1
def test_blank_lines_ignored_when_parsing(impl):
    lines = ["", "r1,100.00,2024-01-10T10:00:00Z,US", "  ", "r2,50.00,2024-01-05T09:00:00Z,CA"]
    records = impl.parse_records(lines)
    assert len(records) == 2
    assert impl.min_by_amount(records) == "r2"


# ---------------------------------------------------------------- Part 2: extreme(key, mode)
@pytest.mark.part2
def test_example_extreme_amount_max(impl):
    assert impl.part2(["amount max"] + RECORDS) == ["r4"]


@pytest.mark.part2
def test_example_extreme_created_at_min(impl):
    assert impl.part2(["created_at min"] + RECORDS) == ["r3"]


@pytest.mark.part2
def test_example_extreme_country_min_and_max(impl):
    assert impl.part2(["country min"] + RECORDS) == ["r2"]
    assert impl.part2(["country max"] + RECORDS) == ["r1"]  # US ties r1/r4, first wins


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_key_raises(impl):
    records = impl.parse_records(RECORDS)
    with pytest.raises(ValueError):
        impl.extreme(records, "bogus", "min")


@pytest.mark.part2
@pytest.mark.edge
def test_unknown_mode_raises(impl):
    records = impl.parse_records(RECORDS)
    with pytest.raises(ValueError):
        impl.extreme(records, "amount", "bogus")


@pytest.mark.part2
@pytest.mark.edge
def test_extreme_empty_is_none(impl):
    assert impl.extreme([], "amount", "min") is None
    assert impl.part2(["amount min"]) == ["NONE"]


@pytest.mark.part2
def test_created_at_z_and_offset_are_equal_instants(impl):
    # Z and an equivalent numeric offset must compare as the same instant
    lines = ["a,10.00,2024-01-01T10:00:00Z,US", "b,20.00,2024-01-01T10:00:00+00:00,US"]
    records = impl.parse_records(lines)
    # a is strictly smaller amount, but this test only checks parsing/comparison consistency:
    # tie amounts at same instant should not raise and should resolve deterministically
    assert impl.extreme(records, "created_at", "min") == "a"


# ---------------------------------------------------------------- Part 3: extreme_with(comparator)
@pytest.mark.part3
def test_example_comparator_diverges_from_part1(impl):
    records = impl.parse_records(RECORDS)
    # amount ties r2/r3 at 50.00; comparator breaks the tie by created_at, picking r3 --
    # different from part1's min_by_amount, which picks r2 (first on tie)
    assert impl.extreme_with(records, impl.by_amount_then_created_at) == "r3"
    assert impl.min_by_amount(records) == "r2"


@pytest.mark.part3
def test_part3_via_stdin_style_dispatch(impl):
    assert impl.part3(RECORDS) == ["r3"]


@pytest.mark.part3
@pytest.mark.edge
def test_extreme_with_empty_is_none(impl):
    assert impl.extreme_with([], impl.by_amount_then_created_at) is None
    assert impl.part3([]) == ["NONE"]


@pytest.mark.part3
def test_extreme_with_custom_comparator_ignores_amount(impl):
    # a comparator that only looks at `country` -- must not assume amount is involved
    records = impl.parse_records(RECORDS)

    def by_country(a, b):
        if a.country == b.country:
            return 0
        return -1 if a.country < b.country else 1

    assert impl.extreme_with(records, by_country) == "r2"  # "CA" is smallest


@pytest.mark.part3
def test_extreme_with_reversed_comparator_finds_max(impl):
    records = impl.parse_records(RECORDS)

    def by_amount_desc(a, b):
        if a.amount == b.amount:
            return 0
        return -1 if a.amount > b.amount else 1

    assert impl.extreme_with(records, by_amount_desc) == "r4"


@pytest.mark.part3
@pytest.mark.edge
def test_by_amount_then_created_at_is_total_order_on_ties(impl):
    # three-way tie on amount, distinct created_at -- must pick the earliest deterministically
    lines = [
        "x,10.00,2024-03-01T00:00:00Z,US",
        "y,10.00,2024-01-01T00:00:00Z,US",
        "z,10.00,2024-02-01T00:00:00Z,US",
    ]
    records = impl.parse_records(lines)
    assert impl.extreme_with(records, impl.by_amount_then_created_at) == "y"


# ---------------------------------------------------------------- Part 4: extreme_all + ties
@pytest.mark.part4
def test_example_ties_amount_min(impl):
    assert impl.part4(["amount min"] + RECORDS) == ["r2", "r3"]


@pytest.mark.part4
def test_example_ties_country_max(impl):
    assert impl.part4(["country max"] + RECORDS) == ["r1", "r4"]


@pytest.mark.part4
@pytest.mark.edge
def test_extreme_all_empty_is_none(impl):
    assert impl.extreme_all([], "amount", "min") == []
    assert impl.part4(["amount min"]) == ["NONE"]


@pytest.mark.part4
@pytest.mark.edge
def test_extreme_all_single_record(impl):
    lines = ["only,10.00,2024-01-01T00:00:00Z,US"]
    assert impl.part4(["amount min"] + lines) == ["only"]


@pytest.mark.part4
@pytest.mark.fmt
def test_extreme_all_sorted_plain_string_order(impl):
    # ids intentionally out of alphabetical/numeric input order, all tied at the same amount
    lines = [
        "user2,5.00,2024-01-01T00:00:00Z,US",
        "B,5.00,2024-01-01T00:00:00Z,US",
        "user10,5.00,2024-01-01T00:00:00Z,US",
        "a,5.00,2024-01-01T00:00:00Z,US",
    ]
    out = impl.part4(["amount min"] + lines)
    assert out == ["B", "a", "user10", "user2"]  # plain string order: 'B' < 'a' < 'user10' < 'user2'


@pytest.mark.part4
@pytest.mark.edge
def test_extreme_all_duplicate_ids_both_listed(impl):
    lines = ["dup,5.00,2024-01-01T00:00:00Z,US", "dup,5.00,2024-01-02T00:00:00Z,CA"]
    assert impl.part4(["amount min"] + lines) == ["dup", "dup"]


@pytest.mark.part4
def test_extreme_all_no_ties_returns_one(impl):
    assert impl.part4(["amount max"] + RECORDS) == ["r4"]


# ---------------------------------------------------------------- io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(RECORDS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "r2\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\namount max\n" + "\n".join(RECORDS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "r4\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\n" + "\n".join(RECORDS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "r3\n"


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_part4(run_script):
    r = run_script("PART 4\namount min\n" + "\n".join(RECORDS) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "r2\nr3\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_empty(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.io
def test_stdin_none_output_for_empty_records(run_script):
    r = run_script("PART 1\n")
    assert r.returncode == 0
    assert r.stdout == "NONE\n"


# ---------------------------------------------------------------- perf
@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_records(run_script):
    rng = random.Random(0)
    base = datetime(2024, 1, 1)
    countries = ["US", "CA", "DE", "FR", "GB"]
    lines = []
    for i in range(100_000):
        amount = Decimal(rng.randrange(0, 100)).quantize(Decimal("0.01"))  # small range -> many ties
        ts = (base + timedelta(seconds=rng.randrange(0, 10_000_000))).strftime("%Y-%m-%dT%H:%M:%SZ")
        country = rng.choice(countries)
        lines.append(f"r{i},{amount},{ts},{country}")
    stdin = "PART 4\namount min\n" + "\n".join(lines) + "\n"
    r = run_script(stdin, timeout=30)
    assert r.returncode == 0, r.stderr
    out_ids = r.stdout.split()
    assert out_ids == sorted(out_ids)  # plain string ascending
    assert len(out_ids) >= 1
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
