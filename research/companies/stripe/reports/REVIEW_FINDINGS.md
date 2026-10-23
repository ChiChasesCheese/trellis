# Adversarial review findings

Scope: q01, q02, q03, q04, q05, q09. Reviewer: Claude (adversarial pass). Date: 2026-08-26.

Severity: high = wrong answer on a valid input; medium = spec ambiguity that could flip a hidden test; low = style/clarity.

## q01_fraud_mcc_disputes — verdict: SOUND

Method: 3000 random streams (`random.Random(1)`, up to 6 accounts / 5 MCCs / 15 events incl. duplicate ids, disputes of unknown / already-disputed ids, interleaved setup lines) compared against an independent recompute-from-scratch oracle using `fractions.Fraction`, across 6 configs (part2, part3 sticky/non-sticky, part4 sticky/non-sticky/`dispute_removes_charge=False`): 0 mismatches. All 16 stdin cases (worked examples for PART 1/2/3/4/5, no trailing newline, CRLF, blank-only input, empty input, spaces around commas) match problem.md byte-for-byte. Perf: 10^4 events 0.031 s, 10^5 events 0.133 s (ratio 4.3x for 10x, startup-dominated, linear). Full suite: 21 passed.

Findings:
1. (medium, spec) Re-using a charge id after it was disputed: `CHARGE,c1,m,1,f` / `DISPUTE,c1` / `CHARGE,c1,m,1,f` -> solution counts the second CHARGE as a new charge (ledger entry was popped) and outputs `m`. problem.md says "a repeated charge_id is ignored (idempotent)" without saying whether a disputed id is still "seen". Either reading is defensible; the solution's reading (dispute erases the charge "as if it never happened") is consistent with Part 4 wording. Not changed; documented here so a hidden test can be diagnosed quickly.
2. (low) `main` parses the PART line with `lines[0].split()[1]`; `PART1` (no space) raises IndexError. Spec shows `PART n` with a space so this is out-of-contract; cheap to harden with a regex.
3. (low, tests) Three tests pass on the empty `starter_template.py`: `test_part2_ignores_disputes_and_empty` (compares two `{}` results and empty inputs only), `test_variant_dispute_marks_non_fraud_but_keeps_total` (every expected value is `NONE`, so a stub returning `NONE` passes), `test_perf_100k_events` (only checks one output line + timing). The first two should include at least one positive expectation. 18/21 fail on the template, so the suite is not vacuous overall.
4. (low) `starter.py` in the tree is a partially-filled drill copy (has `THRESHOLDS` typo, `literal.split(',')`), not the template; `IMPL=starter` fails 18/21 identically. Fine per CONVENTIONS.md, just noting it is not a clean template.
5. (low, spec) `parse_threshold('1.')` -> `('ratio', 1, 1)` and `fmt_threshold` prints `ratio,1.0` (round-trip not identity). Out-of-contract literal; no action.

## q02_merchant_fraud_score — verdict: SOUND

Method: 2500 random inputs (`random.Random(1)`; 1-4 merchants + a "ghost" merchant, 0-12 txns with amounts hitting 99/100/101/0/negative and hours hitting every band boundary, random rules incl. mult 0) vs an independent O(n^2) oracle that recounts pairs from scratch for each transaction, for part1/part2/part3: 0 mismatches. 11 stdin cases (Examples 1-4, no trailing newline, CRLF, empty, blank-only, `PART 3` alone, merchants-only, empty TRANSACTIONS/RULES sections) match problem.md byte-for-byte; empty input produces empty output (no newline) which is consistent with "one line per merchant". Perf: 10^4 txns 0.038 s, 10^5 txns 0.188 s (ratio 4.9x for 10x, linear). Template: 29/29 fail (no vacuous tests). Suite: 29 passed.

Findings:
1. (medium, spec) Transactions whose `merchant_id` is not in MERCHANTS are silently dropped (`if t[0] in scores`), and the test `test_unknown_merchant_transactions_are_ignored` locks that in, but problem.md never states this rule. A hidden test could equally expect the merchant to appear with base 0 or the run to error. Suggest adding one sentence to the Rules section ("transactions of undeclared merchants are ignored; they still consume their rule slot").
2. (low, spec) Duplicate `merchant_id` lines in MERCHANTS: last base_score wins (dict overwrite). Not stated in problem.md.
3. (low) `zip(transactions, rules)` silently truncates when the RULES section is shorter than TRANSACTIONS; the spec guarantees equal length, so no wrong answer on valid input, but a malformed hidden input would fail silently rather than loudly.
4. (low, spec) problem.md states `n, m <= 1000` while the perf test drives 10^5 transactions in < 2 s; harmless (stricter than the contract) but the numbers disagree.
5. (low) `main` does `{1,2,3}[part]` -> KeyError for `PART 4`; spec says n in 1..3 so out-of-contract.

## q03_chat_billing — verdict: SOUND

Method: 3000 random months (`random.Random(1)`; 1-3 users x 1-8 sessions, token values drawn from block/allowance boundaries {0,99,100,101,199,20000,39999,40000,40099,40100,13333,13400,13500,10^9} plus random, plans shuffled) vs an independent `decimal.Decimal` oracle (ROUND_HALF_UP on the fee, allowance consumed greedily input-then-output): 0 mismatches. 7 stdin cases (worked example, no trailing newline, CRLF, reversed input order, blank lines in between, empty, whitespace-only) match problem.md byte-for-byte; empty input -> empty output, no newline. Perf: 10^4 lines 0.030 s, 10^5 lines 0.113 s (ratio 3.8x, linear). Template: 19/20 fail. Suite: 20 passed.

Findings:
1. (medium, spec) When the prorated allowance is not a multiple of 100 (r = 1/3 -> 13,333 tokens), a fixed session of 13,400 billable tokens leaves 67 overage tokens and the solution floors again to 0 blocks -> `u: $5.00`. problem.md says only "overage at payg block prices"; a grader that computes overage blocks as `ceil(67/100)` or that rounds the allowance itself down to a 100-multiple (13,300 -> 100 over -> 1 block -> $5.03) would disagree. The test `test_prorated_allowance_floors_and_payg_ignores_allowance` locks in the double-floor reading. Suggest one sentence in Part 3 stating that overage is billed in complete 100-blocks (the same rule as Part 1), which is the reading used.
2. (low) `plan` comparison is exact-case (`p == "fixed"`); `FIXED` or any unknown plan string is silently billed as payg (`u,100,100,FIXED` -> `$0.07`). In-contract inputs are lowercase, so no wrong answer on valid input; `.lower()` would be a free hardening.
3. (low, tests) `test_empty_stdin` passes on the empty template (inherently: empty in -> empty out). Not vacuous overall (19/20 fail).
4. (low, spec) The Rules never say what happens to a user with zero sessions (cannot occur since users only exist via session lines) nor whether `user_id` may contain spaces; both moot for the stated format.

## q04_card_range_obfuscation — verdict: SOUND (two spec ambiguities worth pinning down)

Method: 4000 random tables (`random.Random(1)`; 0-7 intervals over a tiny offset space 0..20 to force touching / nested / identical / same-start / same-end collisions, 3 brands, 10% wide 10^8-scale spans) vs an independent oracle (O(n^2) owner scan per gap, fixed-point merge loop) for Parts 1-4: 0 mismatches. Invariants checked on every case: after Part >= 2 the union of intervals covers `[LO, HI]` with no hole and starts at LO; after Part 4 no two consecutive same-brand touching intervals remain: 0 failures. 18 stdin cases (Examples 1-5 with and without `PART n`, Example 3 under PART 1/2/4, no trailing newline, CRLF, `N = 0`, empty, `PART 2` alone, BIN with leading zero `042424`) match byte-for-byte. Perf: 10^4 intervals 0.035 s, 10^5 0.314 s (9x for 10x; n log n sort, well under 2 s). Template: 23/24 fail. Suite: 24 passed.

Findings:
1. (medium, spec) Part 4 merges only *consecutive* same-brand intervals in `(start,end,brand)` order. Input `0,4,VISA` / `2,3,AMEX` / `5,9,VISA` yields three lines (`...0000,...0004,VISA` / `...0002,...0003,AMEX` / `...0005,...9999,VISA`) because AMEX sits between the two VISA pieces in sort order, even though the VISA pieces touch. Likewise `0,9,VISA` / `2,3,AMEX` / `4,6,VISA` keeps the contained VISA piece. The literal spec ("consecutive", "repeat until nothing merges") supports the solution, but a grader that merges same-brand touching intervals regardless of what is printed between them would output one VISA line. Suggest the spec state this explicitly (or the Variants section mention the alternative).
2. (medium, spec) Part 1 tie on the smallest start: `5,10,A` / `5,20,B` -> A (first in sorted order, i.e. the *smaller end*) gets `start = LO`; B keeps start 5. problem.md only gives a tie rule for the largest end (Part 3: smaller start wins). By analogy one could argue the covering interval (B, larger end) should be the one extended to LO. Output differs between the two readings. Suggest stating "ties on the smallest start: the one with the smaller end / first in sorted order".
3. (low) The `N` line is parsed but not used; extra or missing interval lines are processed as-is (`N=1` with two lines -> both used). Tolerant, but a hidden test relying on N to truncate would differ; out-of-contract.
4. (low, tests) `test_n_zero_prints_nothing` passes on the empty template (inherent). 23/24 fail, suite not vacuous.
5. (low) Sorting happens three times (extend_outer, fill_gaps, render); harmless for 10^5 but a cheap tidy-up.

## q05_card_validation_luhn — verdict: SOUND

Method: 2500 random cards (`random.Random(1)`; lengths 13/15/16/17, prefixes 4/50/51/55/56/34/35/37/2223/6011, half forced Luhn-valid) compared to an independent oracle with its own Luhn (digit-sum-of-doubled formulation) and explicit prefix table: `classify`/`part1` 0 mismatches; `masked_counts`/`part3` vs brute-force enumeration of all `*` completions (1-3 stars, plus 4-5 star cases every 40th iteration) 0 mismatches; `recover`/`part4` vs brute-force single-change + adjacent-swap enumeration sorted by `int()` 0 mismatches. 12 stdin cases (Examples 1-4 and 6 verbatim, PART-protocol without trailing newline, CRLF, HackerRank form without the `Q` header, empty, `PART 3` alone, valid observed card -> no output) match byte-for-byte; Example 5 verified structurally (first line `4242424242424242,VISA`, 15 lines, `5242424242424249` second, `5272424242424242` last). Perf: 3000 mixed P3/P4 queries 0.44 s, 10^4 1.42 s (linear; ~140 us per P4 query dominated by ~150 candidate Luhn checks). Template: 16/20 fail. Suite: 20 passed.

Findings:
1. (medium, robustness) Bare card lines with no `PART n` line and no `Pk` tag crash: stdin `4242424242424242\n4242424242424241\n` -> first line is consumed as the `Q` header (`isdigit()`), second line hits `tag, card = ln.split()` -> `ValueError`, empty stdout, non-zero exit. problem.md only promises the two tagged protocols, so this is out-of-contract, but the source (femisowems repo) has "one card per line" samples and a hidden Part-1 file with raw cards is plausible. The part is fully inferable from the line itself (`*` -> P3, trailing `?` -> P4, otherwise P2, which equals P1 for 16-digit 4-prefixed cards), so a fallback dispatch would be cheap. Not changed (no wrong answer on in-contract input).
2. (low, tests) Four tests pass on the empty template: `test_masked_dp_matches_brute_force` (brute force is computed with the stub's own `network_of`/`luhn_ok`, so `{} == {}`), `test_valid_observed_card_has_no_originals`, `test_recover_wrong_length_yields_nothing` (all expect `[]`), `test_perf_...` (timing only). The DP-vs-brute test should use a self-contained Luhn/network in the test rather than `impl.*`, otherwise it is tautological for any implementation.
3. (low, spec) The perf budget is stated as "< 2 s" for 3000 queries; problem.md never bounds `Q`. At 10^5 queries the current P4 path would take ~14 s. Fine for the stated OA (5 tests per part) but worth a sentence in problem.md.
4. (low, spec) Part 1 says the input "is a 16-digit number starting with 4" and the solution only checks Luhn (a Part-1 line `5555555555554444` prints `VISA`). Consistent with the contract; noting only that Part 1 is not a subset of Part 2 for out-of-shape input.

## q09_jupyter_load_balancer — verdict: SOUND

Method: 3000 random request streams (`random.Random(1)`; 1-4 targets, cap in {0,1,2,3,10}, 0-25 requests over 6 reusable ids / 3 objects / SHUTDOWN indices 0..n+1, 30% `shutdown_permanent`, 15% `variant_b`) vs an independent oracle that recomputes loads by scanning active connections and picks the least-loaded target by linear scan: 0 mismatches; every logged target index in 1..n. 9 stdin cases (Examples 1-3, no trailing newline, CRLF, empty, header-only, header with extra spaces, blank lines between requests) match byte-for-byte. Perf (n=10^5 targets): 2x10^4 requests 0.08 s, 2x10^5 requests 0.336 s (4.2x for 10x, linear; heap with lazy invalidation works). n=10^4 / 2x10^5 requests 0.259 s. Pathological: 1 target, 10^5 CONNECT then 10^5 SHUTDOWN -> 0.16 s (all evicted once, later shutdowns are no-ops). 3 targets, 10^5 sticky connections, 100 alternating SHUTDOWNs -> 4.0 s but emits 5.08 M log lines, i.e. output-bound and inherent to the spec ("each successful re-route is logged"). Template: 23/24 fail. Suite: 24 passed.

Findings:
1. (medium, spec) Re-route order on a second SHUTDOWN. `2 10` / `CONNECT a u` / `CONNECT b u` / `CONNECT c u` / `SHUTDOWN 1` / `SHUTDOWN 2`: after the first shutdown target 2 holds b (arrived 2nd) plus re-routed a, c (arrived 1st, 3rd). The solution evicts by *original* CONNECT sequence -> `a,u,1 / b,u,1 / c,u,1`; a grader that orders by the time each connection landed on the target would print `b,u,1 / a,u,1 / c,u,1`. problem.md says "original CONNECT arrival order", which supports the solution, but the phrase is one adjective away from the other reading; worth an explicit example in the Edge-cases list. No test pins this down today.
2. (low, spec) A re-routed connection keeps its original `seq`; a connection re-placed by SHUTDOWN and later re-CONNECTed under the same id after a DISCONNECT gets a new seq. Consistent, undocumented.
3. (low) `SHUTDOWN` with a non-integer index (`SHUTDOWN x`) raises `ValueError`; out-of-contract.
4. (low, tests) `test_empty_and_header_only_stdin` passes on the empty template (inherent). Suite otherwise not vacuous.
5. (low) The heap is never compacted; after 2x10^5 requests it holds at most n + requests entries (~3x10^5 tuples), well inside the 256 MB budget.

## Summary
No HIGH findings; no solution.py or test file was modified. Medium items are all spec ambiguities that a one-line clarification in the relevant problem.md would close: q01 #1, q02 #1, q03 #1, q04 #1-2, q05 #1, q09 #1.
