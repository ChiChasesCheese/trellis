"""ex05 参考答案。"""
from __future__ import annotations

import csv
import io
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from typing import Any

_MISSING = object()


def read_csv_text(text: str) -> list[dict]:
    out: list[dict] = []
    for raw in csv.DictReader(io.StringIO(text)):
        row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in raw.items() if k is not None}
        if not row.get("id"):
            continue
        try:
            row["amount"] = int(row["amount"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(row)
    return out


def write_csv_rows(rows: list[dict], fieldnames: list[str]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def clean_numeric_rows(rows: list[dict], field: str) -> tuple[list[dict], list[dict]]:
    ok: list[dict] = []
    bad: list[dict] = []
    for row in rows:
        try:
            fixed = dict(row)
            fixed[field] = int(fixed[field])
            ok.append(fixed)
        except (KeyError, TypeError, ValueError):
            bad.append(row)
    return ok, bad


def parse_events_jsonl(text: str) -> list[dict]:
    out: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def dig(obj: Any, *path: Any, default: Any = None) -> Any:
    cur = obj
    for p in path:
        if isinstance(cur, dict):
            cur = cur.get(p, _MISSING)
            if cur is _MISSING:
                return default
        elif isinstance(cur, list) and isinstance(p, int) and 0 <= p < len(cur):
            cur = cur[p]
        else:
            return default
        if cur is None:
            return default
    return cur


def field_status(d: dict, key: str) -> str:
    v = d.get(key, _MISSING)
    if v is _MISSING:
        return "missing"
    if v is None:
        return "null"
    return "present"


def sum_amounts_decimal(values: list) -> str:
    total = Decimal("0")
    for v in values:
        total += Decimal(str(v))
    return str(total)


def summarize_list_response(body: dict) -> tuple[int, str | None]:
    if "error" in body:
        return 0, None
    data = body.get("data") or []
    total = sum(item.get("amount", 0) for item in data)
    last_id = data[-1]["id"] if data else None
    return total, last_id


def csv_to_grouped_report(text: str, key_field: str, amount_field: str) -> str:
    totals: dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for raw in csv.DictReader(io.StringIO(text)):
        row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in raw.items() if k is not None}
        key = row.get(key_field)
        if not key:
            continue
        try:
            amount = Decimal(str(row[amount_field]))
        except (KeyError, InvalidOperation):
            continue
        totals[key] += amount
    result = {k: str(v) for k, v in totals.items()}
    return json.dumps(result, sort_keys=True)
