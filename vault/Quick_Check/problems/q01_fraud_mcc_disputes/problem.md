# q01 · Fraud Detection by MCC — CHARGE/DISPUTE event stream ("Catch Me If You Can")

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 5 parts unlocked one after another) ·
**Last asked:** 2026-07 (interviewfox write-up of a 2026 NG OA; 1point3acres Summer 2026 intern OA threads)
**Frequency:** 7 independent mentions (interviewfox, linkjob, extrabrain, programhelp, leetcode-discuss ×2,
1point3acres threads 1163662/1147871) · **Confidence:** high (rules) / medium (exact input syntax — reconstructed)

## Context
Stripe Radar watches every merchant (a connected *account*) that processes card charges. Each merchant
carries a **Merchant Category Code (MCC)** and every MCC gets its own fraud tolerance: some categories
tolerate a fixed **number** of fraudulent charges, others a **fraction** of fraudulent charges once the
merchant has enough volume to judge. A charge's `code` (the network result code) tells us whether it was
fraud. Later, a **dispute** (chargeback) can arrive for an earlier charge; a dispute reverses that charge
completely, so counters must be unwound and the merchant re-evaluated. Your program ingests the setup
data and the event stream and reports which accounts are currently flagged as fraudulent.

## Input (stdin)
Comma-separated lines, blank lines ignored, spaces around commas tolerated. Setup lines are applied
**before** any event, wherever they appear in the file. The first line may optionally be `PART n`
(see *Output*).

```
MERCHANT,<account_id>,<mcc>            merchant → MCC (last one wins if repeated)
THRESHOLD,<mcc>,<value>                integer literal (e.g. 3)  → COUNT threshold
                                       decimal literal (e.g. 0.25, 1.0) → RATIO threshold
FRAUD_CODES,<code>[,<code>...]         result codes that mean fraud (repeatable; union)
MIN_COUNT,<n>                          minimum charge count before a RATIO threshold may fire (default 0)
STICKY                                 optional: once flagged, stay flagged (3-part variant, see Part 3)
CHARGE,<charge_id>,<account_id>,<amount>,<code>
DISPUTE,<charge_id>                    refers to an earlier CHARGE
```
`amount` is an integer in cents; it is parsed but never affects flagging. Charge ids are unique. Up to
10^5 event lines, ≤ 10^4 merchants.

## Output
Default (no `PART` line, or `PART 4` / `PART 5`): **one line** — the fraudulent account ids,
**lexicographically sorted (plain string order), joined by `,` with no spaces**, or the literal `NONE`
when no account is flagged.
`PART 1`: one line per merchant, sorted by account id: `account,mcc,count,<n>` /
`account,mcc,ratio,<literal>` / `account,mcc,NONE` (MCC has no threshold).
`PART 2`: one line per account that has at least one CHARGE, sorted: `account,fraud_count,total_count`
(DISPUTE lines are ignored in Parts 1–3).
`PART 3`: same as default but DISPUTE lines are ignored.

## Rules
### Part 1 — parse the setup
Build `merchant → MCC`, `MCC → threshold`, the fraud-code set and `min_count`. A threshold literal
**without** a decimal point is a count threshold; **with** a decimal point it is a ratio threshold, even
`1.0`. Parse ratio literals exactly (store `numerator/10^k`) — never as floats.

### Part 2 — process the event stream in order
For every `CHARGE` keep two counters per account: `total_count` (+1 per charge) and `fraud_count`
(+1 when `code ∈ fraud_codes`). Unknown codes are non-fraud. Charges for accounts that were never
declared with `MERCHANT` are still counted. A repeated `charge_id` is ignored (idempotent, reconstructed).

### Part 3 — flag fraudulent accounts
After each event re-evaluate the touched account:
* **count threshold** `v`: fraudulent iff `fraud_count ≥ v` (non-strict).
* **ratio threshold** `r`: fraudulent iff `total_count ≥ min_count` **and** `fraud_count / total_count ≥ r`
  — compare with integer cross-multiplication `fraud_count × den ≥ num × total_count`, no floats.
* An account with `total_count == 0`, with no `MERCHANT` line, or whose MCC has no `THRESHOLD`, is
  **never** flagged.
* Default (`sticky=False`): the output is the set of accounts fraudulent **after the last event**.
  With `STICKY` / `sticky=True` (3-part variant): an account that was ever fraudulent stays in the output.

### Part 4 — disputes reverse the original charge completely
`DISPUTE,<charge_id>`: the charge is removed as if it never happened — `total_count −= 1` and, if it was a
fraud charge, `fraud_count −= 1` — then the account is re-evaluated (so a non-sticky account can become
un-flagged, and disputing a *non-fraud* charge can push a ratio account **over** the line).

### Part 5 — edge cases (all must hold)
* a second `DISPUTE` for the same charge is a no-op;
* a `DISPUTE` for an unknown charge id is ignored;
* disputing a non-fraud charge only lowers `total_count`;
* a merchant whose every charge was disputed has `total_count == 0` → not flagged (no division by zero);
* accounts with an unknown MCC / no threshold are counted but never flagged;
* a `MIN_COUNT` gate applies to ratio thresholds only (reconstructed: count thresholds are volume-free).

## Worked examples
Setup used by all three examples:
```
MERCHANT,acct_a,5411
MERCHANT,acct_b,5812
MERCHANT,acct_c,5411
THRESHOLD,5411,2
THRESHOLD,5812,0.5
FRAUD_CODES,stolen_card,fraudulent
MIN_COUNT,3
```
**Example 1** (Parts 1–3)
```
CHARGE,ch_1,acct_a,1000,approved
CHARGE,ch_2,acct_a,2500,stolen_card
CHARGE,ch_3,acct_a,300,fraudulent
CHARGE,ch_4,acct_b,900,stolen_card
CHARGE,ch_5,acct_b,900,approved
CHARGE,ch_6,acct_c,100,stolen_card
-> acct_a
```
acct_a: fraud 2 / total 3, count threshold 2 → flagged. acct_b: 1/2 but total 2 < MIN_COUNT 3 → not
flagged. acct_c: 1/1, count threshold 2 → not flagged.
`PART 1` output: `acct_a,5411,count,2` / `acct_b,5812,ratio,0.5` / `acct_c,5411,count,2`.
`PART 2` output: `acct_a,2,3` / `acct_b,1,2` / `acct_c,1,1`.

**Example 2** (Part 4 — dispute un-flags) — Example 1 events followed by
```
DISPUTE,ch_2
-> NONE            (acct_a now 1/2 < 2)        with STICKY -> acct_a
```

**Example 3** (Part 4/5 — ratio merchant, disputing a non-fraud charge)
```
CHARGE,ch_4,acct_b,900,stolen_card
CHARGE,ch_5,acct_b,900,approved
CHARGE,ch_7,acct_b,900,stolen_card     acct_b 2/3 ≥ 0.5 and 3 ≥ 3 → flagged
DISPUTE,ch_5                           acct_b 2/2, but total 2 < 3 → un-flagged
CHARGE,ch_8,acct_b,900,approved        acct_b 2/3 → flagged again
DISPUTE,ch_5                           duplicate → no-op
DISPUTE,ch_999                         unknown → ignored
-> acct_b
```

## Edge cases hidden tests are known to target
- `==` on both thresholds (count 2 with exactly 2 frauds; ratio 0.5 with exactly 1/2) is fraudulent
- ratio compared in integers: 1/3 vs 0.33 is **above**, 1/3 vs 0.34 is below; 0.1 is exact
- `MIN_COUNT` boundary: total exactly `min_count` counts; one below does not
- `THRESHOLD,mcc,1.0` is a ratio (only 100 % fraud merchants); `THRESHOLD,mcc,1` is a count of one
- double dispute, dispute of unknown id, dispute of a non-fraud charge, all charges disputed (0/0)
- accounts with no `MERCHANT` line / MCC with no threshold: counted in `PART 2`, never in the flag list
- output `NONE` (not an empty line) when nothing is flagged; plain string sort (`acct_10` < `acct_2`)
- sticky vs non-sticky flagging after a dispute

## Variants seen in the wild
- **3-part variant** (linkjob 2025-09, extrabrain 2026-02): P1 count threshold ("exceeds the MCC's max
  fraudulent transactions"), P2 ratio + min count with **permanent** flagging, P3 `DISPUTE` marks the
  charge non-fraud and the merchant "can recover". Supported by `sticky=True` (Part 3) and
  `dispute_removes_charge=False` (dispute keeps the charge in `total_count` but makes it non-fraud).
- Count threshold as strict `>` ("exceeds") in one retelling — the primary here is `≥`; flip one
  comparison if your test data says otherwise.
- programhelp 2025-08 framing: Ticketmaster/Amazon-style large merchants, 0–1 ratio + minimum volume,
  permanent once triggered.

## What this tests
skills: S02 parsing · S03 modeling (two counters per merchant) · S05 threshold semantics (count vs ratio,
`≥`, min-volume gate) · S08 deterministic sort · S09 exact formatting (`NONE`) · S10 event streams with
reversals · S11 idempotency (double dispute) · S18 validation (unknown ids / MCCs) · S19 incremental design

## Sources
- https://interviewfox.ai/interview-questions/stripe-oa-hackerrank-guide/ (5-part version with per-part test counts)
- https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/ (3-part variant)
- https://extrabrain.app/interview-questions/stripe-hackerrank-online-assessment-extrabrain/ (3-part variant with input format)
- https://programhelp.net/en/oa/stripe-hackerrank-online-assessment-questions-guide/ ("Fraudulent Merchant Detection")
- 1point3acres thread-1163662 「Stripe Summer 2026 OA 分享」, thread-1147871 「2026 SDE Summer Intern OA」 (paywalled; snippets)
- leetcode discuss 7344444 (SWE Intern 2026), 7428741 (NG 2025-26 University Recruiting OA) (blocked; snippets)

## Clarifications (from adversarial review, 2026-08-26)
- A `CHARGE` that re-uses a charge id after that id was disputed is treated as a NEW charge (it counts again); a repeat of a live charge id is ignored.
