"""int03 Multi-JSON ETL — YOUR implementation.
Run: pytest loop/rounds/05_integration/int03_multi_json_etl
"""

from __future__ import annotations

import argparse
import csv  # noqa: F401  (Part 3 anomalies.csv 会用到)
import json
import sys
from pathlib import Path  # noqa: F401

MISSING_CREATED_SENTINEL = "9999-99-99"


class EtlError(Exception):
    """Raised for a malformed input file; message must include the file path and (for
    invalid JSON) the line/column of the syntax error."""


# --------------------------------------------------------------------------- Part 1


def load_json_file(path: str):
    """Read and json.loads() one file. Raise EtlError (never a bare json/OSError) with
    the file path and, for parse failures, the line/column of the syntax error."""
    # TODO
    return None


def normalize_email(raw) -> str:
    """'' for anything falsy/non-string; otherwise trimmed + lowercased."""
    # TODO
    return ""


def parse_customers(raw: list[dict]) -> tuple[list[dict], list[dict]]:
    """customers.json's flat records -> (valid Customer dicts, anomaly rows)."""
    # TODO
    return [], []


def parse_legacy(raw: dict) -> tuple[list[dict], list[dict]]:
    """legacy_export.json's {"records": {legacy_id: {"cust": {...}}}} -> (valid Customer
    dicts, anomaly rows). See problem.md's "数据字典" for the field-name mapping."""
    # TODO
    return [], []


def unify_customers(*customer_lists: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    """Merge Customer lists into dict[email, Customer]; duplicate email -> earliest
    `created` wins (missing/empty created sorts last)."""
    # TODO
    return {}, []


def load_all(in_dir: str) -> tuple[dict[str, dict], list[dict], list[dict]]:
    """Read customers.json / legacy_export.json / orders.json from `in_dir`."""
    # TODO
    return {}, [], []


# --------------------------------------------------------------------------- Part 2


def to_legacy(customer: dict) -> dict:
    """Customer -> legacy_export.json's per-record shape."""
    # TODO
    return {}


def from_legacy(record: dict) -> dict:
    """Inverse of to_legacy: from_legacy(to_legacy(c)) == c."""
    # TODO
    return {}


def join_orders(customers: dict[str, dict], orders: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    """Attach each order to its customer by (normalized) customer_email."""
    # TODO
    return {}, []


# --------------------------------------------------------------------------- Part 3


def build_report(joined: dict[str, dict]) -> dict[str, dict]:
    """dict[email, Customer+orders] -> dict[email, {order_count, total_cents,
    most_recent_order}], sorted by email."""
    # TODO
    return {}


def write_outputs(out_dir: str, report: dict[str, dict], anomalies: list[dict]) -> None:
    """report.json + anomalies.csv under out_dir."""
    # TODO
    pass


def run_etl(in_dir: str, out_dir: str) -> dict:
    """Full pipeline: load_all -> join_orders -> build_report -> write_outputs."""
    # TODO
    return {"customers": 0, "orders": 0, "anomalies": 0}


def main_cli(argv: list[str] | None = None) -> int:
    """--in-dir DIR --out-dir DIR"""
    parser = argparse.ArgumentParser(prog="int03-etl")
    parser.add_argument("--in-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args(argv)
    summary = run_etl(args.in_dir, args.out_dir)
    print(f"customers={summary['customers']} orders={summary['orders']} anomalies={summary['anomalies']}")
    return 0


# --------------------------------------------------------------------------- PART n stdin driver


def _read_nonblank(stdin) -> list[str]:
    return [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = _read_nonblank(stdin)
    if not lines or not lines[0].upper().startswith("PART"):
        return
    part = int(lines[0].split()[1])
    args = lines[1:]
    out: list[str] = []

    if part == 1:
        in_dir = args[0]
        customers, _orders_raw, anomalies = load_all(in_dir)
        out.append(f"customers={len(customers)} anomalies={len(anomalies)}")

    elif part == 2:
        in_dir, email = args
        customers, _orders_raw, _anomalies = load_all(in_dir)
        c = customers.get(normalize_email(email))
        if c is None:
            out.append("NOT_FOUND")
        else:
            record = to_legacy(c)
            back = from_legacy(record)
            out.append(json.dumps(record, sort_keys=True))
            out.append("ROUNDTRIP_OK" if back == c else "ROUNDTRIP_FAIL")

    elif part == 3:
        in_dir, out_dir = args
        summary = run_etl(in_dir, out_dir)
        out.append(
            f"customers={summary['customers']} orders={summary['orders']} anomalies={summary['anomalies']}"
        )

    else:
        raise ValueError(f"unknown PART {part!r}")

    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
