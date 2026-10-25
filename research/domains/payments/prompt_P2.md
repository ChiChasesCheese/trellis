# Card agent — payments domain (`payments`), group P2

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never switch branches, never commit, never spawn agents. You own
`vault/domains/payments/cards/<branch>/` for branches **reconciliation, cross-border, payouts, risk-compliance, platform** — nothing else. Scratch work in `/tmp/pay_P2/`.

## 0. Resume rule
`uv run trellis --domain payments stats` and `ls` your folders; skip leaves that already have cards. `git checkout uv.lock`
whenever uv touches it.

## 1. Read first
- `skeleton/payments.yaml`: your leaves, their summaries (what each must cover) and `requires`.
- `proposals/WRITING_RULES.md` rules 1, 3, 5, 6, 11, 12.
- Format example: `vault/domains/pl/cards/memory/pl-memory-tracing-gc-go-vs-java.md`.
- Related pages to stay consistent with: `vault/interviews/core/system-design/tiktok/sd01-payment-system.md`,
  `vault/interviews/core/fundamentals/tiktok/tiktok-idempotency-transactions.md`.

## 2. Who reads these cards
Chi: a backend engineer at PayPal/Braintree (fee and settlement pipelines, Amex settlement, interchange data,
reconciliation) interviewing with ByteDance **Global Payment** (acquisition, disbursement, transaction monitoring,
payment method management, FX conversion, accounting, reconciliation; high-availability, financially safe distributed
systems). Senior framing: the reasoning, the design space, the trade-offs and best practice — not definitions for their
own sake. But **never assume he already knows a concept**: introduce each one from zero before using it.

## 3. Cards per leaf: 6–9, in this order (`step`)
1. **Problem and principle**: what problem the concept solves for a payment business; the design space.
2. **Foundations** (1–3): each concept the leaf names, from zero — what it is, a concrete money example with numbers.
3. **Mechanism / worked flow**: the step-by-step flow with a concrete transaction (amounts, currencies, timestamps,
   which ledger accounts move).
4. **Design choices and trade-offs**: 2–4 options, what each buys and costs, which a large platform picks and why.
5. **Best practice**: what a senior payments engineer does, and why.
6. **Failure scenario**: a realistic incident (double charge, lost callback, reconciliation break, FX loss …), how it
   happens and how the design prevents or detects it.
7. **Interview angle**: how this shows up in a system design or deep-dive question, and the 3–4 points to say.
Code (Python, type hints) only where it shows a mechanism (idempotency store, state transition guard, matching);
≤ 15 lines; run it and quote the real output.

## 4. Card format
```
---
id: pay-<leaf-slug>-<card-slug>
node: <leaf id>
type: qa
step: <n>
---
## Q
...
## A
...
```
`id` lowercase ASCII + hyphens, starts with `pay-`, unique; file `<id>.md`; no `source:` / `tags:`. Chinese prose,
English terms in full-width parentheses on first use per card; ≤ 250 whitespace-separated words per answer (split
otherwise); tables ≤ 5 rows; no ASCII diagrams. Self-contained: the question names its subject; never refer to other
cards, sources, or where a fact came from. Numbers (fees, settlement days, chargeback windows) as typical magnitudes
with 约 / 通常, and only ones you are sure of; card-network rules change — say "通常" rather than quoting exact bps
you are unsure of.

## 5. Gate
`uv run trellis --domain payments validate` (0 errors, no `not_self_contained` / `leans_on_source` / word-count warnings
on your cards); `uv run python scripts/plain_style.py <your files>`; `uv run python scripts/phone_diagrams.py <your
files>`; `git checkout uv.lock`. Reply ≤ 10 lines: cards per branch, gate results, up to 6 claims you are least sure of.
