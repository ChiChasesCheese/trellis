import random

import pytest

CMD_STREAM = [
    "PAY p1 1000 2026-01-01T10:00:00 cus_a",
    "PAY p2 500 2026-01-02T09:00:00 cus_b",
    "PAY p1 999 2026-01-03T00:00:00 cus_a",
    "REFUND r1 p1 300 2026-01-05T00:00:00",
    "REVENUE",
    "RANGE 2026-01-01T00:00:00 2026-01-02T23:59:59",
]
CMD_STREAM_OUT = [
    "PAY p1 OK",
    "PAY p2 OK",
    "PAY p1 DUP",
    "REFUND r1 OK",
    "REVENUE 1200",
    "RANGE 2",
    "p1 1000 2026-01-01T10:00:00 cus_a 300",
    "p2 500 2026-01-02T09:00:00 cus_b 0",
]


def _example_ledger(impl):
    """problem.md Example 1 state (p1 1000 / p2 500 / duplicate p1 ignored) -> revenue 1500."""
    L = impl.PaymentLedger()
    assert L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a") is True
    assert L.add_payment("p2", 500, "2026-01-02T09:00:00", "cus_b") is True
    assert L.add_payment("p1", 999, "2026-01-03T00:00:00", "cus_a") is False
    return L


def _example2_ledger(impl):
    """problem.md Example 2 applied on top of Example 1 -> revenue 800, p1 refunded 700."""
    L = _example_ledger(impl)
    assert L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00") is True
    assert L.add_refund("r2", "p1", 400, "2026-01-06T00:00:00") is True
    return L


# ---------------------------------------------------------------- Part 1
@pytest.mark.part1
def test_example1_verbatim(impl):
    assert _example_ledger(impl).get_total_revenue() == 1500


@pytest.mark.part1
def test_add_payment_and_total_revenue(impl):
    L = impl.PaymentLedger()
    assert L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a") is True
    assert L.add_payment("p2", 500, "2026-01-02T09:00:00", "cus_b") is True
    assert L.get_total_revenue() == 1500


@pytest.mark.part1
def test_duplicate_payment_id_is_idempotent_and_does_not_overwrite(impl):
    L = impl.PaymentLedger()
    assert L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a") is True
    assert L.add_payment("p1", 999, "2026-01-03T00:00:00", "cus_z") is False
    assert L.get_total_revenue() == 1000  # original amount kept, not overwritten
    assert L.get_payments_by_date("2026-01-01T00:00:00", "2026-12-31T23:59:59") == [
        {
            "payment_id": "p1",
            "amount_cents": 1000,
            "ts": "2026-01-01T10:00:00",
            "customer": "cus_a",
            "refunded_cents": 0,
        }
    ]


@pytest.mark.part1
def test_empty_ledger_revenue_is_zero(impl):
    assert impl.PaymentLedger().get_total_revenue() == 0


@pytest.mark.part1
@pytest.mark.edge
def test_zero_amount_payment_is_valid(impl):
    L = impl.PaymentLedger()
    assert L.add_payment("p1", 0, "2026-01-01T00:00:00", "cus_a") is True
    assert L.get_total_revenue() == 0


@pytest.mark.part1
@pytest.mark.edge
def test_invalid_timestamp_shapes_raise_value_error(impl):
    L = impl.PaymentLedger()
    for bad_ts in ["2026-01-01 00:00:00", "2026-02-30T00:00:00", "2026-01-01T25:00:00", "not-a-date", ""]:
        with pytest.raises(ValueError):
            L.add_payment("p", 100, bad_ts, "cus_a")


# ---------------------------------------------------------------- Part 2
@pytest.mark.part2
def test_example2_verbatim(impl):
    L = _example2_ledger(impl)
    assert L.get_total_revenue() == 800
    with pytest.raises(ValueError):
        L.add_refund("r3", "p1", 400, "2026-01-07T00:00:00")  # 700+400 > 1000
    assert L.add_refund("r1", "p1", 300, "2026-01-08T00:00:00") is False  # r1 already applied
    with pytest.raises(KeyError):
        L.add_refund("rX", "ghost", 100, "2026-01-08T00:00:00")
    assert L.get_total_revenue() == 800  # none of the three failures touched state


@pytest.mark.part2
def test_partial_refunds_accumulate_and_reduce_revenue(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    assert L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00") is True
    assert L.add_refund("r2", "p1", 400, "2026-01-06T00:00:00") is True
    assert L.get_total_revenue() == 300


@pytest.mark.part2
@pytest.mark.edge
def test_refund_exactly_remaining_balance_is_allowed_one_cent_over_raises(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    assert L.add_refund("r1", "p1", 1000, "2026-01-05T00:00:00") is True  # exact boundary
    assert L.get_total_revenue() == 0

    L2 = impl.PaymentLedger()
    L2.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    L2.add_refund("r1", "p1", 999, "2026-01-05T00:00:00")
    with pytest.raises(ValueError):
        L2.add_refund("r2", "p1", 2, "2026-01-06T00:00:00")  # 999+2=1001 > 1000


@pytest.mark.part2
@pytest.mark.edge
def test_duplicate_refund_id_is_idempotent_before_amount_check(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    assert L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00") is True
    assert L.add_refund("r1", "p1", 300, "2026-01-06T00:00:00") is False  # dup id, ignored
    assert L.get_total_revenue() == 700  # only the first r1 counted


@pytest.mark.part2
def test_refund_unknown_payment_raises_key_error(impl):
    L = impl.PaymentLedger()
    with pytest.raises(KeyError):
        L.add_refund("r1", "ghost", 100, "2026-01-05T00:00:00")


@pytest.mark.part2
@pytest.mark.edge
def test_refund_invalid_timestamp_raises_before_other_checks(impl):
    L = impl.PaymentLedger()
    with pytest.raises(ValueError):
        L.add_refund("r1", "ghost", 100, "not-a-timestamp")  # bad ts wins over unknown payment


# ---------------------------------------------------------------- Part 3
@pytest.mark.part3
def test_example3_verbatim(impl):
    L = _example2_ledger(impl)
    lo, hi = "2026-01-01T00:00:00", "2026-01-02T23:59:59"
    rows = L.get_payments_by_date(lo, hi)
    assert rows == [
        {
            "payment_id": "p1",
            "amount_cents": 1000,
            "ts": "2026-01-01T10:00:00",
            "customer": "cus_a",
            "refunded_cents": 700,
        },
        {
            "payment_id": "p2",
            "amount_cents": 500,
            "ts": "2026-01-02T09:00:00",
            "customer": "cus_b",
            "refunded_cents": 0,
        },
    ]
    L2 = impl.PaymentLedger.load_json(L.export_json())
    assert L2.get_total_revenue() == L.get_total_revenue() == 800
    assert L2.get_payments_by_date(lo, hi) == rows


@pytest.mark.part3
def test_get_payments_by_date_inclusive_and_sorted(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    L.add_payment("p2", 500, "2026-01-02T09:00:00", "cus_b")
    L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00")
    rows = L.get_payments_by_date("2026-01-01T00:00:00", "2026-01-02T23:59:59")
    assert rows == [
        {
            "payment_id": "p1",
            "amount_cents": 1000,
            "ts": "2026-01-01T10:00:00",
            "customer": "cus_a",
            "refunded_cents": 300,
        },
        {
            "payment_id": "p2",
            "amount_cents": 500,
            "ts": "2026-01-02T09:00:00",
            "customer": "cus_b",
            "refunded_cents": 0,
        },
    ]


@pytest.mark.part3
@pytest.mark.edge
def test_range_boundary_inclusive_one_second_outside_excluded(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 100, "2026-01-01T00:00:00", "cus_a")
    L.add_payment("p2", 100, "2026-01-02T00:00:00", "cus_a")
    assert [
        r["payment_id"] for r in L.get_payments_by_date("2026-01-01T00:00:00", "2026-01-01T00:00:00")
    ] == ["p1"]
    assert L.get_payments_by_date("2026-01-01T00:00:01", "2026-01-01T23:59:59") == []


@pytest.mark.part3
@pytest.mark.edge
def test_ties_broken_by_payment_id_string_order(impl):
    L = impl.PaymentLedger()
    L.add_payment("zeta", 10, "2026-01-01T00:00:00", "cus_a")
    L.add_payment("alpha", 20, "2026-01-01T00:00:00", "cus_a")
    rows = L.get_payments_by_date("2026-01-01T00:00:00", "2026-01-01T00:00:00")
    assert [r["payment_id"] for r in rows] == ["alpha", "zeta"]


@pytest.mark.part3
def test_export_load_json_round_trip_preserves_state(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    L.add_payment("p2", 500, "2026-01-02T09:00:00", "cus_b")
    L.add_refund("r1", "p1", 300, "2026-01-05T00:00:00")
    blob = L.export_json()
    L2 = impl.PaymentLedger.load_json(blob)
    assert L2.get_total_revenue() == L.get_total_revenue()
    assert L2.get_payments_by_date("2026-01-01T00:00:00", "2026-12-31T00:00:00") == L.get_payments_by_date(
        "2026-01-01T00:00:00", "2026-12-31T00:00:00"
    )


@pytest.mark.part3
@pytest.mark.edge
def test_loaded_ledger_still_enforces_refund_rules(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    L.add_refund("r1", "p1", 1000, "2026-01-05T00:00:00")
    L2 = impl.PaymentLedger.load_json(L.export_json())
    assert L2.add_refund("r1", "p1", 1, "2026-01-06T00:00:00") is False  # replayed refund_id: dup
    with pytest.raises(ValueError):
        L2.add_refund("r2", "p1", 1, "2026-01-06T00:00:00")  # already fully refunded


@pytest.mark.part3
@pytest.mark.edge
def test_get_payments_by_date_invalid_bounds_raise(impl):
    L = impl.PaymentLedger()
    L.add_payment("p1", 1000, "2026-01-01T10:00:00", "cus_a")
    with pytest.raises(ValueError):
        L.get_payments_by_date("2026-13-01T00:00:00", "2026-01-02T00:00:00")
    with pytest.raises(ValueError):
        L.get_payments_by_date("2026-01-01T00:00:00", "garbage")


# ---------------------------------------------------------------- io / fmt / perf
@pytest.mark.part3
@pytest.mark.fmt
def test_run_commands_exact_format(impl):
    assert impl.run_commands(CMD_STREAM) == CMD_STREAM_OUT


@pytest.mark.part3
@pytest.mark.io
def test_stdin_stdout_exact(run_script):
    r = run_script("\n".join(CMD_STREAM) + "\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "\n".join(CMD_STREAM_OUT) + "\n"


@pytest.mark.part3
@pytest.mark.io
def test_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0 and r.stdout == ""


@pytest.mark.part3
@pytest.mark.io
def test_command_stream_error_paths(run_script):
    lines = [
        "PAY p1 1000 2026-01-01T10:00:00 cus_a",
        "PAY p2 500 not-a-timestamp cus_b",
        "REFUND r1 ghost 100 2026-01-05T00:00:00",
        "REFUND r2 p1 5000 2026-01-05T00:00:00",
        "RANGE garbage 2026-01-02T00:00:00",
    ]
    r = run_script("\n".join(lines) + "\n")
    out = r.stdout.splitlines()
    assert out[0] == "PAY p1 OK"
    assert out[1].startswith("PAY p2 ERROR")
    assert out[2].startswith("REFUND r1 ERROR")
    assert out[3].startswith("REFUND r2 ERROR")
    assert out[4].startswith("RANGE ERROR")


@pytest.mark.part3
@pytest.mark.perf
def test_perf_100k_payments_and_range_query(run_script):
    rng = random.Random(0)
    lines = []
    for i in range(100_000):
        day = 1 + rng.randrange(28)
        hh, mm, ss = rng.randrange(24), rng.randrange(60), rng.randrange(60)
        ts = f"2026-01-{day:02d}T{hh:02d}:{mm:02d}:{ss:02d}"
        lines.append(f"PAY p{i} {rng.randrange(1, 100000)} {ts} cus{i % 500}")
    lines.append("REVENUE")
    lines.append("RANGE 2026-01-10T00:00:00 2026-01-12T23:59:59")
    r = run_script("\n".join(lines) + "\n", timeout=30)
    assert r.returncode == 0, r.stderr
    out = r.stdout.splitlines()
    assert out[100_000].startswith("REVENUE ")
    assert out[100_001].startswith("RANGE ")
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
