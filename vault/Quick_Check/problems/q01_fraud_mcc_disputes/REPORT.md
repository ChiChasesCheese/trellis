# q01 Fraud Detection by MCC — report

## Summary
The most-reported Stripe University-Recruiting OA (2025–2026): Radar-style merchant flagging by MCC
threshold over an ordered CHARGE/DISPUTE stream. It is "two counters per merchant" plus three things
candidates get wrong — count vs ratio thresholds (with a min-volume gate), exact `≥` semantics without
floats, and unwinding a charge when a dispute arrives (idempotently).

## Sources & confidence
high (rules) — interviewfox 2026-07 5-part write-up with per-part test counts; linkjob 2025-09 and
extrabrain 2026-02 3-part variant; programhelp 2025-08; 1point3acres Summer-2026 intern threads and two
leetcode-discuss OA posts (snippets only). medium (input syntax) — no source gives the setup-line
grammar verbatim; `MERCHANT/THRESHOLD/FRAUD_CODES/MIN_COUNT` lines and the `PART n` header are ours.
The event lines `CHARGE,charge_id,account_id,amount,code` / `DISPUTE,charge_id` are as reported.

## Approach by part
1. `part1` — one pass over setup lines; threshold literal with `.` → `("ratio", num, 10^k)`, without →
   `("count", n, 1)`. Fraud codes are a set (union over repeated lines).
2. `part2` — `fraud[acct]`, `total[acct]` (defaultdict) + a ledger `charges[charge_id] = (acct, is_fraud)`.
3. `part3` — after every event re-evaluate the touched account only: count `fraud ≥ n`; ratio
   `total ≥ min_count and fraud·den ≥ num·total`. Unknown MCC / no threshold / total 0 → never.
   `sticky` (keyword or `STICKY` line) keeps a once-flagged account in the set.
4. `part4` — DISPUTE pops the ledger entry, decrements `total` (and `fraud` if it was fraud), re-evaluates.
   `dispute_removes_charge=False` gives the 3-part variant (charge stays counted, becomes non-fraud).
5. `part5` — same engine; double dispute / unknown id fall out of "not in ledger → no-op".

Conflicts resolved: 3-part sources say "once flagged stays flagged" and simultaneously "can recover after
a dispute"; the 5-part (more sources) says re-evaluate → primary is non-sticky, sticky is a flag. One
retelling has the count threshold as strict "exceeds"; primary is `≥` (interviewfox wording).
Reconstructed: `MIN_COUNT` gates ratio thresholds only; duplicate `charge_id` is ignored.

## Pitfalls hidden tests target
`==` boundary on both thresholds; float ratio comparison (1/3 vs 0.33, 0.1); `1` vs `1.0`; MIN_COUNT
boundary; disputing a *non-fraud* charge raising the ratio; double dispute; dispute of unknown id;
all charges disputed (0/0); accounts with no MERCHANT/threshold present in counts but never flagged;
`NONE` literal; plain string sort (`acct_10` < `acct_2`); sticky vs re-evaluated.

## Complexity & measured cost
O(events + merchants log merchants). 100k events (25 % disputes) / 5k merchants.
Measured: 0.16s, 47 MB (budget 2 s / 256 MB).

## Test inventory
21 tests — part1: 4 · part2: 3 · part3: 6 · part4: 4 · part5: 4 (incl. 1 io, 1 perf); edge 12 · fmt 2 · io 2 · perf 1.
IMPL=starter: 18 fail / 3 pass (the three "NONE"-only assertions) — suite is not vacuous.

## Skills exercised
S02 parsing · S03 modeling (counters + ledger) · S05 threshold semantics · S08 deterministic sort ·
S09 exact formatting · S10 event stream with reversals · S11 idempotency · S18 validation · S19 incremental design
