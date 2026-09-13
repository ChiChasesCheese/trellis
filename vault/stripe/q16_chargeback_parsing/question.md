# q16 · Chargeback Parsing — parse network chargeback records, drop corrupted rows, cancel withdrawn disputes

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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s12-time-and-dates|S12 时间与日期]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s24-payments-domain-vocab|S24 领域词汇（支付）]]
