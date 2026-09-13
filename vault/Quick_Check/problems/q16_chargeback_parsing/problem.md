# q16 · Chargeback Parsing — parse network chargeback records, drop corrupted rows, cancel withdrawn disputes

**Type:** bespoke OA · **Stage:** HackerRank OA (University / New Grad 2024, 60 min, 3 parts) · **Last asked:** 2024-09-25 (leetcode discuss 5832245); programhelp 2025-08-08 repost
**Frequency:** 2 independent sources (leetcode discuss "Stripe University New Grad OA 2024"; programhelp 2025-08-08 「Parsing and Filtering Refund/Dispute Data」) · **Confidence:** medium (part structure and the withdrawn rule are verbatim; the exact field list and output line are reconstructed)

## Context
"Stripe processes billions of dollars… the end user can file a chargeback… the bank sends this
chargeback information to Stripe. The chargeback is the first stage in the lifecycle of a dispute; your
job is to extract relevant information about a dispute by parsing this chargeback information so the
dispute can be surfaced to the merchant." Card networks deliver chargebacks as flat files; rows can be
corrupted, and a cardholder can later *withdraw* a chargeback, in which case the merchant should never
see the dispute at all.

## Input (stdin)
First line `PART n`. Then one chargeback record per line (the concatenation of one or more network
files, in file order). Blank lines are ignored; spaces around commas are trimmed. Up to 2·10^5 lines.
```
network,transaction_id,amount,currency,reason,date
visa,txn_123,2500,usd,fraudulent,2024-01-05
```
(record shape reconstructed — the post does not list the fields.) Fields:
- `network` ∈ {`visa`, `mastercard`, `amex`, `discover`} (case-insensitive on input);
- `transaction_id`: opaque string, unique per network;
- `amount`: integer in the currency's **minor unit** (Stripe convention: `2500` = $25.00; `2500` JPY = ¥2500);
- `currency`: lowercase ISO 4217 code;
- `reason`: e.g. `fraudulent`, `duplicate`, `product_not_received`, `general`, `withdrawn`;
- `date`: `YYYY-MM-DD`.

## Output
One line per surviving record, **in input order**:
```
[NETWORK] transaction_id: <money> CURRENCY - reason (YYYY-MM-DD)
```
`NETWORK` and `CURRENCY` upper-cased. `<money>`: two-decimal currencies print `symbol + x.xx`
(`usd` → `$25.00`, `eur` → `€19.99`, `gbp` → `£50.00`); **zero-decimal** currencies (`jpy`, `krw`) print the
integer with no decimals (`¥2500`, `₩2500`); any other currency prints `x.xx` with no symbol (`12.34 CAD`).
Parts 2–3 then print `SKIPPED: n` (number of corrupted rows) as the last line, always (even `SKIPPED: 0`).

## Rules
### Part 1 — parse valid records
All rows are valid; print each in the format above.

### Part 2 — skip corrupted rows
A row is **corrupted** (skip it, count it, keep going) when any of:
- it does not have exactly 6 fields;
- `amount` is not an integer ≥ 0 (`25.00`, `abc`, `-1`, empty);
- `date` does not parse with `datetime.strptime(date, "%Y-%m-%d")` (`2024-02-30`, `2024-13-01`,
  `01/05/2024`); a valid date is re-printed normalized as `%Y-%m-%d`;
- `network` is not one of the four known networks (`paypal`, `visa2`, empty);
- `transaction_id`, `currency` or `reason` is empty.
Blank lines are not rows and are not counted. Output the valid rows in input order, then `SKIPPED: n`.

### Part 3 — cancel withdrawn disputes
Among the **valid** rows, group by `(network, transaction_id)`. If **any** row of a group has reason
`withdrawn`, **no row of that group is output** — the original and the withdrawal both disappear,
whichever came first (the source says "later-dated file… listed with reason withdrawn: do not process
either row"; arrival order does not matter here, and a group with two withdrawals or with only a
withdrawal is dropped too). Same `transaction_id` on a different network is a different dispute and is
unaffected. Withdrawn rows are not counted in `SKIPPED` (only corrupted rows are). Survivors print in
input order, then `SKIPPED: n`.

## Worked examples
```
PART 1
visa,txn_123,2500,usd,fraudulent,2024-01-05
mastercard,txn_124,1999,eur,product_not_received,2024-01-06
amex,txn_125,5000,gbp,duplicate,2024-01-07
discover,txn_126,2500,jpy,general,2024-01-08
->
[VISA] txn_123: $25.00 USD - fraudulent (2024-01-05)
[MASTERCARD] txn_124: €19.99 EUR - product_not_received (2024-01-06)
[AMEX] txn_125: £50.00 GBP - duplicate (2024-01-07)
[DISCOVER] txn_126: ¥2500 JPY - general (2024-01-08)
```
```
PART 2
visa,txn_1,2500,usd,fraudulent,2024-01-05
visa,txn_2,25.00,usd,fraudulent,2024-01-05        (amount not an integer)
paypal,txn_3,100,usd,fraudulent,2024-01-05        (unknown network)
visa,txn_4,100,usd,fraudulent,2024-02-30          (invalid date)
visa,txn_5,100,usd,fraudulent                     (5 fields)
visa,txn_6,100,usd,fraudulent,2024-01-05,extra    (7 fields)
->
[VISA] txn_1: $25.00 USD - fraudulent (2024-01-05)
SKIPPED: 5
```
```
PART 3
visa,txn_1,2500,usd,fraudulent,2024-01-05
visa,txn_1,2500,usd,withdrawn,2024-01-09
mastercard,txn_1,2500,usd,fraudulent,2024-01-05
visa,txn_2,100,usd,withdrawn,2024-01-01
visa,txn_2,100,usd,fraudulent,2024-01-03
visa,txn_3,700,usd,general,2024-01-03
->
[MASTERCARD] txn_1: $25.00 USD - fraudulent (2024-01-05)
[VISA] txn_3: $7.00 USD - general (2024-01-03)
SKIPPED: 0
```

## Edge cases hidden tests are known to target
- money: `5` → `$0.05`, `100` → `$1.00`, `0` → `$0.00`, `123456789` → `$1234567.89`; JPY never shows
  decimals; unknown currency has no symbol
- corrupted rows: too few / too many fields, `25.00`, negative, empty amount, `2024-02-30`, `2024-2-3`
  (accepted by strptime → printed `2024-02-03`), unknown network, upper-case `VISA` accepted
- `SKIPPED: 0` still printed; empty input prints only `SKIPPED: 0` (Part 1: nothing)
- withdrawn before the original; two withdrawals; withdrawal with no original; same id on two networks
  (only the withdrawn network's rows vanish); a *corrupted* withdrawal row does not cancel anything
- output order is input order (no sorting); duplicates of a non-withdrawn dispute are printed twice
- whitespace around fields, blank lines, trailing newline

## Variants seen in the wild
- The original reads "one or more files" and aggregates them; here files are concatenated on stdin.
- programhelp 2025-08-08 frames the same three parts as "refund/dispute data" with the corrupted rows
  described as "rows that cannot be parsed into a dispute object".

## What this tests
skills: S02 delimited parsing with malformed rows · S06 minor-unit money and zero-decimal currencies ·
S09 exact output formatting · S11 de-duplication / reversal of paired events · S12 date validation ·
S18 validation and error paths · S24 dispute/chargeback vocabulary

## Sources
- https://leetcode.com/discuss/interview-question/5832245/ (Stripe University New Grad OA 2024, 2024-09-25; verbatim three parts)
- programhelp 2025-08-08 「Parsing and Filtering Refund/Dispute Data」 (repost of the same three parts)
- https://docs.stripe.com/disputes/how-disputes-work (dispute lifecycle: chargeback is the first stage)
- https://docs.stripe.com/currencies (minor units, zero-decimal currencies)
