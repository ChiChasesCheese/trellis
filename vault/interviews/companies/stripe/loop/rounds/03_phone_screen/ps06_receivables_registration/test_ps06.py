import random

import pytest

HEADER = "customer_id,merchant_id,payout_date,card_type,amount"

PART1_EXAMPLE = [
    HEADER,
    "c1,m1,2026-08-03,visa,150.00",
    "c2,m1,2026-08-03,visa,50.00",
    "c3,m1,2026-08-03,mastercard,20.00",
    "c4,m2,2026-08-04,visa,100.00",
]
PART1_EXAMPLE_OUT = [
    "m1,mastercard,2026-08-03,20.00",
    "m1,visa,2026-08-03,200.00",
    "m2,visa,2026-08-04,100.00",
]

PART2_EXAMPLE = [
    HEADER,
    "c1,m1,2026-08-08,visa,150.00",
    "c2,m1,2026-08-10,visa,50.00",
    "c3,m1,2026-08-09,visa,-30.00",
    "c4,m2,2026-08-04,visa,BAD",
    "c5,m2,2026-08-04",
    "c6,m3,2026-13-01,visa,10.00",
]
PART2_EXAMPLE_OUT = ["m1,visa,2026-08-10,170.00", "SKIPPED 3"]


# ---------------------------------------------------------------- Part 1: happy-path aggregation
@pytest.mark.part1
def test_example_aggregation(impl):
    assert impl.part1(PART1_EXAMPLE) == PART1_EXAMPLE_OUT


@pytest.mark.part1
def test_single_row(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,10.00"]
    assert impl.part1(rows) == ["m1,visa,2026-08-03,10.00"]


@pytest.mark.part1
@pytest.mark.edge
def test_duplicate_customer_rows_merge_not_overwrite(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,10.00", "c1,m1,2026-08-03,visa,10.00"]
    assert impl.part1(rows) == ["m1,visa,2026-08-03,20.00"]


@pytest.mark.part1
@pytest.mark.edge
def test_header_only_no_rows(impl):
    assert impl.part1([HEADER]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_sort_by_merchant_then_date_then_card_type(impl):
    rows = [
        HEADER,
        "c1,m2,2026-08-01,visa,1.00",
        "c2,m1,2026-08-02,visa,1.00",
        "c3,m1,2026-08-01,mastercard,1.00",
        "c4,m1,2026-08-01,visa,1.00",
    ]
    out = impl.part1(rows)
    assert out == [
        "m1,mastercard,2026-08-01,1.00",
        "m1,visa,2026-08-01,1.00",
        "m1,visa,2026-08-02,1.00",
        "m2,visa,2026-08-01,1.00",
    ]


@pytest.mark.part1
@pytest.mark.edge
def test_part1_does_not_roll_weekend_dates(impl):
    rows = [HEADER, "c1,m1,2026-08-08,visa,10.00"]  # Saturday stays Saturday in Part 1
    assert impl.part1(rows) == ["m1,visa,2026-08-08,10.00"]


@pytest.mark.part1
@pytest.mark.fmt
def test_totals_have_no_thousands_separator_and_sub_unit_negative_keeps_zero(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,1234567.89", "c2,m2,2026-08-03,visa,-0.05"]
    assert impl.part1(rows) == ["m1,visa,2026-08-03,1234567.89", "m2,visa,2026-08-03,-0.05"]


@pytest.mark.part1
def test_blank_lines_ignored(impl):
    rows = [HEADER, "", "c1,m1,2026-08-03,visa,10.00", "   "]
    assert impl.part1(rows) == ["m1,visa,2026-08-03,10.00"]


# ---------------------------------------------------------------- Part 2: robustness + weekend
@pytest.mark.part2
def test_example_skip_and_roll(impl):
    assert impl.part2(PART2_EXAMPLE) == PART2_EXAMPLE_OUT


@pytest.mark.part2
def test_skipped_zero_still_printed(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,10.00"]
    assert impl.part2(rows) == ["m1,visa,2026-08-03,10.00", "SKIPPED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_negative_amount_can_make_total_negative(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,-30.00"]
    assert impl.part2(rows) == ["m1,visa,2026-08-03,-30.00", "SKIPPED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_total_can_net_to_exactly_zero(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,30.00", "c2,m1,2026-08-03,visa,-30.00"]
    assert impl.part2(rows) == ["m1,visa,2026-08-03,0.00", "SKIPPED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_weekday_dates_do_not_roll(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa,10.00"]  # Monday
    assert impl.part2(rows) == ["m1,visa,2026-08-03,10.00", "SKIPPED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_saturday_and_sunday_both_roll_to_same_monday(impl):
    rows = [
        HEADER,
        "c1,m1,2026-08-08,visa,10.00",  # Saturday -> Monday 08-10
        "c2,m1,2026-08-09,visa,5.00",  # Sunday -> Monday 08-10
    ]
    assert impl.part2(rows) == ["m1,visa,2026-08-10,15.00", "SKIPPED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_weekend_roll_crosses_month_boundary(impl):
    # 2026-01-31 is a Saturday -> rolls to 2026-02-02 Monday
    rows = [HEADER, "c1,m1,2026-01-31,visa,10.00"]
    assert impl.part2(rows) == ["m1,visa,2026-02-02,10.00", "SKIPPED 0"]


@pytest.mark.part2
@pytest.mark.edge
def test_bad_field_count_skipped(impl):
    rows = [HEADER, "c1,m1,2026-08-03,visa"]  # missing amount
    assert impl.part2(rows) == ["SKIPPED 1"]


@pytest.mark.part2
@pytest.mark.edge
def test_bad_amount_formats_skipped(impl):
    rows = [
        HEADER,
        "c1,m1,2026-08-03,visa,150.5",  # one decimal digit
        "c2,m1,2026-08-03,visa,150",  # no decimal point
        "c3,m1,2026-08-03,visa,abc",  # not numeric
        "c4,m1,2026-08-03,visa,",  # empty
    ]
    assert impl.part2(rows) == ["SKIPPED 4"]


@pytest.mark.part2
@pytest.mark.edge
def test_bad_date_formats_skipped(impl):
    rows = [
        HEADER,
        "c1,m1,2026-13-01,visa,10.00",  # invalid month
        "c2,m1,2026-02-30,visa,10.00",  # invalid day (not a real date)
        "c3,m1,2026/08/03,visa,10.00",  # wrong separator
    ]
    assert impl.part2(rows) == ["SKIPPED 3"]


@pytest.mark.part2
def test_multiple_merchants_partial_skip(impl):
    rows = [
        HEADER,
        "c1,m1,2026-08-03,visa,10.00",
        "c2,m2,2026-08-03,visa,BAD",
        "c3,m2,2026-08-04,mastercard,5.00",
    ]
    out = impl.part2(rows)
    assert out == ["m1,visa,2026-08-03,10.00", "m2,mastercard,2026-08-04,5.00", "SKIPPED 1"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(PART1_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(PART1_EXAMPLE_OUT) + "\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\n" + "\n".join(PART2_EXAMPLE) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(PART2_EXAMPLE_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_stdin_header_only(run_script):
    r = run_script("PART 1\n" + HEADER + "\n")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part2
@pytest.mark.perf
def test_perf_100k_rows(run_script):
    rng = random.Random(0)
    merchants = [f"m{i}" for i in range(200)]
    cards = ["visa", "mastercard", "amex", "elo"]
    lines = [HEADER]
    expected_bad = 0
    for i in range(100_000):
        merchant = rng.choice(merchants)
        card = rng.choice(cards)
        day = rng.randrange(1, 28)
        date_str = f"2026-08-{day:02d}"
        cents = rng.randrange(-100_000, 100_000)
        amount = f"{cents / 100:.2f}"
        if i % 5000 == 0:  # sprinkle a few malformed rows
            lines.append(f"c{i},{merchant},{date_str},{card}")  # missing amount field
            expected_bad += 1
        else:
            lines.append(f"c{i},{merchant},{date_str},{card},{amount}")
    r = run_script("PART 2\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out_lines = r.stdout.splitlines()
    assert out_lines[-1] == f"SKIPPED {expected_bad}"
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
