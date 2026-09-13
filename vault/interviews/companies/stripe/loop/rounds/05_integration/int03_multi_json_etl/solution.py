"""int03 Multi-JSON ETL — reference solution.

Read three JSON files with inconsistent shapes (a "current" customers export, an "old
system" legacy export with different field names, and an orders export), unify them into
one `dict[email, Customer]`, cross-join orders, and emit a report + an anomalies CSV.

Public API (same shape as starter.py / starter_template.py):
    load_json_file(path) -> Any                                    Part 1 (raises EtlError)
    normalize_email(raw) -> str                                     Part 1
    parse_customers(raw) -> (list[Customer], list[anomaly])         Part 1
    parse_legacy(raw) -> (list[Customer], list[anomaly])            Part 1
    unify_customers(*customer_lists) -> (dict[email,Customer], list[anomaly])  Part 1
    load_all(in_dir) -> (dict[email,Customer], list[order], list[anomaly])     Part 1
    to_legacy(customer) -> dict                                     Part 2
    from_legacy(record) -> Customer                                 Part 2
    join_orders(customers, orders) -> (dict[email,Customer+orders], list[anomaly])  Part 2
    build_report(joined) -> dict[email, {order_count,total_cents,most_recent_order}] Part 3
    write_outputs(out_dir, report, anomalies) -> None               Part 3
    run_etl(in_dir, out_dir) -> summary dict                        Part 3
    main_cli(argv) -> int                                           Part 3 (--in-dir/--out-dir)
    main(stdin=sys.stdin, stdout=sys.stdout) -> None                PART n driver for io tests

Only stdlib: json, csv, argparse, pathlib.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

MISSING_CREATED_SENTINEL = "9999-99-99"  # sorts after any real ISO date -> "missing loses ties"


class EtlError(Exception):
    """Raised for a malformed input file. Message always includes the file path and, for
    invalid JSON, the line/column reported by json.JSONDecodeError."""


def _anomaly(kind: str, source: str, ref: str, detail: str) -> dict:
    """Build one anomaly row: the four columns anomalies.csv writes, in that order."""
    return {"type": kind, "source": source, "ref": ref, "detail": detail}


# --------------------------------------------------------------------------- Part 1


def load_json_file(path: str):
    """Read and json.loads() one file. Raises EtlError (never a bare json/OSError) with
    the file path and, for parse failures, the line/column of the syntax error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError as e:
        raise EtlError(f"{path}: file not found") from e
    except OSError as e:
        raise EtlError(f"{path}: {e}") from e
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise EtlError(f"{path}: invalid JSON at line {e.lineno} column {e.colno}: {e.msg}") from e


def normalize_email(raw) -> str:
    """'' for anything falsy/non-string; otherwise trimmed + lowercased."""
    if not raw or not isinstance(raw, str):
        return ""
    return raw.strip().lower()


def parse_customers(raw: list[dict]) -> tuple[list[dict], list[dict]]:
    """customers.json's flat records -> (valid Customer dicts, anomaly rows).
    A record with no usable email is dropped and logged, never silently kept with ''."""
    customers: list[dict] = []
    anomalies: list[dict] = []
    for rec in raw:
        email = normalize_email(rec.get("email"))
        if not email:
            anomalies.append(
                _anomaly("missing_email", "customers", str(rec["id"]), "customer record has no usable email")
            )
            continue
        customers.append(
            {
                "id": str(rec["id"]),
                "email": email,
                "name": rec.get("name", ""),
                "created": rec.get("created", ""),
            }
        )
    return customers, anomalies


def _legacy_cust_to_customer(legacy_id: str, cust: dict) -> dict:
    """Map one legacy_export.json {mail,full_name,signup_date} dict to a Customer (does
    not validate the email). Shared by parse_legacy (Part 1) and from_legacy (Part 2) so
    the field-name mapping lives in exactly one place."""
    return {
        "id": legacy_id,
        "email": normalize_email(cust.get("mail")),
        "name": cust.get("full_name", ""),
        "created": cust.get("signup_date", ""),
    }


def parse_legacy(raw: dict) -> tuple[list[dict], list[dict]]:
    """legacy_export.json's {"records": {legacy_id: {"cust": {...}}}} -> (valid Customer
    dicts, anomaly rows). Field names differ from customers.json -- see problem.md's
    "数据字典": mail->email, full_name->name, signup_date->created."""
    customers: list[dict] = []
    anomalies: list[dict] = []
    records = raw.get("records", {}) if isinstance(raw, dict) else {}
    for legacy_id, rec in records.items():
        cust = rec.get("cust", {}) if isinstance(rec, dict) else {}
        customer = _legacy_cust_to_customer(legacy_id, cust)
        if not customer["email"]:
            anomalies.append(
                _anomaly("missing_email", "legacy", legacy_id, "legacy record has no usable mail")
            )
            continue
        customers.append(customer)
    return customers, anomalies


def unify_customers(*customer_lists: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    """Merge any number of Customer lists into dict[email, Customer]. Duplicate email ->
    the record with the earliest `created` wins (a missing/empty `created` sorts last, so
    it never beats a dated record); first-seen wins on an exact tie. Every dropped
    duplicate is logged as a 'duplicate_customer' anomaly."""
    best: dict[str, dict] = {}
    anomalies: list[dict] = []
    for lst in customer_lists:
        for c in lst:
            email = c["email"]
            existing = best.get(email)
            if existing is None:
                best[email] = c
                continue
            existing_key = existing.get("created") or MISSING_CREATED_SENTINEL
            new_key = c.get("created") or MISSING_CREATED_SENTINEL
            winner, loser = (c, existing) if new_key < existing_key else (existing, c)
            anomalies.append(
                _anomaly(
                    "duplicate_customer",
                    "unify",
                    email,
                    f"dropped id={loser['id']!r} created={loser.get('created','')!r}, kept id={winner['id']!r}",
                )
            )
            best[email] = winner
    return best, anomalies


def load_all(in_dir: str) -> tuple[dict[str, dict], list[dict], list[dict]]:
    """Read customers.json / legacy_export.json / orders.json from `in_dir`. Returns
    (unified customers dict[email,Customer], raw orders list, anomalies so far)."""
    base = Path(in_dir)
    customers_raw = load_json_file(str(base / "customers.json"))
    legacy_raw = load_json_file(str(base / "legacy_export.json"))
    orders_raw = load_json_file(str(base / "orders.json"))

    if not isinstance(customers_raw, list):
        raise EtlError(f"{base / 'customers.json'}: expected a JSON list of customer records")
    if not isinstance(legacy_raw, dict):
        raise EtlError(f"{base / 'legacy_export.json'}: expected a JSON object with a 'records' key")
    if not isinstance(orders_raw, list):
        raise EtlError(f"{base / 'orders.json'}: expected a JSON list of order records")

    cust_valid, cust_anom = parse_customers(customers_raw)
    legacy_valid, legacy_anom = parse_legacy(legacy_raw)
    unified, dup_anom = unify_customers(cust_valid, legacy_valid)
    return unified, orders_raw, cust_anom + legacy_anom + dup_anom


# --------------------------------------------------------------------------- Part 2


def to_legacy(customer: dict) -> dict:
    """Customer -> legacy_export.json's per-record shape ({"legacy_id","cust":{mail,
    full_name,signup_date}}). Pure format conversion, no I/O."""
    return {
        "legacy_id": customer["id"],
        "cust": {
            "mail": customer["email"],
            "full_name": customer.get("name", ""),
            "signup_date": customer.get("created", ""),
        },
    }


def from_legacy(record: dict) -> dict:
    """Inverse of to_legacy: legacy_export.json's per-record shape -> Customer.
    from_legacy(to_legacy(c)) == c for any Customer c whose email is already
    normalize_email()'d (true for every Customer this module produces). Reuses Part 1's
    `_legacy_cust_to_customer` so parsing and round-tripping share one field mapping."""
    return _legacy_cust_to_customer(record["legacy_id"], record.get("cust", {}))


def _order_total_cents(order: dict) -> int:
    """Σ qty × unit_cents over one order's items, in integer cents (no float, no
    rounding -- both operands are already integers)."""
    return sum(int(item.get("qty", 0)) * int(item.get("unit_cents", 0)) for item in order.get("items", []))


def _duplicate_order_anomalies(seen_ids: dict[str, int]) -> list[dict]:
    """One 'duplicate_order' anomaly per order_id seen more than once (not one per
    repeat -- problem.md: report the duplication, don't dedupe amounts)."""
    return [
        _anomaly("duplicate_order", "orders", order_id, f"order_id appears {count} times")
        for order_id, count in seen_ids.items()
        if order_id and count > 1
    ]


def join_orders(customers: dict[str, dict], orders: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    """Attach each order to its customer by (normalized) customer_email. Returns a NEW
    dict[email, Customer] where every value has an added "orders" list (each order
    reduced to order_id/status/placed_at/total_cents, amounts in integer cents), plus
    anomaly rows for orders with no usable email, orders whose email matches no known
    customer ("orphan"), and order_ids that repeat."""
    joined = {email: dict(c, orders=[]) for email, c in customers.items()}
    anomalies: list[dict] = []
    seen_ids: dict[str, int] = {}

    for order in orders:
        order_id = order.get("order_id", "")
        seen_ids[order_id] = seen_ids.get(order_id, 0) + 1
        email = normalize_email(order.get("customer_email"))
        if not email:
            anomalies.append(_anomaly("missing_email", "orders", order_id, "order has no customer_email"))
            continue
        if email not in joined:
            anomalies.append(_anomaly("orphan_order", "orders", order_id, f"no customer for email {email!r}"))
            continue
        joined[email]["orders"].append(
            {
                "order_id": order_id,
                "status": order.get("status", ""),
                "placed_at": order.get("placed_at", ""),
                "total_cents": _order_total_cents(order),
            }
        )

    anomalies.extend(_duplicate_order_anomalies(seen_ids))
    return joined, anomalies


# --------------------------------------------------------------------------- Part 3


def build_report(joined: dict[str, dict]) -> dict[str, dict]:
    """dict[email, Customer+orders] -> dict[email, {order_count, total_cents,
    most_recent_order}], sorted by email. most_recent_order is the order_id with the
    lexicographically-largest placed_at (works because placed_at is ISO-8601), or None
    for a customer with zero joined orders."""
    report: dict[str, dict] = {}
    for email in sorted(joined):
        orders = joined[email].get("orders", [])
        total_cents = sum(o["total_cents"] for o in orders)
        most_recent = max(orders, key=lambda o: o["placed_at"])["order_id"] if orders else None
        report[email] = {
            "order_count": len(orders),
            "total_cents": total_cents,
            "most_recent_order": most_recent,
        }
    return report


def write_outputs(out_dir: str, report: dict[str, dict], anomalies: list[dict]) -> None:
    """report.json (sorted by email, pretty-printed) + anomalies.csv (header:
    type,source,ref,detail) under out_dir, creating out_dir if needed."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    with open(out_path / "anomalies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "source", "ref", "detail"])
        for a in anomalies:
            writer.writerow([a["type"], a["source"], a["ref"], a["detail"]])


def run_etl(in_dir: str, out_dir: str) -> dict:
    """Full pipeline: load_all -> join_orders -> build_report -> write_outputs. Returns a
    small summary dict (customers/orders/anomalies counts) for CLI/PART-driver output."""
    customers, orders_raw, anomalies = load_all(in_dir)
    joined, join_anom = join_orders(customers, orders_raw)
    anomalies = anomalies + join_anom
    report = build_report(joined)
    write_outputs(out_dir, report, anomalies)
    return {"customers": len(customers), "orders": len(orders_raw), "anomalies": len(anomalies)}


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
    """Dispatches on a leading 'PART n' line, remaining non-blank lines are that part's
    positional arguments (see problem.md's "main() / PART n 驱动")."""
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
