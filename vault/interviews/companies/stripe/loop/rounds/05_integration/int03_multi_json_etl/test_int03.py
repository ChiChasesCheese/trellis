"""int03 Multi-JSON ETL — tests. Uses the `impl` fixture (repo-root conftest.py, loads
solution.py or starter.py under IMPL=starter) and `run_script` for io tests. Fixture data
is small, hand-built JSON written to tmp_path per CONVENTIONS.md (the larger data/*.json
files are random.Random(0)-generated and only used by the CLI end-to-end / perf checks)."""

from __future__ import annotations

import csv
import json
import random
import time
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


def _write_dir(tmp_path, customers=None, legacy=None, orders=None) -> str:
    d = tmp_path / "in"
    d.mkdir(exist_ok=True)
    (d / "customers.json").write_text(json.dumps(customers if customers is not None else []))
    (d / "legacy_export.json").write_text(json.dumps(legacy if legacy is not None else {"records": {}}))
    (d / "orders.json").write_text(json.dumps(orders if orders is not None else []))
    return str(d)


WORKED_CUSTOMERS = [
    {"id": 1, "email": "Alice@Example.com ", "name": "Alice A", "created": "2024-03-01"},
    {"id": 2, "email": "bob@example.com", "created": "2024-01-15"},
    {"id": 3, "email": "alice@example.com", "name": "Alice Dup", "created": "2023-11-20"},
    {"id": 4, "name": "No Email"},
]
WORKED_LEGACY = {
    "records": {
        "L001": {"cust": {"mail": "carol@example.com", "full_name": "Carol C", "signup_date": "2022-05-05"}},
        "L002": {"cust": {"mail": "bob@example.com", "full_name": "Bob Legacy"}},
        "L003": {"cust": {}},
    }
}
WORKED_ORDERS = [
    {
        "order_id": "O1",
        "customer_email": "alice@example.com",
        "items": [{"sku": "A", "qty": 2, "unit_cents": 500}],
        "status": "paid",
        "placed_at": "2024-05-01T10:00:00",
    },
    {
        "order_id": "O2",
        "customer_email": "ALICE@example.com",
        "items": [{"sku": "B", "qty": 1, "unit_cents": 1200}],
        "status": "paid",
        "placed_at": "2024-06-01T10:00:00",
    },
    {
        "order_id": "O3",
        "customer_email": "ghost@example.com",
        "items": [],
        "status": "paid",
        "placed_at": "2024-01-01T00:00:00",
    },
    {
        "order_id": "O4",
        "customer_email": "",
        "items": [],
        "status": "paid",
        "placed_at": "2024-01-01T00:00:00",
    },
    {
        "order_id": "O1",
        "customer_email": "alice@example.com",
        "items": [{"sku": "A", "qty": 2, "unit_cents": 500}],
        "status": "paid",
        "placed_at": "2024-05-01T10:00:00",
    },
]


def _worked_dir(tmp_path) -> str:
    return _write_dir(tmp_path, WORKED_CUSTOMERS, WORKED_LEGACY, WORKED_ORDERS)


# --------------------------------------------------------------------------- Part 1


@pytest.mark.part1
def test_worked_example_load_all(impl, tmp_path):
    in_dir = _worked_dir(tmp_path)
    unified, orders_raw, anomalies = impl.load_all(in_dir)

    assert set(unified) == {"alice@example.com", "bob@example.com", "carol@example.com"}
    assert unified["alice@example.com"] == {
        "id": "3",
        "email": "alice@example.com",
        "name": "Alice Dup",
        "created": "2023-11-20",
    }
    assert unified["bob@example.com"]["id"] == "2"
    assert unified["carol@example.com"] == {
        "id": "L001",
        "email": "carol@example.com",
        "name": "Carol C",
        "created": "2022-05-05",
    }
    assert len(orders_raw) == 5

    types = sorted((a["type"], a["ref"]) for a in anomalies)
    assert types == [
        ("duplicate_customer", "alice@example.com"),
        ("duplicate_customer", "bob@example.com"),
        ("missing_email", "4"),
        ("missing_email", "L003"),
    ]


@pytest.mark.part1
def test_normalize_email(impl):
    assert impl.normalize_email(" Foo@Bar.COM ") == "foo@bar.com"
    assert impl.normalize_email("") == ""
    assert impl.normalize_email(None) == ""
    assert impl.normalize_email(123) == ""


@pytest.mark.part1
@pytest.mark.edge
def test_parse_customers_missing_and_blank_email(impl):
    raw = [
        {"id": 1, "email": "a@x.com", "name": "A", "created": "2024-01-01"},
        {"id": 2, "name": "No Email Key"},
        {"id": 3, "email": "", "name": "Blank"},
        {"id": 4, "email": "   ", "name": "Whitespace Only"},
    ]
    customers, anomalies = impl.parse_customers(raw)
    assert [c["id"] for c in customers] == ["1"]
    assert {a["ref"] for a in anomalies} == {"2", "3", "4"}
    assert all(a["type"] == "missing_email" and a["source"] == "customers" for a in anomalies)


@pytest.mark.part1
@pytest.mark.edge
def test_parse_customers_missing_name_and_created_default_empty(impl):
    raw = [{"id": 1, "email": "a@x.com"}]
    customers, anomalies = impl.parse_customers(raw)
    assert anomalies == []
    assert customers == [{"id": "1", "email": "a@x.com", "name": "", "created": ""}]


@pytest.mark.part1
@pytest.mark.edge
def test_parse_legacy_missing_and_blank_mail(impl):
    # Mirrors test_parse_customers_missing_and_blank_email: parse_legacy must be usable
    # (and independently testable) without any Part 2 function implemented.
    raw = {
        "records": {
            "L1": {"cust": {"mail": "a@x.com", "full_name": "A", "signup_date": "2024-01-01"}},
            "L2": {"cust": {"full_name": "No Mail Key"}},
            "L3": {"cust": {"mail": "", "full_name": "Blank"}},
            "L4": {"cust": {"mail": "   ", "full_name": "Whitespace Only"}},
        }
    }
    customers, anomalies = impl.parse_legacy(raw)
    assert [c["id"] for c in customers] == ["L1"]
    assert {a["ref"] for a in anomalies} == {"L2", "L3", "L4"}
    assert all(a["type"] == "missing_email" and a["source"] == "legacy" for a in anomalies)


@pytest.mark.part1
@pytest.mark.edge
def test_parse_legacy_field_mapping_and_missing_defaults(impl):
    # mail->email, full_name->name, signup_date->created; name/created default to "" when
    # the legacy record's cust dict omits them (not KeyError, not None).
    raw = {"records": {"L9": {"cust": {"mail": "A@X.com "}}}}
    customers, anomalies = impl.parse_legacy(raw)
    assert anomalies == []
    assert customers == [{"id": "L9", "email": "a@x.com", "name": "", "created": ""}]


@pytest.mark.part1
@pytest.mark.edge
def test_unify_missing_created_never_beats_a_dated_record(impl):
    # order matters for the assertion, not for correctness: the dated record must win
    # regardless of which list it's passed in first.
    dated = [{"id": "1", "email": "x@x.com", "name": "Dated", "created": "2020-01-01"}]
    undated = [{"id": "2", "email": "x@x.com", "name": "Undated", "created": ""}]

    unified, anomalies = impl.unify_customers(undated, dated)
    assert unified["x@x.com"]["id"] == "1"

    unified2, anomalies2 = impl.unify_customers(dated, undated)
    assert unified2["x@x.com"]["id"] == "1"


@pytest.mark.part1
@pytest.mark.edge
def test_unify_exact_tie_keeps_first_seen(impl):
    a = [{"id": "1", "email": "x@x.com", "name": "First", "created": "2020-01-01"}]
    b = [{"id": "2", "email": "x@x.com", "name": "Second", "created": "2020-01-01"}]
    unified, _ = impl.unify_customers(a, b)
    assert unified["x@x.com"]["id"] == "1"


@pytest.mark.part1
@pytest.mark.edge
def test_load_json_file_empty_file_raises_etlerror_with_position(impl, tmp_path):
    p = tmp_path / "empty.json"
    p.write_text("")
    with pytest.raises(impl.EtlError) as exc_info:
        impl.load_json_file(str(p))
    msg = str(exc_info.value)
    assert str(p) in msg
    assert "line 1" in msg and "column 1" in msg


@pytest.mark.part1
@pytest.mark.edge
def test_load_json_file_malformed_raises_etlerror(impl, tmp_path):
    p = tmp_path / "bad.json"
    p.write_text('{"a": 1,}')  # trailing comma
    with pytest.raises(impl.EtlError) as exc_info:
        impl.load_json_file(str(p))
    assert str(p) in str(exc_info.value)


@pytest.mark.part1
@pytest.mark.edge
def test_load_all_missing_file_raises_etlerror(impl, tmp_path):
    d = tmp_path / "in"
    d.mkdir()
    with pytest.raises(impl.EtlError):
        impl.load_all(str(d))


@pytest.mark.part1
@pytest.mark.edge
def test_load_all_customers_not_a_list_raises_etlerror(impl, tmp_path):
    d = tmp_path / "in"
    d.mkdir()
    (d / "customers.json").write_text(json.dumps({"oops": "not a list"}))
    (d / "legacy_export.json").write_text(json.dumps({"records": {}}))
    (d / "orders.json").write_text(json.dumps([]))
    with pytest.raises(impl.EtlError):
        impl.load_all(str(d))


# --------------------------------------------------------------------------- Part 2


@pytest.mark.part2
def test_to_legacy_from_legacy_roundtrip_worked_example(impl, tmp_path):
    in_dir = _worked_dir(tmp_path)
    unified, _orders_raw, _anomalies = impl.load_all(in_dir)
    c = unified["carol@example.com"]

    record = impl.to_legacy(c)
    assert record == {
        "legacy_id": "L001",
        "cust": {"mail": "carol@example.com", "full_name": "Carol C", "signup_date": "2022-05-05"},
    }
    assert impl.from_legacy(record) == c


@pytest.mark.part2
@pytest.mark.edge
def test_roundtrip_holds_for_every_generated_customer(impl):
    rng = random.Random(0)
    for i in range(50):
        c = {
            "id": str(i),
            "email": f"user{i}@example.com",
            "name": rng.choice(["Alice", "Bob", ""]),
            "created": rng.choice(["2020-01-01", "2021-06-15", ""]),
        }
        assert impl.from_legacy(impl.to_legacy(c)) == c


@pytest.mark.part2
def test_join_orders_worked_example(impl, tmp_path):
    in_dir = _worked_dir(tmp_path)
    unified, orders_raw, _anomalies = impl.load_all(in_dir)
    joined, anomalies = impl.join_orders(unified, orders_raw)

    assert len(joined["alice@example.com"]["orders"]) == 3  # O1, O2, dup O1
    assert joined["bob@example.com"]["orders"] == []

    by_type = sorted((a["type"], a["ref"]) for a in anomalies)
    assert by_type == [
        ("duplicate_order", "O1"),
        ("missing_email", "O4"),
        ("orphan_order", "O3"),
    ]


@pytest.mark.part2
@pytest.mark.edge
def test_join_orders_case_insensitive_email_matches(impl, tmp_path):
    in_dir = _write_dir(
        tmp_path,
        customers=[{"id": 1, "email": "a@x.com", "name": "A", "created": "2024-01-01"}],
        orders=[
            {
                "order_id": "O1",
                "customer_email": "A@X.com",
                "items": [{"sku": "s", "qty": 1, "unit_cents": 100}],
                "status": "paid",
                "placed_at": "2024-01-01T00:00:00",
            }
        ],
    )
    unified, orders_raw, _ = impl.load_all(in_dir)
    joined, anomalies = impl.join_orders(unified, orders_raw)
    assert len(joined["a@x.com"]["orders"]) == 1
    assert anomalies == []


@pytest.mark.part2
@pytest.mark.edge
def test_join_orders_empty_items_is_zero_not_anomaly(impl, tmp_path):
    in_dir = _write_dir(
        tmp_path,
        customers=[{"id": 1, "email": "a@x.com", "name": "A", "created": "2024-01-01"}],
        orders=[
            {
                "order_id": "O1",
                "customer_email": "a@x.com",
                "items": [],
                "status": "paid",
                "placed_at": "2024-01-01T00:00:00",
            }
        ],
    )
    unified, orders_raw, _ = impl.load_all(in_dir)
    joined, anomalies = impl.join_orders(unified, orders_raw)
    assert joined["a@x.com"]["orders"][0]["total_cents"] == 0
    assert anomalies == []


# --------------------------------------------------------------------------- Part 3


@pytest.mark.part3
def test_build_report_worked_example(impl, tmp_path):
    in_dir = _worked_dir(tmp_path)
    unified, orders_raw, _ = impl.load_all(in_dir)
    joined, _ = impl.join_orders(unified, orders_raw)
    report = impl.build_report(joined)

    assert report["alice@example.com"] == {"order_count": 3, "total_cents": 3200, "most_recent_order": "O2"}
    assert report["bob@example.com"] == {"order_count": 0, "total_cents": 0, "most_recent_order": None}
    assert list(report) == sorted(report)  # sorted by email


@pytest.mark.part3
@pytest.mark.fmt
def test_run_etl_writes_report_and_anomalies(impl, tmp_path):
    in_dir = _worked_dir(tmp_path)
    out_dir = tmp_path / "out"
    summary = impl.run_etl(in_dir, str(out_dir))

    assert summary == {"customers": 3, "orders": 5, "anomalies": 7}  # 4 (part1) + 3 (join)

    report = json.loads((out_dir / "report.json").read_text())
    assert report["alice@example.com"]["order_count"] == 3

    with open(out_dir / "anomalies.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 7
    assert set(rows[0]) == {"type", "source", "ref", "detail"}


@pytest.mark.part3
@pytest.mark.edge
def test_run_etl_creates_nested_out_dir(impl, tmp_path):
    in_dir = _worked_dir(tmp_path)
    out_dir = tmp_path / "a" / "b" / "c"
    impl.run_etl(in_dir, str(out_dir))
    assert (out_dir / "report.json").exists()
    assert (out_dir / "anomalies.csv").exists()


@pytest.mark.part3
def test_main_cli_prints_summary(impl, tmp_path, capsys):
    in_dir = _worked_dir(tmp_path)
    out_dir = tmp_path / "out"
    rc = impl.main_cli(["--in-dir", in_dir, "--out-dir", str(out_dir)])
    assert rc == 0
    captured = capsys.readouterr()
    assert "customers=3" in captured.out
    assert "orders=5" in captured.out


@pytest.mark.part3
def test_against_generated_data_dir_is_internally_consistent(impl):
    """Sanity check against the larger random.Random(0)-generated data/ fixtures: no
    exception, and every report entry's order_count matches the number of joined orders."""
    unified, orders_raw, anomalies = impl.load_all(str(DATA_DIR))
    joined, join_anomalies = impl.join_orders(unified, orders_raw)
    report = impl.build_report(joined)
    assert len(unified) > 200
    assert len(orders_raw) > 200
    for email, row in report.items():
        assert row["order_count"] == len(joined[email]["orders"])
        assert row["total_cents"] == sum(o["total_cents"] for o in joined[email]["orders"])


# --------------------------------------------------------------------------- io


@pytest.mark.part1
@pytest.mark.io
def test_io_part1(run_script, tmp_path):
    in_dir = _worked_dir(tmp_path)
    r = run_script(f"PART 1\n{in_dir}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "customers=3 anomalies=4"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.fmt
def test_io_part2_roundtrip(run_script, tmp_path):
    in_dir = _worked_dir(tmp_path)
    r = run_script(f"PART 2\n{in_dir}\ncarol@example.com\n")
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert json.loads(lines[0]) == {
        "cust": {"full_name": "Carol C", "mail": "carol@example.com", "signup_date": "2022-05-05"},
        "legacy_id": "L001",
    }
    assert lines[1] == "ROUNDTRIP_OK"


@pytest.mark.part2
@pytest.mark.io
@pytest.mark.edge
def test_io_part2_not_found(run_script, tmp_path):
    in_dir = _worked_dir(tmp_path)
    r = run_script(f"PART 2\n{in_dir}\nnobody@example.com\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "NOT_FOUND"


@pytest.mark.part3
@pytest.mark.io
def test_io_part3(run_script, tmp_path):
    in_dir = _worked_dir(tmp_path)
    out_dir = tmp_path / "out"
    r = run_script(f"PART 3\n{in_dir}\n{out_dir}\n")
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "customers=3 orders=5 anomalies=7"
    assert (out_dir / "report.json").exists()


@pytest.mark.part1
@pytest.mark.io
def test_io_empty_stdin(run_script):
    r = run_script("")
    assert r.returncode == 0
    assert r.stdout == ""


# --------------------------------------------------------------------------- perf


@pytest.mark.part3
@pytest.mark.perf
def test_perf_join_and_report_100k_orders(impl):
    rng = random.Random(0)
    n_customers = 2_000
    customers = {
        f"user{i}@example.com": {
            "id": str(i),
            "email": f"user{i}@example.com",
            "name": f"User {i}",
            "created": "2024-01-01",
        }
        for i in range(n_customers)
    }
    orders = []
    for i in range(100_000):
        cid = rng.randrange(n_customers)
        orders.append(
            {
                "order_id": f"O{i}",
                "customer_email": f"user{cid}@example.com",
                "items": [{"sku": "s", "qty": 1, "unit_cents": 100}],
                "status": "paid",
                "placed_at": f"2024-01-01T00:00:{i % 60:02d}",
            }
        )

    t0 = time.perf_counter()
    joined, _anomalies = impl.join_orders(customers, orders)
    report = impl.build_report(joined)
    elapsed = time.perf_counter() - t0

    assert len(report) == n_customers
    assert elapsed < 2.0, f"too slow: {elapsed:.2f}s"
