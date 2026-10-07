"""Export alerts for the customer's SIEM: JSON lines or CSV."""
from __future__ import annotations

import csv
import io
import json
from typing import Iterable

from .alerts import Alert
from .config import Config
from .errors import InsiderWatchError
from .scoring import severity_label

CSV_COLUMNS = ["id", "ts", "user", "signal", "score", "severity", "reasons"]


def export_alerts(alerts: Iterable[Alert], fmt: str, config: Config) -> str:
    rows = [{**a.to_dict(), "severity": severity_label(a.score, config)} for a in alerts]
    if fmt == "jsonl":
        return "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "reasons": " | ".join(row["reasons"])})
        return buf.getvalue()
    raise InsiderWatchError(f"unknown export format {fmt!r} (expected jsonl or csv)")
