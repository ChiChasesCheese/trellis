"""q14 Join Dataset — YOUR implementation. Run: python drill.py test q14"""
from __future__ import annotations

import sys


def join_dataset(field_name: str, customer_csv: str, processor_csv: str,
                 skip_unmatched: bool = True, drop_duplicate_key: bool = False) -> str:
    """Join two CSV texts on `field_name`.
    Part 1: inner join (skip_unmatched=True), columns = customer cols + processor cols,
            sorted by customer `order`, then customer position, then processor `order`, then position.
    Part 2: skip_unmatched=False keeps unmatched customer rows with empty processor cells.
    Part 3: one customer row matching many processor rows -> one output row per match.
    Raise ValueError("missing join column '<field_name>'") if either file lacks the column."""
    # TODO
    return ""


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    text = stdin.read()
    lines = text.splitlines()
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
