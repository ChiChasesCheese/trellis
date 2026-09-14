"""q25 Invoice / Payment Reconciliation — YOUR implementation. Run: python drill.py test q25"""
from __future__ import annotations

import sys


def part1(invoices: list[str], payments: list[str]) -> list[str]:
    """invoices: 'id,due YYYY-MM-DD,amount_cents'; payments: 'id,amount_cents,memo'.
    Exact memo 'Paying off: <id>' + exact amount -> PAID. Return ['id: PAID|UNPAID', ...]
    in invoice input order."""
    # TODO
    return []


def part2(invoices: list[str], payments: list[str]) -> list[str]:
    """Memo mentions restrict candidates (else all); exact amount to earliest-due unpaid."""
    # TODO
    return []


def part3(invoices: list[str], payments: list[str]) -> list[str]:
    """Pour a payment over candidates oldest-first; PARTIAL (remaining r); 'pid: UNAPPLIED x'."""
    # TODO
    return []


def part4(invoices: list[str], payments: list[str]) -> list[str]:
    """Part 3 plus leading audit lines 'pid -> iid amount' in application order."""
    # TODO
    return []


PARTS = {1: part1, 2: part2, 3: part3, 4: part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1]) if lines[0].upper().startswith("PART") else 1
    invoices, payments, section = [], [], []
    for ln in lines[1:] if lines[0].upper().startswith("PART") else lines:
        if ln.upper() == "INVOICES":
            section = invoices
        elif ln.upper() == "PAYMENTS":
            section = payments
        else:
            section.append(ln)
    out = PARTS[part](invoices, payments)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
