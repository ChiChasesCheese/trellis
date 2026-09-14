import random
from decimal import Decimal

import pytest

EX1 = ["alice,10.00", "bob,25.50", "alice,5.00", "carol,25.50"]
EX3 = [
    "2024-01-01,alice,10.00",
    "2024-01-01,bob,5.00",
    "2024-01-02,alice,1.00",
    "2024-01-02,bob,1.00",
    "2024-01-02,carol,3.00",
]
EX4 = ["alice,10.00", "QUERY", "bob,50.00", "QUERY", "alice,-3.00", "QUERY", "bob,-60.00", "QUERY"]


def _brute_totals(records, allow_negative):
    totals = {}
    for rec in records:
        user, amount = rec.split(",")
        totals[user] = totals.get(user, Decimal(0)) + Decimal(amount)
    return {u: int(v * 100) for u, v in totals.items()}


# ------------------------------------------------------------------------ Part 1
@pytest.mark.part1
def test_worked_example_1(impl):
    assert impl.top_two_users(EX1) == [("bob", 2550), ("carol", 2550)]


@pytest.mark.part1
def test_worked_example_2_single_user(impl):
    assert impl.top_two_users(["alice,10.00"]) == [("alice", 1000)]


@pytest.mark.part1
@pytest.mark.edge
def test_empty_records(impl):
    assert impl.top_two_users([]) == []


@pytest.mark.part1
@pytest.mark.edge
def test_negative_amount_raises(impl):
    with pytest.raises(ValueError):
        impl.top_two_users(["alice,-5.00"])


@pytest.mark.part1
@pytest.mark.edge
@pytest.mark.parametrize("bad", ["alice,5", "alice,5.001", "alice,5.1", "alice", ",5.00", "alice,5.00,x"])
def test_malformed_record_raises(impl, bad):
    with pytest.raises(ValueError):
        impl.top_two_users([bad])


@pytest.mark.part1
@pytest.mark.edge
def test_many_small_amounts_no_float_drift(impl):
    # 1000 * 0.10 must sum to exactly 10000 cents -- a float accumulator can drift off by one.
    records = [f"alice,0.10"] * 1000
    assert impl.top_two_users(records) == [("alice", 10000)]


@pytest.mark.part1
@pytest.mark.edge
def test_random_against_decimal_brute_force(impl):
    rng = random.Random(0)
    for _ in range(200):
        users = ["alice", "bob", "carol", "dave"][: rng.randint(1, 4)]
        records = [f"{rng.choice(users)},{rng.randint(0, 999)}.{rng.randint(0, 99):02d}" for _ in range(rng.randint(0, 8))]
        expected_totals = _brute_totals(records, allow_negative=False)
        expected = sorted(expected_totals.items(), key=lambda p: (-p[1], p[0]))[:2]
        assert impl.top_two_users(records) == expected, records


# ------------------------------------------------------------------------ Part 2
@pytest.mark.part2
def test_part2_worked_example(impl):
    assert impl.top_k_per_day(EX3, 2) == [
        ("2024-01-01", [("alice", 1000), ("bob", 500)]),
        ("2024-01-02", [("carol", 300), ("alice", 100)]),
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_k_zero_keeps_dates_empty_lists(impl):
    assert impl.top_k_per_day(EX3, 0) == [("2024-01-01", []), ("2024-01-02", [])]


@pytest.mark.part2
@pytest.mark.edge
def test_part2_k_negative_raises(impl):
    with pytest.raises(ValueError):
        impl.top_k_per_day(EX3, -1)


@pytest.mark.part2
@pytest.mark.edge
def test_part2_empty_records(impl):
    assert impl.top_k_per_day([], 2) == []


@pytest.mark.part2
@pytest.mark.edge
def test_part2_malformed_record_raises(impl):
    with pytest.raises(ValueError):
        impl.top_k_per_day(["alice,10.00"], 2)  # missing date field


@pytest.mark.part2
@pytest.mark.fmt
def test_part2_output_lines(impl):
    assert impl.part2(["N 5", *EX3, "K 2"]) == [
        "2024-01-01 2",
        "alice 1000",
        "bob 500",
        "2024-01-02 2",
        "carol 300",
        "alice 100",
    ]


# ------------------------------------------------------------------------ Part 3
@pytest.mark.part3
def test_part3_worked_example(impl):
    assert impl.process_stream(EX4) == [
        [("alice", 1000)],
        [("bob", 5000), ("alice", 1000)],
        [("bob", 5000), ("alice", 700)],
        [("alice", 700), ("bob", -1000)],
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_no_queries_returns_empty(impl):
    assert impl.process_stream(["alice,10.00"]) == []


@pytest.mark.part3
@pytest.mark.edge
def test_part3_query_before_any_purchase(impl):
    assert impl.process_stream(["QUERY"]) == [[]]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_refund_can_go_negative_and_still_rank(impl):
    events = ["alice,5.00", "alice,-10.00", "QUERY"]
    assert impl.process_stream(events) == [[("alice", -500)]]


@pytest.mark.part3
@pytest.mark.edge
def test_part3_malformed_event_raises(impl):
    with pytest.raises(ValueError):
        impl.process_stream(["alice"])


@pytest.mark.part3
@pytest.mark.edge
def test_part3_random_matches_running_totals(impl):
    rng = random.Random(1)
    for _ in range(150):
        users = ["alice", "bob", "carol"]
        totals = {}
        events = []
        expected = []
        for _ in range(rng.randint(0, 12)):
            if rng.random() < 0.3:
                events.append("QUERY")
                ranked = sorted(totals.items(), key=lambda p: (-p[1], p[0]))[:2]
                expected.append(ranked)
            else:
                user = rng.choice(users)
                cents = rng.randint(-999, 999)
                sign = "-" if cents < 0 else ""
                cents_abs = abs(cents)
                events.append(f"{user},{sign}{cents_abs // 100}.{cents_abs % 100:02d}")
                totals[user] = totals.get(user, 0) + cents
        assert impl.process_stream(events) == expected, events


@pytest.mark.part3
@pytest.mark.fmt
def test_part3_output_lines(impl):
    assert impl.part3(["N 8", *EX4]) == [
        "Q 1",
        "alice 1000",
        "Q 2",
        "bob 5000",
        "alice 1000",
        "Q 2",
        "bob 5000",
        "alice 700",
        "Q 2",
        "alice 700",
        "bob -1000",
    ]


@pytest.mark.part3
@pytest.mark.perf
def test_perf_part3_100000_events(run_script):
    rng = random.Random(0)
    users = [f"user{i}" for i in range(2000)]
    lines = []
    n = 100_000
    for _ in range(n):
        if rng.random() < 0.001:
            lines.append("QUERY")
        else:
            user = rng.choice(users)
            lines.append(f"{user},{rng.randint(0, 999)}.{rng.randint(0, 99):02d}")
    r = run_script("PART 3\nN " + str(len(lines)) + "\n" + "\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    assert r.seconds < 2.0, f"took {r.seconds:.2f}s"


# ------------------------------------------------------------------------ io
@pytest.mark.part1
@pytest.mark.io
def test_stdin_stdout_part1(run_script):
    r = run_script("PART 1\nN 2\nalice,10.00\nbob,5.00\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "alice 1000\nbob 500\n"


@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_part2(run_script):
    r = run_script("PART 2\nN 5\n" + "\n".join(EX3) + "\nK 2\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "2024-01-01 2\nalice 1000\nbob 500\n2024-01-02 2\ncarol 300\nalice 100\n"


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_part3(run_script):
    r = run_script("PART 3\nN 8\n" + "\n".join(EX4) + "\n")
    assert r.returncode == 0, r.stderr
    assert "Q 1\nalice 1000\n" in r.stdout
