# q25 · Invoice / Payment Reconciliation — match incoming payments to open invoices

## Context
A Stripe Invoicing merchant receives bank transfers that do not carry a Stripe invoice reference.
Each transfer has an id, an amount and a free-text memo the customer typed. Reconciliation is the
job of deciding which open invoice(s) each payment settles. Real reconciliation starts with an
exact rule (memo names the invoice, amount matches) and progressively relaxes it (match by amount
to the oldest invoice, let one payment cover several invoices, keep an audit trail).

## Input (stdin)
```
PART <n>
INVOICES
<invoice_id>,<due_date YYYY-MM-DD>,<amount_cents>
...
PAYMENTS
<payment_id>,<amount_cents>,<memo free text, may be empty, may contain commas>
...
```
Blank lines are ignored; spaces around separators are tolerated. A payment line is split on its
**first two commas only** — everything after the second comma is the memo. Amounts are integer
cents. Up to 10^5 invoices and 10^5 payments. Payments are processed **in input order**.
Each part is also callable as `partN(invoices: list[str], payments: list[str]) -> list[str]`.

## Output
One line per invoice **in input order**: `<invoice_id>: PAID`, `<invoice_id>: UNPAID`, or (Part 3+)
`<invoice_id>: PARTIAL (remaining <cents>)`. Part 3+ then prints, in payment input order, one line
per payment with money left over: `<payment_id>: UNAPPLIED <cents>`. Part 4 prefixes the whole
output with the audit trail (see Part 4). An invoice with amount 0 is `PAID` from the start.
"Due order" everywhere means ascending due date, ties broken by invoice input order.

## Rules
### Part 1 — exact memo, exact amount
A payment settles an invoice only if its memo is **exactly** `Paying off: <invoice_id>` (spaces
around the id tolerated; nothing else in the memo), that invoice exists and is unpaid, and the
payment amount **equals** the invoice amount. Then the invoice is `PAID`. Any other payment is
ignored (a second payment for an already-paid invoice is ignored — no double application).

### Part 2 — relaxed memo, still exact amount
The memo is free text. Tokenize it on anything that is not `[A-Za-z0-9_-]`; every token equal to
an invoice id is a *mention*. Candidates are the mentioned invoices if there is at least one
mention, otherwise **all** invoices (empty memo, or memo without recognizable ids). The payment
settles the **earliest-due unpaid candidate whose amount equals the payment amount**. If no
candidate qualifies the payment is ignored — a memo that names invoices never falls back to the
unmentioned ones.

### Part 3 — one payment may cover several invoices
Candidates are chosen as in Part 2, but the amount no longer has to match. The payment is poured
into the candidates **in due order (oldest first)**: each invoice takes
`min(payment_left, invoice_remaining)` until the payment is exhausted. An invoice with money still
owed after all payments is `PARTIAL (remaining r)` (or `UNPAID` if untouched). Money left after
the last candidate is reported as `<payment_id>: UNAPPLIED <left>` — it never spills onto
unmentioned invoices. Payments with amount ≤ 0 are ignored and produce no line.

### Part 4 — audit trail (reconstructed)
Same matching as Part 3. Before the invoice lines, print one line per application, in the order
the applications happened: `<payment_id> -> <invoice_id> <cents_applied>`. Then the invoice
status lines, then the `UNAPPLIED` lines.

## Worked examples
**Example A — Part 1**
```
PART 1
INVOICES
invoiceA,2024-01-01,100
invoiceB,2024-01-15,200
invoiceC,2024-02-01,500
PAYMENTS
paymentABC,500,Paying off: invoiceC
payment2,200,Paying off: invoiceA
payment3,100,invoiceA
```
```
invoiceA: UNPAID
invoiceB: UNPAID
invoiceC: PAID
```
payment2 names invoiceA but 200 ≠ 100 → ignored; payment3's memo is not the exact form → ignored.
Under **Part 2** the same input gives `invoiceA: PAID / invoiceB: UNPAID / invoiceC: PAID`
(payment3 mentions invoiceA and 100 = 100; payment2 still mismatches).

**Example B — Part 2**
```
PART 2
INVOICES
invoiceA,2024-03-01,100
invoiceB,2024-01-01,100
invoiceC,2024-02-01,300
PAYMENTS
p1,100,
p2,100,Thanks!
p3,250,Paying off: invoiceA and invoiceC
```
```
invoiceA: PAID
invoiceB: PAID
invoiceC: UNPAID
```
p1 (no memo) → earliest-due unpaid 100-invoice is invoiceB; p2 (no ids) → invoiceA; p3 mentions
A and C but 250 matches neither → ignored.

**Example C — Part 3**
```
PART 3
INVOICES
invoiceA,2024-01-01,100
invoiceB,2024-01-15,200
invoiceC,2024-02-01,500
PAYMENTS
paymentABC,500,Paying off: invoiceC
payment2,250,
payment3,40,Paying off: invoiceB
payment4,1000,Paying off: invoiceA
```
```
invoiceA: PAID
invoiceB: PARTIAL (remaining 10)
invoiceC: PAID
payment4: UNAPPLIED 1000
```
payment2 → 100 to invoiceA, 150 to invoiceB; payment3 → 40 more to invoiceB (10 left);
payment4 names invoiceA, which is already paid → all 1000 unapplied.

**Example D — Part 4** (same input as Example C with `PART 4`)
```
paymentABC -> invoiceC 500
payment2 -> invoiceA 100
payment2 -> invoiceB 150
payment3 -> invoiceB 40
invoiceA: PAID
invoiceB: PARTIAL (remaining 10)
invoiceC: PAID
payment4: UNAPPLIED 1000
```

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
