"""Converting between "a list of record dicts" (what `parser.parse_text()` returns for a
document whose top level is a YAML list of mappings) and CSV text, in both directions.

This module knows nothing about YAML syntax or indentation -- by the time anything here runs,
`parser.py` has already turned the document into plain Python dicts/lists. All this module does
is decide which columns a set of records needs and how a cell's text maps back to a scalar value.
"""

from __future__ import annotations

import csv
import io

from .scalars import coerce_scalar, scalar_to_text


def collect_fieldnames(records: list[dict]) -> list[str]:
    """The CSV header: every key that appears in any record, in first-seen order (record 0's
    keys first, then any keys record 1 introduces that record 0 didn't have, and so on)."""
    seen: dict[str, None] = {}
    for record in records:
        for key in record:
            seen.setdefault(key, None)
    return list(seen)


def to_csv_text(records: list[dict]) -> str:
    """Render a list of record dicts as CSV text (header row + one row per record). A record
    missing a column that some other record has gets an empty cell there, not an error."""
    fieldnames = collect_fieldnames(records)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, restval="", extrasaction="raise")
    writer.writeheader()
    for record in records:
        writer.writerow({key: scalar_to_text(record.get(key)) for key in fieldnames})
    return buf.getvalue()


def from_csv_text(text: str) -> list[dict]:
    """The inverse of to_csv_text: parse CSV text back into a list of record dicts, coercing
    each cell's text back to a scalar (int/float/bool/string) the same way the YAML parser would.
    """
    reader = csv.DictReader(io.StringIO(text))
    return [{key: coerce_scalar(value) for key, value in row.items()} for row in reader]
