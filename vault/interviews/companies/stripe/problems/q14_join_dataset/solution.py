"""q14 Join Dataset — reference solution.

Parse both CSVs with the csv module (quoted commas survive), index the processor rows by the join
value once (O(n + m)), then emit customer x processor pairs and sort with an explicit key.
"""
from __future__ import annotations

import csv
import io
import sys
from collections import defaultdict

Row = list[str]


def parse_csv(text: str) -> tuple[list[str], list[Row]]:
    """(header, rows). Header names and cells are stripped; blank lines skipped;
    short rows padded with '' and long rows truncated to the header length."""
    reader = csv.reader(io.StringIO(text))
    header: list[str] = []
    rows: list[Row] = []
    for rec in reader:
        rec = [c.strip() for c in rec]
        if not any(rec):          # blank line -> [] or ['']
            continue
        if not header:
            header = rec
            continue
        rec = (rec + [""] * len(header))[: len(header)]
        rows.append(rec)
    return header, rows


def order_key(header: list[str], row: Row, position: int) -> tuple[int, int]:
    """Numeric `order` column, falling back to input position when absent / non-integer.
    Returned as (order, position) so ties on `order` are broken by input position."""
    if "order" in header:
        try:
            return int(row[header.index("order")]), position
        except ValueError:
            pass
    return position, position


def join_dataset(field_name: str, customer_csv: str, processor_csv: str,
                 skip_unmatched: bool = True, drop_duplicate_key: bool = False) -> str:
    c_hdr, c_rows = parse_csv(customer_csv)
    p_hdr, p_rows = parse_csv(processor_csv)
    if field_name not in c_hdr or field_name not in p_hdr:
        raise ValueError(f"missing join column '{field_name}'")
    c_key, p_key = c_hdr.index(field_name), p_hdr.index(field_name)

    # processor index: join value -> [(sort key, row)] already sorted by processor order
    by_key: dict[str, list[tuple[tuple[int, int], Row]]] = defaultdict(list)
    for j, prow in enumerate(p_rows):
        by_key[prow[p_key]].append((order_key(p_hdr, prow, j), prow))
    for matches in by_key.values():
        matches.sort(key=lambda m: m[0])

    empty_proc = [""] * len(p_hdr)
    out: list[tuple[tuple[int, int, int, int], Row]] = []
    for i, crow in enumerate(c_rows):
        ck = order_key(c_hdr, crow, i)
        matches = by_key.get(crow[c_key], [])
        if not matches:
            if not skip_unmatched:                       # Part 2: left join keeps the row
                out.append((ck + (-1, -1), crow + empty_proc))
            continue
        for pk, prow in matches:                          # Part 3: one row per match
            out.append((ck + pk, crow + prow))
    # full sort key: (customer order, customer position, processor order, processor position)
    out.sort(key=lambda item: item[0])

    keep = list(range(len(c_hdr) + len(p_hdr)))
    if drop_duplicate_key:                                # variant: single copy of the key
        keep.remove(len(c_hdr) + p_key)
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow([(c_hdr + p_hdr)[k] for k in keep])
    for _, row in out:
        writer.writerow([row[k] for k in keep])
    return buf.getvalue()


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = stdin.read().splitlines()
    if not lines:
        return
    _, field_name, flag = lines[0].split()
    sep = lines.index("---")
    customer_csv = "\n".join(lines[1:sep])
    processor_csv = "\n".join(lines[sep + 1:])
    try:
        stdout.write(join_dataset(field_name, customer_csv, processor_csv, flag.lower() == "true"))
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
