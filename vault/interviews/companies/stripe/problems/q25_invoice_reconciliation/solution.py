"""q25 Invoice / Payment Reconciliation — reference solution.

All money is integer cents. One engine `reconcile(invoices, payments, part)` implements the
four progressively relaxed rule sets; the parts only differ in (a) how candidates are chosen
from the memo and (b) whether the amount must match exactly or is poured across invoices.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict, deque

TOKEN = re.compile(r"[A-Za-z0-9_\-]+")            # Part 2+: memo tokens that may name an invoice
EXACT_MEMO = re.compile(r"Paying off:\s*(\S+)")    # Part 1: the whole memo must be this


def parse_invoices(lines: list[str]) -> list[tuple[str, str, int]]:
    out = []
    for raw in lines:
        if raw.strip():
            iid, due, amt = (p.strip() for p in raw.split(","))
            out.append((iid, due, int(amt)))
    return out


def parse_payments(lines: list[str]) -> list[tuple[str, int, str]]:
    out = []
    for raw in lines:
        if raw.strip():
            parts = raw.split(",", 2)                 # memo may itself contain commas
            memo = parts[2].strip() if len(parts) > 2 else ""
            out.append((parts[0].strip(), int(parts[1].strip()), memo))
    return out


def reconcile(invoices: list[str], payments: list[str], part: int) -> list[str]:
    inv = parse_invoices(invoices)
    remaining = [amt for _, _, amt in inv]
    # due order = ascending ISO date (string order is chronological), ties by input index
    by_due = sorted(range(len(inv)), key=lambda i: (inv[i][1], i))
    rank = {i: r for r, i in enumerate(by_due)}
    by_id: dict[str, list[int]] = defaultdict(list)          # id -> indices in due order
    for i in by_due:
        by_id[inv[i][0]].append(i)
    by_amount: dict[int, deque] = defaultdict(deque)          # Parts 1-2: amount -> unpaid, due order
    for i in by_due:
        by_amount[remaining[i]].append(i)
    cursor = 0                                                # Parts 3-4: by_due[:cursor] fully paid
    audit: list[str] = []
    unapplied: list[str] = []

    for pid, amt, memo in parse_payments(payments):
        if amt <= 0:                                          # zero/negative payments carry no money
            continue
        # ---- candidate selection: None means "all invoices"
        if part == 1:
            m = EXACT_MEMO.fullmatch(memo)                    # strict: nothing else in the memo
            if not m or m.group(1) not in by_id:
                continue
            cands = by_id[m.group(1)]
        else:
            mentioned = {t for t in TOKEN.findall(memo) if t in by_id}
            cands = sorted((i for t in mentioned for i in by_id[t]), key=rank.__getitem__) if mentioned else None

        if part <= 2:
            # exact amount: earliest-due unpaid candidate whose amount == payment amount
            if cands is None:
                q = by_amount[amt]
                while q and remaining[q[0]] == 0:             # drop invoices paid via a memo
                    q.popleft()
                hit = q[0] if q else None
            else:
                hit = next((i for i in cands if remaining[i] == amt), None)
            if hit is not None:
                remaining[hit] = 0
                audit.append(f"{pid} -> {inv[hit][0]} {amt}")
            continue

        # Parts 3-4: pour into candidates oldest-first until the payment is exhausted
        if cands is None:
            while cursor < len(by_due) and remaining[by_due[cursor]] == 0:
                cursor += 1
            cands = (by_due[k] for k in range(cursor, len(by_due)))
        for i in cands:
            if amt == 0:
                break
            pay = min(amt, remaining[i])
            if pay == 0:
                continue
            remaining[i] -= pay
            amt -= pay
            audit.append(f"{pid} -> {inv[i][0]} {pay}")
        if amt > 0:                                           # leftover never spills elsewhere
            unapplied.append(f"{pid}: UNAPPLIED {amt}")

    lines = audit if part == 4 else []
    for (iid, _, total), rem in zip(inv, remaining):
        status = "PAID" if rem == 0 else ("UNPAID" if rem == total else f"PARTIAL (remaining {rem})")
        lines.append(f"{iid}: {status}")
    if part >= 3:
        lines += unapplied
    return lines


def part1(invoices: list[str], payments: list[str]) -> list[str]:
    return reconcile(invoices, payments, 1)


def part2(invoices: list[str], payments: list[str]) -> list[str]:
    return reconcile(invoices, payments, 2)


def part3(invoices: list[str], payments: list[str]) -> list[str]:
    return reconcile(invoices, payments, 3)


def part4(invoices: list[str], payments: list[str]) -> list[str]:
    return reconcile(invoices, payments, 4)


PARTS = {1: part1, 2: part2, 3: part3, 4: part4}


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    has_header = lines[0].upper().startswith("PART")
    part = int(lines[0].split()[1]) if has_header else 1
    invoices, payments, section = [], [], []
    for ln in lines[1:] if has_header else lines:
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
