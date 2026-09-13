# Stripe OA drill kit — overall report

**Date:** 2026-08-26 · **Repo:** https://github.com/ChiChasesCheese/stripeoa · **Local:** `~/Code/ITV/stripe-oa`
**State:** 53 problem sets (40 bespoke + 13 LeetCode-tag), 965 tests, all green (`reports/TEST_SUMMARY.md`).

## 1. What the OA is (triangulated, see `catalog/CATALOG.md` header + `catalog/raw/process_and_jd.md` §A)

- HackerRank, **60 min hard limit, ONE bespoke problem in 3–5 parts** that unlock in sequence; each part extends the same program.
- **~17–25 hidden tests**; reported outcomes 14/20 (reject), 18/20, 22/25, 16/19 (advance). No score shown; partial credit advances.
- **Not LeetCode**: stdin/CSV parsing → dict-of-records state → business rules → exact stdout. Stripe employee on Blind: "input parsing, creating classes, proper data structures, business logic".
- Language free; Stripe engineers advise against Java for speed. Browser IDE, print-debug only, tab-focus logged, AI/paste detection.
- The OA bank is **small and recycled** (programhelp 2026-03: ~3 problems rotating; Blind: "Stripe has a small fixed set of questions"). The same problems recur in the 45–60 min phone screen.

## 2. Drill order (from `catalog/CATALOG.md` "Top 10", ranked OA stage × recency × #refs)

| # | dir | why |
|---|---|---|
| 1 | `q01_fraud_mcc_disputes` | 2025–26 intern/NG flagship; 5 parts; 8 refs; last 2026-07 |
| 2 | `q09_jupyter_load_balancer` | 5-part OA, 13 refs, needs a heap to pass perf |
| 3 | `q02_merchant_fraud_score` | ran alongside q01 in the Oct–Nov 2025 cycle; strict `>` and once-per-group traps |
| 4 | `q18_collusion_ring` | OA 2026-07 with verbatim examples; union-find |
| 5 | `q17_datacenter_router_haversine` | newest verbatim OA (2026-08-11/13) |
| 6 | `q07_subscription_notifications` | OA + VO, 13 refs; event ordering + reversals |
| 7 | `q03_chat_billing` | InterviewDB "last reported Aug 2026"; metered + prorated billing |
| 8 | `q15_kyc_verification` | "five incremental steps", CSV validation |
| 9 | `q29_deployment_windows` | OA 2026-08 (UTC mapping + sliding window) |
| 10 | `q08_store_closing_penalty` | most-attested problem overall (16 refs), LC 2483 twin |

Then: q04 q13 q05 q06 q10; phone-screen set: q22 q21 q19 q25 q32. Algo set qA01–qA13 for the phone screen / onsite.

## 3. Catalog (`catalog/CATALOG.md`)

- **Table A — 42 bespoke problems** (22 OA-bearing, 20 phone/onsite), each with aliases, stage, parts, last-asked date, **#independent refs**, confidence, source URLs (16 footnotes for rows with > 6 sources). 40 have a `problems/` dir.
- **Table B — 18 algorithm rows**: the 14 LeetCode Stripe-tag problems with frequency triples from three company-wise mirrors (snehasishroy 2026-07, liquidslr 2025-06, shreeratn 2025-05) + 4 non-tag algorithm reports. 13 have a dir.
- **Table C — 32 title-only / unverified items** (Observability, Stripepay Backend, Factory Cost, User Roles, MLE OA, integration/bug-squash/design rounds, ignored SEO lists) with where each was seen.
- Raw research kept verbatim in `catalog/raw/` (5 files, ~2,100 lines): Chinese sources, English forums, GitHub repos with verbatim prompts and sample I/O, LeetCode-tag CSVs, process/JD/glossary.

Source reliability: 1point3acres 题库 / LeetCode Discuss / Blind / GitHub repos with prompts = high; csoahelp / programhelp / oavoservice dated write-ups = medium (consistent details, but they sell OA help); interviewfox / linkjob / extrabrain / lodely = low (AI-rewritten; type is right, numbers are not). Every problem.md states which version was chosen when sources conflict and lists the others under *Variants*.

## 4. Skills matrix (`skills_matrix.md`)

24 bespoke test targets S01–S24 (each backed by candidate reports or Stripe docs) and 16 algorithm targets A01–A16, mapped to the problems that drill them and to the recurring JD lines (9 Stripe SWE JDs 2025–26 + the two already evaluated in career-ops). The ones that decide pass/fail most often: S01 read everything first · S04 once-per-group aggregation · S05 strict vs non-strict thresholds · S06 integer money + explicit rounding · S08 tie-breaks · S09 byte-exact output · S10 reversals · S11 idempotency.

## 5. What each problem set contains

`problems/qNN_slug/`: `problem.md` (standardized statement: context, I/O, rules per part, 3+ worked examples, hidden-test edge list, variants, skills, sources) · `starter_template.py` + `starter.py` (yours) · `solution.py` (reference, integer money, deterministic ties, commented rules) · `test_qNN.py` (markers part1–5 / edge / fmt / perf / io; same suite runs against your starter via `IMPL=starter`) · `REPORT.md` (approach per part, pitfalls, measured time/memory, test inventory, skills).

Test inventory: **965 tests = 453 edge · 60 fmt · 55 perf · 75 io**, plus worked examples verbatim. Perf budgets 2 s / 256 MB on the largest plausible input (10^5–10^6 records); all measured runs ≤ 1.3 s. Every suite was confirmed to FAIL against the empty starter (non-vacuous).

Reconstruction policy: where a source only gave a part's title (q15 P4–5, q17 P4, q28, q29, q37, q40, algo follow-ups), the rule was designed to be faithful to the title and is marked **(reconstructed)** in problem.md — treat those parts as practice, not as the exact hidden tests.

## 6. Quality gates applied

- Each suite run against the reference (green) and the empty starter (must fail).
- Verbatim samples from GitHub repos / candidate posts reproduced byte-for-byte where they exist (q05, q06, q08, q17, q18, q24, q30, q31, q32, q33, q35).
- Source conflicts resolved explicitly and the alternative kept behind a flag + tests (q01 sticky flag, q02 repeat_mode, q05 output format, q17 tie order, q19 zero-q, q20 rounding, q39 log polarity).
- Bugs the suites caught during construction: q07 memory (282 MB → 197 MB), q12 rule re-tokenizing (3.98 s → 0.28 s), q26 lock migration, q03 hand-computed expectations, plus several wrong test expectations fixed on the test side.
- Adversarial review (independent brute-force oracles, ≥ 2500 random cases per problem, io byte-diff, quadratic check) on the top-12 OA problems → `reports/REVIEW_FINDINGS.md`, `REVIEW_FINDINGS_2.md`. Result: 11 SOUND / 1 BUG FOUND (q10 `INIT` arity — fixed, regression test added); 1 high, 12 medium spec ambiguities (each now written into the problem.md "Clarifications" section), ~40 low. q05's DP-vs-brute-force test was tautological and was rewritten with an independent oracle.

## 7. How to drill (60 minutes, the real protocol)

```
python drill.py start q01        # prints the WHOLE statement; timer starts
python drill.py test q01 -k part1 # lock part 1, then part 2 …
python drill.py test q01          # full: edge + fmt + perf + io
python drill.py time q01
python drill.py ref q01           # the reference passes everything
```
Minute 0–5 read all parts; decide the state shape from the LAST part. 5–45 code part by part, lock each with the tests. 45–55 boundary sweep (empty / single / duplicate / out-of-order / zero / negative / exact threshold). 55–60 output format only. Print debug to stderr, delete before submit.

## 8. Caveats

- 1point3acres threads and question-bank full texts are login/paywalled; their content comes from snippets + question-page first screens. The five threads listed in `catalog/raw/cn_sources.md` §5 (e.g. thread-1145788 "stripe OA 彙整 2026") are worth a manual read with your account.
- Numbers in aggregator rewrites (rates, thresholds) were not trusted unless corroborated; problem.md notes the trusted source per number.
- Stripe monitors pasting/similarity: drill here, but in the real OA type from scratch.
