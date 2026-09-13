import random

import pytest

P1_LINES = [
    "RATES",
    "US,widget,5.00",
    "CA,widget,7.25",
    "ORDERS",
    "o1,US,widget,3",
    "o2,CA,widget,2",
    "o3,US,gadget,1",
]
P1_OUT = ["o1: $15.00", "o2: $14.50", "o3: ERROR unknown product US/gadget"]

P2_LINES = [
    "RATES",
    "US,widget,21,inf,4.00",  # deliberately unsorted
    "US,widget,1,10,5.00",
    "US,widget,11,20,4.50",
    "ORDERS",
    "o1,US,widget,5",
    "o2,US,widget,15",
    "o3,US,widget,50",
]
P2_OUT = ["o1: $25.00", "o2: $67.50", "o3: $200.00"]

P3_LINES = [
    "RATES",
    "US,widget,1,10,5.00,incremental",
    "US,widget,11,20,4.50,incremental",
    "US,widget,21,inf,4.00,incremental",
    "CA,widget,1,10,5.00,fixed",
    "CA,widget,11,20,4.50,fixed",
    "ORDERS",
    "o1,US,widget,15",
    "o2,CA,widget,15",
]
P3_OUT = ["o1: $72.50", "o2: $67.50"]

P3_GAP_LINES = [
    "RATES",
    "US,widget,1,10,5.00,incremental",
    "US,widget,15,inf,3.00,incremental",
    "ORDERS",
    "o1,US,widget,5",
    "o2,US,widget,20",
]
P3_GAP_OUT = ["o1: $25.00", "o2: ERROR incremental gap for US/widget at qty=20"]


# ---------------------------------------------------------------- Part 1: flat unit price
@pytest.mark.part1
def test_example_flat(impl):
    assert impl.part1(P1_LINES) == P1_OUT


@pytest.mark.part1
@pytest.mark.edge
def test_unknown_product_error(impl):
    lines = ["RATES", "US,widget,5.00", "ORDERS", "o1,FR,widget,1"]
    assert impl.part1(lines) == ["o1: ERROR unknown product FR/widget"]


@pytest.mark.part1
@pytest.mark.edge
def test_zero_quantity_known_product(impl):
    lines = ["RATES", "US,widget,5.00", "ORDERS", "o1,US,widget,0"]
    assert impl.part1(lines) == ["o1: $0.00"]


@pytest.mark.part1
@pytest.mark.edge
def test_zero_quantity_unknown_product_still_errors(impl):
    lines = ["RATES", "US,widget,5.00", "ORDERS", "o1,US,gadget,0"]
    assert impl.part1(lines) == ["o1: ERROR unknown product US/gadget"]


@pytest.mark.part1
@pytest.mark.fmt
def test_money_decimal_digit_variants(impl):
    lines = ["RATES", "US,a,5", "US,b,5.5", "US,c,5.50", "ORDERS", "o1,US,a,2", "o2,US,b,2", "o3,US,c,2"]
    assert impl.part1(lines) == ["o1: $10.00", "o2: $11.00", "o3: $11.00"]


@pytest.mark.part1
def test_output_is_input_order_not_sorted(impl):
    lines = ["RATES", "US,widget,1.00", "ORDERS", "z1,US,widget,1", "a1,US,widget,1"]
    assert impl.part1(lines) == ["z1: $1.00", "a1: $1.00"]


# ---------------------------------------------------------------- Part 2: quantity tiers
@pytest.mark.part2
def test_example_tiered(impl):
    assert impl.part2(P2_LINES) == P2_OUT


@pytest.mark.part2
@pytest.mark.edge
def test_band_boundaries_inclusive_both_ends(impl):
    lines = [
        "RATES",
        "US,widget,1,10,5.00",
        "US,widget,11,20,4.50",
        "ORDERS",
        "o1,US,widget,10",
        "o2,US,widget,11",
    ]
    assert impl.part2(lines) == ["o1: $50.00", "o2: $49.50"]


@pytest.mark.part2
@pytest.mark.edge
def test_gap_between_bands_errors(impl):
    lines = ["RATES", "US,widget,1,10,5.00", "US,widget,15,inf,3.00", "ORDERS", "o1,US,widget,12"]
    assert impl.part2(lines) == ["o1: ERROR no tier for US/widget at qty=12"]


@pytest.mark.part2
@pytest.mark.edge
def test_open_ended_top_band(impl):
    lines = ["RATES", "US,widget,1,10,5.00", "US,widget,11,inf,1.00", "ORDERS", "o1,US,widget,1000000"]
    assert impl.part2(lines) == ["o1: $1000000.00"]


@pytest.mark.part2
def test_zero_quantity_tiered(impl):
    lines = ["RATES", "US,widget,1,10,5.00", "ORDERS", "o1,US,widget,0"]
    assert impl.part2(lines) == ["o1: $0.00"]


@pytest.mark.part2
@pytest.mark.edge
def test_unsorted_rate_table_still_correct(impl):
    # P2_LINES already lists the top band before the bottom two on purpose
    assert impl.part2(P2_LINES) == P2_OUT


# ---------------------------------------------------------------- Part 3: mixed incremental/fixed
@pytest.mark.part3
def test_example_mixed(impl):
    assert impl.part3(P3_LINES) == P3_OUT


@pytest.mark.part3
def test_fixed_matches_part2_exactly(impl):
    # same ladder+quantity as P2_LINES' o2, now explicitly typed 'fixed' -> same $67.50
    lines = ["RATES", "US,widget,1,10,5.00,fixed", "US,widget,11,20,4.50,fixed", "ORDERS", "o1,US,widget,15"]
    assert impl.part3(lines) == ["o1: $67.50"]


@pytest.mark.part3
@pytest.mark.edge
def test_incremental_gap_only_when_order_crosses_it(impl):
    assert impl.part3(P3_GAP_LINES) == P3_GAP_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_incremental_vs_fixed_same_quantity_different_totals(impl):
    lines = [
        "RATES",
        "US,widget,1,10,5.00,incremental",
        "US,widget,11,20,4.50,incremental",
        "CA,widget,1,10,5.00,fixed",
        "CA,widget,11,20,4.50,fixed",
        "ORDERS",
        "o1,US,widget,15",
        "o2,CA,widget,15",
    ]
    assert impl.part3(lines) == ["o1: $72.50", "o2: $67.50"]


@pytest.mark.part3
@pytest.mark.edge
def test_incremental_first_band_boundary_exact(impl):
    # quantity == 10 exactly: entirely inside the first band, 10 * 5.00 = 50.00
    lines = [
        "RATES",
        "US,widget,1,10,5.00,incremental",
        "US,widget,11,20,4.50,incremental",
        "ORDERS",
        "o1,US,widget,10",
    ]
    assert impl.part3(lines) == ["o1: $50.00"]


@pytest.mark.part3
@pytest.mark.edge
def test_incremental_reaches_open_ended_top_band(impl):
    # 10 @ 5.00 + 10 @ 4.50 + 30 @ 4.00 = 50 + 45 + 120 = 215.00 (the 'inf' band charges qty - 20 units)
    lines = P3_LINES[:6] + ["ORDERS", "o1,US,widget,50"]
    assert impl.part3(lines) == ["o1: $215.00"]


@pytest.mark.part3
def test_no_tier_error_same_message_as_part2(impl):
    lines = [
        "RATES",
        "US,widget,1,10,5.00,incremental",
        "US,widget,15,inf,3.00,incremental",
        "ORDERS",
        "o1,US,widget,12",
    ]
    assert impl.part3(lines) == ["o1: ERROR no tier for US/widget at qty=12"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_exact_part1(run_script):
    r = run_script("PART 1\n" + "\n".join(P1_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P1_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact_part3(run_script):
    r = run_script("PART 3\n" + "\n".join(P3_LINES) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(P3_OUT) + "\n"


@pytest.mark.part1
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part1
@pytest.mark.perf
def test_perf_100k_orders(run_script):
    rng = random.Random(0)
    countries = ["US", "CA", "UK", "FR", "DE"]
    products = ["widget", "gadget", "gizmo"]
    rate_lines = ["RATES"]
    for c in countries:
        for p in products:
            rate_lines.append(f"{c},{p},{rng.randrange(1, 20)}.{rng.randrange(0, 99):02d}")
    rate_lines.append("ORDERS")
    order_lines = [
        f"o{i},{rng.choice(countries)},{rng.choice(products)},{rng.randrange(0, 1000)}"
        for i in range(100_000)
    ]
    stdin_text = "PART 1\n" + "\n".join(rate_lines + order_lines) + "\n"
    r = run_script(stdin_text, timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 100_000
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
