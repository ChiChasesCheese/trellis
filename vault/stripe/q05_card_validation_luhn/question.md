# q05 · Payment Card Validation — Luhn, network detection, redacted `*` digits, corrupted `?` cards

## Context
Stripe processes cards across several networks. A card number's shape identifies the network
(length + BIN prefix) and its last digit is a Luhn check digit, so a card is only "valid" if
both agree. Real-world twists: card numbers arrive **redacted** (`*` in place of digits, as in a
receipt or a log) and you must count how many real cards could hide behind the mask; or they
arrive **corrupted** by exactly one typo (one wrong digit, or two adjacent digits swapped — the
two errors Luhn was designed to catch) and you must list every valid original.

## Networks and Luhn
| network | length | prefix |
|---|---|---|
| VISA | 16 | `4` |
| MASTERCARD | 16 | `51`–`55` |
| AMEX | 15 | `34` or `37` |

Luhn: starting from the rightmost digit and moving left, double every **second** digit (the
2nd, 4th, … from the right); if a doubled value is > 9 subtract 9; sum every digit; the card is
valid iff the sum is divisible by 10.

## Input (stdin)
Two accepted protocols (both tested):
1. `PART n` (n ∈ 1..4) on the first line, then **one card per line**.
2. HackerRank form: first line `Q`, then `Q` lines `P1 card`, `P2 card`, `P3 redacted`,
   `P4 corrupted?` mixing parts freely; each line is answered in order.
Blank lines are ignored. Cards are digit strings (plus `*` in Part 3 and a trailing `?` in Part 4).

## Output
One block per query, in query order, each block being the lines listed under its part below.
A Part 3 / Part 4 query with no result prints **nothing**.

## Rules
### Part 1 — basic VISA validation
Input is a 16-digit number starting with `4`. Print `VISA` if the Luhn checksum passes, else
`INVALID_CHECKSUM`.

### Part 2 — multi-network validation
Input is a 15- or 16-digit number (any digits). Decide the network by **length + prefix first**:
no match → `UNKNOWN_NETWORK` (regardless of checksum). Otherwise print the network name if Luhn
passes, else `INVALID_CHECKSUM`.

### Part 3 — redacted digits
Input contains one to five `*`, each hiding exactly one digit. Count, **per network**, the
completions that are valid cards (network shape + Luhn). Print one line per network with a
non-zero count, `NETWORK,count`, in alphabetical network order (`AMEX` < `MASTERCARD` < `VISA`).
The prefix may be masked (`**2424242424242` → the 15-digit length makes AMEX the only candidate;
`34…` and `37…` are both tried).

### Part 4 — corrupted card (exactly one error)
Input ends with `?`; the observed digits contain **exactly one** error: either one digit was
changed, or two adjacent digits were swapped. Print every valid original (any network, same
length) as `card_number,NETWORK`, **ascending numeric order, deduplicated** (a change and a swap
can produce the same candidate). The observed number itself is never an answer.

## Worked examples
Example 1 (Part 1):
```
PART 1
4532015112830366
4242424242424243
4242424242424242
```
→ `VISA`, `INVALID_CHECKSUM`, `VISA`.

Example 2 (Part 2, verbatim from the repo sample):
```
PART 2
5482334509943
4425233430109994
562523343010901
5555555555554444
378282246310005
```
→ `UNKNOWN_NETWORK` (13 digits), `INVALID_CHECKSUM` (VISA shape, Luhn fails), `UNKNOWN_NETWORK`
(15 digits, prefix 56), `MASTERCARD`, `AMEX`.

Example 3 (Part 3):
```
PART 3
4242424242424*42
3*8282246310005
**2424242424242
5*5555555555444*
```
→ `VISA,1` / `AMEX,1` / `AMEX,1` / `MASTERCARD,5` (second digit 1–5 each fixes one check digit).

Example 4 (Part 4, verbatim from the repo sample; 16 originals, all VISA):
```
PART 4
4532015112830367?
```
→
```
4432015112830367,VISA
4523015112830367,VISA
4531015112830367,VISA
4532005112830367,VISA
4532010112830367,VISA
4532015012830367,VISA
4532015111830367,VISA
4532015112330367,VISA
4532015112820367,VISA
4532015112830267,VISA
4532015112830317,VISA
4532015112830366,VISA
4532015112839367,VISA
4532015152830367,VISA
4532915112830367,VISA
4572015112830367,VISA
```
(Single-digit changes plus adjacent swaps such as `32→23` giving `4523…`.)

Example 5 (Part 4 crossing networks): `5242424242424242?` → `4242424242424242,VISA` first
(numerically smallest), then 14 `MASTERCARD` originals `5242424242424249`, `5242424242424272`,
`5242424242424942`, … `5272424242424242`.

Example 6 (HackerRank mixed protocol):
```
3
P1 4242424242424241
P2 4111111111111111
P3 4242424242424*4*
```
→ `INVALID_CHECKSUM`, `VISA`, `VISA,10`.

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s14-string-normalization|S14 字符串归一化 / 规范化]]
- [[s15-masked-input-combinatorics|S15 掩码输入上的小规模组合]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
