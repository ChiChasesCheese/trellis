import random

import pytest

EXAMPLE_ADDS = [
    ("DANNON", 1000, "2020-11-02T14:00:00Z"),
    ("UNILEVER", 200, "2020-10-31T11:00:00Z"),
    ("DANNON", -200, "2020-10-31T15:00:00Z"),
    ("MILLER COORS", 10000, "2020-11-01T14:00:00Z"),
    ("DANNON", 300, "2020-10-31T10:00:00Z"),
]
EXAMPLE_LINES = [f"ADD,{p},{n},{t}" for p, n, t in EXAMPLE_ADDS]


def account(impl, adds):
    a = impl.PointsAccount()
    for p, n, t in adds:
        a.add(p, n, t)
    return a


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example_balances_before_spend(impl):
    a = account(impl, EXAMPLE_ADDS)
    assert a.balances() == {"DANNON": 1100, "UNILEVER": 200, "MILLER COORS": 10000}
    assert list(a.balances()) == ["DANNON", "UNILEVER", "MILLER COORS"]  # first-add order


@pytest.mark.part1
@pytest.mark.edge
def test_empty_and_zero(impl):
    assert impl.PointsAccount().balances() == {}
    a = account(impl, [("A", 0, "2021-01-01T00:00:00Z")])
    assert a.balances() == {"A": 0}
    assert impl.process([]) == []


@pytest.mark.part1
@pytest.mark.fmt
def test_balance_line_format(impl):
    assert impl.process(EXAMPLE_LINES + ["BALANCE"]) == ["DANNON,1100;UNILEVER,200;MILLER COORS,10000"]


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example_spend_verbatim(impl):
    a = account(impl, EXAMPLE_ADDS)
    assert a.spend(5000) == [("DANNON", -100), ("UNILEVER", -200), ("MILLER COORS", -4700)]
    assert a.balances() == {"DANNON": 1000, "UNILEVER": 0, "MILLER COORS": 5300}


@pytest.mark.part2
@pytest.mark.edge
def test_fifo_ignores_insertion_order(impl):
    a = account(impl, [("B", 100, "2021-01-02T00:00:00Z"), ("A", 100, "2021-01-01T00:00:00Z")])
    assert a.spend(150) == [("A", -100), ("B", -50)]


@pytest.mark.part2
@pytest.mark.edge
def test_same_timestamp_insertion_order_and_aggregation(impl):
    a = account(impl, [("A", 10, "2021-01-01T00:00:00Z"), ("B", 10, "2021-01-01T00:00:00Z"),
                       ("A", 10, "2021-01-01T00:00:00Z")])
    assert a.spend(25) == [("A", -15), ("B", -10)]  # A's two entries aggregated, first-consumption order


@pytest.mark.part2
@pytest.mark.edge
def test_naive_and_zulu_timestamps_compare(impl):
    a = account(impl, [("A", 10, "2021-01-01 00:00:00"), ("B", 10, "2020-12-31T00:00:00Z")])
    assert a.spend(10) == [("B", -10)]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_negative_cancels_oldest_positive_of_that_payer(impl):
    # -200 dated 15:00 cancels the 300 dated 10:00 -> DANNON contributes 100 first
    a = account(impl, EXAMPLE_ADDS)
    assert a.spend(100) == [("DANNON", -100)]
    assert a.spend(1) == [("UNILEVER", -1)]


@pytest.mark.part3
@pytest.mark.edge
def test_negative_before_any_positive_of_payer(impl):
    a = impl.PointsAccount()
    a.add("A", 50, "2021-01-01T00:00:00Z")
    with pytest.raises(ValueError):
        a.add("A", -80, "2021-01-03T00:00:00Z")
    a.add("A", 100, "2021-01-05T00:00:00Z")
    a.add("A", -80, "2021-01-03T00:00:00Z")    # now fine: 150 - 80 = 70
    assert a.balances() == {"A": 70}
    assert a.spend(70) == [("A", -70)]
    assert a.balances() == {"A": 0}


@pytest.mark.part3
@pytest.mark.edge
def test_negative_exactly_cancels(impl):
    a = account(impl, [("A", 100, "2021-01-01T00:00:00Z"), ("A", -100, "2021-01-02T00:00:00Z"),
                       ("B", 5, "2021-01-03T00:00:00Z")])
    assert a.spend(5) == [("B", -5)]
    assert a.balances() == {"A": 0, "B": 0}


@pytest.mark.part3
def test_example_lines_negative_add_error(impl):
    out = impl.process(["ADD,A,50,2021-01-01T00:00:00Z", "ADD,A,-80,2021-01-03T00:00:00Z",
                        "ADD,A,100,2021-01-05T00:00:00Z", "ADD,A,-80,2021-01-03T00:00:00Z", "SPEND,70"])
    assert out == ["ERROR", "A,-70"]


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example_multiple_spends_and_error(impl):
    out = impl.process(["ADD,A,100,2021-01-01T00:00:00Z", "ADD,B,100,2021-01-02T00:00:00Z",
                        "SPEND,150", "SPEND,100", "SPEND,50", "BALANCE"])
    assert out == ["A,-100;B,-50", "ERROR", "B,-50", "A,0;B,0"]


@pytest.mark.part4
@pytest.mark.edge
def test_spend_boundary_exact_one_over_zero(impl):
    a = account(impl, [("A", 100, "2021-01-01T00:00:00Z")])
    with pytest.raises(ValueError):
        a.spend(101)
    assert a.balances() == {"A": 100}          # unchanged
    assert a.spend(0) == []
    assert a.spend(100) == [("A", -100)]
    with pytest.raises(ValueError):
        a.spend(1)


@pytest.mark.part4
@pytest.mark.fmt
def test_spend_zero_prints_empty_line(impl):
    assert impl.process(["ADD,A,1,2021-01-01T00:00:00Z", "SPEND,0", "SPEND,-1"]) == ["", "ERROR"]


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EXAMPLE_LINES + ["BALANCE", "SPEND,5000", "BALANCE"]) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == ("DANNON,1100;UNILEVER,200;MILLER COORS,10000\n"
                        "DANNON,-100;UNILEVER,-200;MILLER COORS,-4700\n"
                        "DANNON,1000;UNILEVER,0;MILLER COORS,5300\n")
    assert run_script("").stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_adds_with_spends(run_script):
    rng = random.Random(0)
    lines, bal = [], {}
    for i in range(100_000):
        p = f"P{rng.randrange(50)}"
        n = rng.randrange(1, 1000)
        if rng.random() < 0.2 and bal.get(p, 0) >= n:
            n = -n
        bal[p] = bal.get(p, 0) + n
        ts = f"2021-01-01T{rng.randrange(24):02d}:{rng.randrange(60):02d}:{rng.randrange(60):02d}Z"
        lines.append(f"ADD,{p},{n},{ts}")
        if i % 10_000 == 9_999:
            lines.append("SPEND,1000")
            lines.append("BALANCE")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == 20 and "ERROR" not in r.stdout
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
