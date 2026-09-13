# q25 Invoice / Payment Reconciliation — report

## Summary
Match incoming bank transfers (id, amount, free-text memo) to open invoices with rules that
relax part by part: exact memo + exact amount, then memo tokens or "all invoices" with exact
amount to the earliest-due invoice, then one payment poured oldest-first across several
invoices with `PARTIAL` / `UNAPPLIED` reporting, then an audit trail. It is Stripe Invoicing's
reconciliation of un-referenced payments; the difficulty is candidate selection (mentioned
invoices never fall back to the rest) and keeping input-order output while matching in due order.

## Sources & confidence
medium — 2 independent mentions: 1point3acres interview/post/7379560 (`payment="paymentABC,
500,Paying off: invoiceC"`, invoices `["invoiceA,2024-01-01,100",…]`, progressively relaxed
rules, integration variant adds an API) and the 1point3acres 题库 entry (High frequency, last
asked 2026-08-13); catalog/raw/cn_sources.md §3. Part 4 (audit trail) is reconstructed from the
"integration variant adds an API" remark.

## Approach by part
Parse invoices `(id, due, cents)` and payments split on the first two commas only. Due order
= ISO date string order, ties by input index (`by_due`). One `reconcile(invoices, payments,
part)` engine; `partN` wrappers.
1. `EXACT_MEMO.fullmatch` (`Paying off:\s*(\S+)`), invoice must exist, be unpaid, and
   `amount == remaining`; otherwise ignored.
2. Tokens `[A-Za-z0-9_-]+` that equal an invoice id are mentions; candidates = mentions or all.
   Exact amount: `by_amount[amt]` deque in due order, skipping invoices already paid → earliest
   due; for mentioned candidates, scan them in due order.
3. Pour `min(left, remaining)` into candidates oldest-first; unmentioned payments advance a
   `cursor` over fully paid invoices so the walk is amortized O(n); leftover → `UNAPPLIED`,
   never spills; `amt <= 0` ignored silently.
4. Same engine recording `payment -> invoice cents` lines first.

## Pitfalls hidden tests target
- idempotent: a second payment for a paid invoice is ignored (P1–2) or fully `UNAPPLIED` (P3)
- P1 memo is strict (`Paying off: invoiceA today` fails); P2 tokens are whole (`invoiceAB` does
  not mention `invoiceA`); memos with commas keep their text
- earliest-due ties → input order; output always in invoice input order
- boundaries: `payment == remaining` → `PAID`, one below → `PARTIAL (remaining 1)`, one above
  → `UNAPPLIED 1`; zero / negative payments produce no line; 10^12-cent amounts stay integer
- empty invoice list → no output; no payments → all `UNPAID`

## Complexity & measured cost
O((n + m) log n) for the due sort plus amortized O(n + m + mentions) matching, O(n + m)
memory. 100k invoices + 100k payments (half memo-addressed, half blank, Part 3): ~0.39 s,
~132 MB RSS (budget 2 s / 256 MB).
Measured: 0.386s, 132 MB

## Test inventory
19 tests — part1: 6 · part2: 5 · part3: 5 · part4: 3; edge 9 · fmt 2 · perf 1 · io 2.
`IMPL=starter`: 19 fail / 0 pass.

## Skills exercised
S02 parsing (memo split) · S03 records by id · S05 exact-vs-relaxed matching · S06 integer money ·
S08 deterministic due order · S09 exact formatting · S11 idempotent application ·
S19 incremental design
