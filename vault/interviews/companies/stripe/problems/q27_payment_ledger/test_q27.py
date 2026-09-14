import random

import pytest

EX1 = [
    "PAYMENT p1 1000 2026-03-01T10:00:00", "PAYMENT p2 2500 2026-03-01T12:30:00",
    "PAYMENT p1 1000 2026-03-02T00:00:00", "PAYMENT p1 999 2026-03-01T10:00:00",
    "PAYMENT p3 0 2026-03-01T13:00:00", "PAYMENT p4 500 2026-03-01", "REVENUE",
    "REFUND r1 p1 400 2026-03-01T11:00:00", "REFUND r1 p1 400 2026-03-05T00:00:00",
    "REFUND r2 p1 600 2026-03-02T09:00:00", "REFUND r3 p1 1 2026-03-02T09:30:00",
    "REFUND r4 p2 100 2026-03-01T12:00:00", "REFUND r5 px 100 2026-03-01T12:00:00", "REVENUE",
    "REVENUE 2026-03-01T00:00:00 2026-03-01T23:59:59", "REVENUE 2026-03-02T09:00:00 2026-03-02T09:00:00",
    "PAYMENTS 2026-03-01", "PAYMENTS 2026-03-02", "TRANSACTIONS",
]
EX1_OUT = ["OK", "OK", "OK", "REJECTED", "REJECTED", "REJECTED", "3500",
           "OK", "OK", "OK", "REJECTED", "REJECTED", "REJECTED", "2500", "3100", "-600",
           "p1,p2", "NONE",
           "payment,p1,1000,1000", "refund,r1,-400,600", "payment,p2,2500,3100", "refund,r2,-600,2500"]
EX2 = ["PAYMENT b 100 2026-01-01T00:00:00", "PAYMENT a 100 2026-01-01T00:00:00",
       "PAYMENT c 100 2025-12-31T23:59:59", "REFUND z a 100 2026-01-01T00:00:00",
       "PAYMENTS 2026-01-01", "PAYMENTS 2025-12-31", "TRANSACTIONS"]
EX2_OUT = ["OK", "OK", "OK", "OK", "a,b", "c",
           "payment,c,100,100", "payment,a,100,200", "payment,b,100,300", "refund,z,-100,200"]
EX3 = ["REVENUE", "PAYMENTS 2026-01-01", "TRANSACTIONS", "REVENUE 2026-01-01 2026-01-02",
       "PAYMENT p1 12.5 2026-01-01T00:00:00", "FOO"]
EX3_OUT = ["0", "NONE", "NONE", "ERROR", "ERROR", "ERROR"]

T = "2026-03-01T10:00:00"


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_add_payment_idempotency(impl):
    led = impl.PaymentLedger()
    assert led.add_payment("p1", 1000, T) is True
    assert led.add_payment("p1", 1000, "2026-04-01T00:00:00") is True     # replay, ts ignored
    assert led.add_payment("p1", 1001, T) is False                        # different amount
    assert led.add_payment("p1", 1000, "garbage") is True                  # replay wins before validation
    assert led.get_total_revenue() == 1000
    assert len(led.get_balance_transactions()) == 1


@pytest.mark.part1
@pytest.mark.edge
def test_add_payment_rejects_zero_negative_and_bad_ts(impl):
    led = impl.PaymentLedger()
    assert led.add_payment("z", 0, T) is False
    assert led.add_payment("n", -5, T) is False
    for bad in ["2026-03-01", "2026-03-01 10:00:00", "2026-02-30T00:00:00", "2026-03-01T24:00:00",
                "2026-3-1T10:00:00", "2026-03-01T10:00:00Z", "2026-03-01T10:00"]:
        assert led.add_payment("b" + bad, 100, bad) is False, bad
    assert led.get_total_revenue() == 0
    assert led.add_payment("z", 1, T) is True                              # a rejected id is not reserved


@pytest.mark.part1
def test_part1_stream_and_large_amounts(impl):
    lines = ["PAYMENT a 1000000000 2026-01-01T00:00:00"] * 3 + ["PAYMENT b 1000000000 2026-01-01T00:00:01", "REVENUE",
             "REFUND r a 1 2026-01-01T00:00:02", "PAYMENTS 2026-01-01"]
    assert impl.part1(lines) == ["OK", "OK", "OK", "OK", "2000000000", "ERROR", "ERROR"]
    assert impl.part1([]) == []


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
@pytest.mark.edge
def test_partial_refunds_cap_boundary(impl):
    led = impl.PaymentLedger()
    led.add_payment("p", 1000, T)
    assert led.add_refund("r1", "p", 300, "2026-03-01T11:00:00") is True
    assert led.add_refund("r2", "p", 701, "2026-03-01T11:00:00") is False   # one cent over
    assert led.add_refund("r3", "p", 700, "2026-03-01T11:00:00") is True    # exactly the remainder
    assert led.add_refund("r4", "p", 1, "2026-03-01T11:00:00") is False
    assert led.get_total_revenue() == 0
    # rejected r2 did not consume the cap: only r1 + r3 recorded
    assert [r[1] for r in led.get_balance_transactions()] == ["p", "r1", "r3"]


@pytest.mark.part2
@pytest.mark.edge
def test_refund_timestamp_rules(impl):
    led = impl.PaymentLedger()
    led.add_payment("p", 100, T)
    assert led.add_refund("a", "p", 10, "2026-03-01T09:59:59") is False    # one second before
    assert led.add_refund("b", "p", 10, T) is True                          # same second
    assert led.add_refund("c", "p", 10, "2026-03-01") is False              # bad ts
    assert led.add_refund("d", "p", 0, T) is False
    assert led.add_refund("e", "p", -1, T) is False
    assert led.add_refund("f", "nope", 10, T) is False
    assert led.get_total_revenue() == 90


@pytest.mark.part2
@pytest.mark.edge
def test_refund_idempotency(impl):
    led = impl.PaymentLedger()
    led.add_payment("p", 100, T)
    led.add_payment("q", 100, T)
    assert led.add_refund("r", "p", 60, T) is True
    assert led.add_refund("r", "p", 60, "2026-03-09T00:00:00") is True     # replay
    assert led.add_refund("r", "p", 50, T) is False                         # same id, other amount
    assert led.add_refund("r", "q", 60, T) is False                         # same id, other payment
    assert led.get_total_revenue() == 140
    assert led.add_refund("s", "p", 40, T) is True                          # cap counts r once


@pytest.mark.part2
def test_part2_stream_gates_part3_commands(impl):
    lines = ["PAYMENT p 100 " + T, "REFUND r p 100 " + T, "REVENUE", "REVENUE " + T + " " + T, "PAYMENTS 2026-03-01"]
    assert impl.part2(lines) == ["OK", "OK", "0", "ERROR", "ERROR"]


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example1_verbatim(impl):
    assert impl.part4(EX1) == EX1_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_range_revenue_inclusive_bounds_and_open_ends(impl):
    led = impl.PaymentLedger()
    led.add_payment("a", 100, "2026-03-01T10:00:00")
    led.add_payment("b", 200, "2026-03-01T10:00:01")
    led.add_payment("c", 400, "2026-03-03T00:00:00")
    led.add_refund("r", "a", 50, "2026-03-02T00:00:00")
    q = led.get_total_revenue
    assert q("2026-03-01T10:00:00", "2026-03-01T10:00:00") == 100          # == both ends
    assert q("2026-03-01T10:00:01", "2026-03-01T10:00:01") == 200
    assert q("2026-03-01T09:59:59", "2026-03-01T10:00:00") == 100
    assert q("2026-03-01T10:00:02", "2026-03-01T23:59:59") == 0
    assert q("2026-03-02T00:00:00", "2026-03-02T23:59:59") == -50           # refund alone -> negative
    assert q("2026-03-01T00:00:00", "2026-03-03T00:00:00") == 650
    assert q("2026-03-01T00:00:00", "2026-03-02T23:59:59") == 250
    assert q(None, "2026-03-01T23:59:59") == 300
    assert q("2026-03-02T00:00:00", None) == 350
    assert q("2026-03-05T00:00:00", "2026-03-01T00:00:00") == 0             # empty range
    assert q() == 650


@pytest.mark.part3
@pytest.mark.edge
def test_range_query_bad_timestamp_raises(impl):
    led = impl.PaymentLedger()
    with pytest.raises(ValueError):
        led.get_total_revenue("2026-03-01", "2026-03-02T00:00:00")
    with pytest.raises(ValueError):
        led.get_payments_by_date("2026-3-1")
    with pytest.raises(ValueError):
        led.get_payments_by_date("2026-02-30")


@pytest.mark.part3
@pytest.mark.fmt
def test_payments_by_date_sorted_ts_then_id_ignores_refunds(impl):
    led = impl.PaymentLedger()
    led.add_payment("p10", 1, "2026-03-01T23:59:59")
    led.add_payment("p2", 1, "2026-03-01T23:59:59")
    led.add_payment("a", 1, "2026-03-01T00:00:00")
    led.add_payment("next", 1, "2026-03-02T00:00:00")
    led.add_refund("r", "a", 1, "2026-03-01T00:00:00")
    assert led.get_payments_by_date("2026-03-01") == ["a", "p10", "p2"]
    assert led.get_payments_by_date("2026-03-02") == ["next"]
    assert led.get_payments_by_date("2026-03-03") == []


@pytest.mark.part3
def test_example2_verbatim(impl):
    assert impl.part4(EX2) == EX2_OUT


# ---------------------------------------------------------------- Part 4
@pytest.mark.part4
def test_example3_verbatim(impl):
    assert impl.part4(EX3) == EX3_OUT


@pytest.mark.part4
@pytest.mark.fmt
def test_balance_transactions_rows_and_running_net(impl):
    led = impl.PaymentLedger()
    led.add_payment("b", 500, "2026-01-02T00:00:00")
    led.add_payment("a", 300, "2026-01-01T00:00:00")
    led.add_payment("a", 300, "2026-01-01T00:00:00")             # replay: no extra row
    led.add_refund("r2", "a", 100, "2026-01-02T00:00:00")        # same ts as payment b -> after it
    led.add_refund("r1", "a", 100, "2026-01-02T00:00:00")        # same ts -> id order r1 < r2
    led.add_refund("bad", "a", 500, "2026-01-02T00:00:00")       # rejected: no row
    assert led.get_balance_transactions() == [
        ("payment", "a", 300, 300), ("payment", "b", 500, 800),
        ("refund", "r1", -100, 700), ("refund", "r2", -100, 600)]
    assert led.get_total_revenue() == 600


@pytest.mark.part4
@pytest.mark.edge
def test_stream_validation_whitespace_and_case(impl):
    out = impl.part4(["", "  payment  p1  100  " + T, "PAYMENT p1 100", "REFUND r p1 x " + T, "REVENUE x",
                      "PAYMENTS", "transactions", "REVENUE"])
    assert out == ["OK", "ERROR", "ERROR", "ERROR", "ERROR", "payment,p1,100,100", "100"]


@pytest.mark.part4
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(EX1) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(EX1_OUT) + "\n"
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part4
@pytest.mark.perf
def test_perf_100k_events_with_range_queries(run_script):
    rng = random.Random(0)
    lines = []
    n_pay = 70_000
    for i in range(n_pay):
        ts = f"2025-{rng.randrange(1, 13):02d}-{rng.randrange(1, 29):02d}T{rng.randrange(24):02d}:{rng.randrange(60):02d}:{rng.randrange(60):02d}"
        lines.append(f"PAYMENT p{i} {rng.randrange(1, 10 ** 9)} {ts}")
    for i in range(30_000):
        lines.append(f"REFUND r{i} p{rng.randrange(n_pay)} {rng.randrange(1, 1000)} 2026-01-{rng.randrange(1, 29):02d}T00:00:00")
        if i % 150 == 0:
            m1, m2 = sorted(rng.sample(range(1, 13), 2))
            lines.append(f"REVENUE 2025-{m1:02d}-01T00:00:00 2025-{m2:02d}-28T23:59:59")
            lines.append(f"PAYMENTS 2025-{m1:02d}-15")
    lines += ["REVENUE", "TRANSACTIONS"]
    r = run_script("\n".join(lines) + "\n", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") >= len(lines)
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256
