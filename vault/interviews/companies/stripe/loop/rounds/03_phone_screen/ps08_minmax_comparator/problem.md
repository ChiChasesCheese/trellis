# ps08 · Min/Max with comparator

**Type:** phone screen (technical) · **Stage:** 45 min technical phone screen, 4 parts · **Last asked:** 2020-01 (Dublin)
**Frequency:** 1 independent source (rampatra's 2020 Dublin phone-screen writeup), naming all
four parts explicitly · **Confidence:** medium (part *shape* is a verbatim transcript — "Part 1
get min; Part 2 min-or-max by parameter; Part 3 comparator; Part 4 ties" — but the concrete
record schema and worked numbers below are this report's reconstruction, since the writeup does
not include sample data; flagged in Open points)

## Context
Stripe's internal tooling constantly needs "give me the extreme record by some field" — the
oldest unresolved dispute, the highest-value transaction today, the payout with the smallest
amount to double-check for rounding. The naive version hardcodes one field. This problem walks
that up to a fully general extreme-finder: first a fixed field, then a parameterized field+mode,
then an arbitrary caller-supplied comparator (so callers can express multi-field tie-breaks that
a single `key` string cannot), and finally what happens when more than one record is tied for
the extreme — a case every one of the first three designs quietly picks one winner for, until
you're asked to list them all.

## Input (payment records)
One record per line: `id,amount,created_at,country`.
- `id`: opaque string identifier, not guaranteed sorted in the input, comparable as a plain
  string (`sorted()` order — `"B" < "a"`, `"user10" < "user2"`).
- `amount`: a decimal string (may be negative, e.g. a refund), parsed as `decimal.Decimal` —
  never `float`, so two records can be exactly equal even after arithmetic elsewhere in a
  pipeline that used this data.
- `created_at`: ISO-8601 timestamp, `Z` or an explicit UTC offset (`2024-01-15T10:00:00Z` or
  `2024-01-15T10:00:00+00:00`), parsed as `datetime.datetime`.
- `country`: a short string, compared lexicographically (not validated as a real ISO country
  code — any string is accepted and sorted as a string).

Blank lines are ignored when parsing records. Records are **not** deduplicated by `id` — if the
same `id` appears on two lines they are two distinct records that happen to share an `id`, and
both are eligible to be counted as "tied" in Part 4.

## Output (stdin protocol for `main()`)
First line is `PART 1`..`PART 4`.
- `PART 1`: remaining lines are records only.
- `PART 2` / `PART 4`: the **next** line is a control line `<key> <mode>` (`key` ∈
  `{amount, created_at, country}`, `mode` ∈ `{min, max}`), then remaining lines are records.
- `PART 3`: remaining lines are records only — the comparator is fixed in `main()` (see Part 3
  below); the pure function `extreme_with` itself takes an arbitrary comparator and is exercised
  directly by the test suite, not only through stdin.

Output is one id per line (`PART 1`/`2`/`3`: exactly one line) or several (`PART 4`: one line per
tied record, ascending by `id`). **Empty record input always prints exactly one line: `NONE`.**

## Rules

### Part 1 — `min_by_amount(records: list[Record]) -> str | None`
Returns the `id` of the record with the smallest `amount`. On a tie, returns the **first** such
record in input order (a fixed, simple tie-break — Part 4 changes this contract, see below).
`None` for an empty list; `part1(lines)` renders that as `["NONE"]`.

### Part 2 — `extreme(records: list[Record], key: str, mode: str) -> str | None`
Generalizes Part 1 to any of the three fields and either direction. `key="amount"` compares
`Decimal`s numerically; `key="created_at"` compares parsed timestamps chronologically;
`key="country"` compares strings lexicographically. `mode="min"`/`"max"` picks the direction. Same
tie-break as Part 1 (first in input order). An unknown `key` or `mode` raises `ValueError`.

### Part 3 — `extreme_with(records: list[Record], comparator: Callable[[Record, Record], int]) -> str | None`
`comparator(a, b)` returns negative if `a` should be considered "smaller" than `b`, positive if
"larger", `0` if equal — the classic C/`qsort`-style contract (also what `functools.cmp_to_key`
expects). `extreme_with` returns the `id` of the record that is the **minimum** under that
ordering — found by a **linear scan** (`O(n)` comparator calls), not by sorting: keep a running
`best`, and replace it only on a strict improvement (`comparator(candidate, best) < 0`), which
also gives the same "first on tie" tie-break as Parts 1–2 for free. To express "max" with a
comparator, the caller passes a comparator with the sign flipped. `main()`'s `PART 3` uses the
canonical comparator `by_amount_then_created_at` (amount ascending, ties broken by `created_at`
ascending) — a genuinely useful comparator that Part 2's single `(key, mode)` interface *cannot*
express, since it needs two fields with independent tie-break order.

### Part 4 — `extreme_all(records: list[Record], key: str, mode: str) -> list[str]`
Same `(key, mode)` interface as Part 2, but returns **every** record tied for the extreme value
— not just the first. Output is the tied ids, **sorted ascending by `id`** (plain string order),
one per line. This is a genuinely different contract from Parts 1–3 (which always resolve ties to
a single winner) — call it out explicitly if asked to reconcile them. Empty input → `["NONE"]`,
same as every other part.

## Worked examples
Records used throughout (fixed order, referenced by this order below):
```
r1,100.00,2024-01-10T10:00:00Z,US
r2,50.00,2024-01-05T09:00:00Z,CA
r3,50.00,2024-01-01T08:00:00Z,DE
r4,200.00,2024-02-01T00:00:00Z,US
```

Part 1: `min_by_amount` → **r2** (amount 50.00 ties with r3, r2 comes first in input order).

Part 2:
- `extreme(key=amount, mode=max)` → **r4** (200.00, the largest amount)
- `extreme(key=created_at, mode=min)` → **r3** (2024-01-01, the earliest timestamp)
- `extreme(key=country, mode=min)` → **r2** (`"CA"` < `"DE"` < `"US"` lexicographically)
- `extreme(key=country, mode=max)` → **r1** (`"US"` ties between r1 and r4; r1 comes first)

Part 3: `extreme_with(by_amount_then_created_at)` → **r3**. r2 and r3 tie on amount (50.00), so
the comparator falls through to `created_at`; r3's `2024-01-01` is earlier than r2's `2024-01-05`,
so r3 wins — **a different answer than Part 1's `min_by_amount`**, which only ever looks at
`amount` and therefore picks r2 on that same tie. This divergence is the whole point of Part 3:
a comparator can express an ordering a single `key` cannot.

Part 4:
- `extreme_all(key=amount, mode=min)` → **r2, r3** (both 50.00, sorted by id ascending)
- `extreme_all(key=country, mode=max)` → **r1, r4** (both `"US"`, sorted by id ascending)

Empty input, any part → `NONE`.

## Edge cases hidden tests are known to target
- empty record list: every part prints exactly `NONE`, never an empty output / exception
- single record: it is trivially the min and the max
- negative amounts (refunds) compare correctly against positive ones
- exact-tie boundaries: two records with the identical `Decimal` amount, identical `created_at`
  (to the parsed precision), or identical `country` string
- duplicate `id`s across two distinct records — both appear in a Part 4 tie list if both are tied
  (id is not deduplicated); if that duplicate id is itself the sole record, both are the answer
- `id` sort in Part 4 is **plain string order**, not case-insensitive or numeric-aware
  (`"B" < "a"`, `"user10" < "user2"`)
- `created_at` accepts both `Z` and an explicit `+00:00`/other offset and compares them correctly
  as instants (a `Z` timestamp and an equal-instant offset timestamp are equal for tie purposes)
- unknown `key` or `mode` string → `ValueError`, not a silent wrong answer
- `extreme_with` with a comparator that only distinguishes on a field *other than* `amount` (e.g.
  `country` only) still runs correctly — the function must not assume `amount` is involved
- large input (10^5 records) must complete well inside the perf budget with a single linear scan,
  not an `O(n log n)` sort when only the extreme is needed

## Variants seen in the wild
- rampatra's writeup does not name the record schema or field types — this report picked
  `amount`/`created_at`/`country` as a concrete, Stripe-flavored instantiation of "some fields to
  extreme over"; a real transcript might use different field names or a different record shape
  (e.g. plain integers) while keeping the same four-part progression.
- A natural follow-up not in the original four parts: extend `extreme_with` itself to support
  ties (return all records the comparator considers equal to the winner) instead of adding a
  separate `extreme_all` — see 面试官会怎么追问 item 7 below.

## What this tests
skills: S03 modeling records as a small typed structure (not raw CSV lines) · S08 deterministic
ordering with an explicit, stated tie-break that changes on purpose between Part 1-3 and Part 4 ·
S12 timestamp parsing/comparison · S19 incremental design (Part 4 reuses Part 2's `(key, mode)`
interface; Part 3 stands apart as the more general mechanism) · S21 stdlib fluency (`Decimal`,
`datetime.fromisoformat`, `functools.cmp_to_key` vs. a hand-rolled linear scan)

## Sources
- rampatra, 2020-01, Dublin Stripe phone-screen writeup (P14 in `loop/raw/en_forums.md` §3.3):
  "Part 1: take the min value record; Part 2: return min or max based on a parameter; Part 3: use
  a comparator; Part 4: handle ties."

## 面试官会怎么追问
1. "Why does `extreme_with` do a linear scan instead of `min(records, key=functools.cmp_to_key(comparator))`?"
   (answer: same asymptotic result for finding *one* extreme, but the linear scan is `O(n)`
   comparator calls vs. `cmp_to_key`-based `min`'s `O(n)` as well in CPython's implementation —
   the real reason to prefer the hand-rolled scan here is that it makes the "first on tie" rule
   explicit and auditable in one `if` condition, and it doesn't require wrapping every record in
   a `cmp_to_key`-produced object; if you needed the *sorted* order for something else, sorting
   would be justified, but for a single extreme it's unnecessary work)
2. "What invariants does `comparator` need to satisfy for `extreme_with` to be correct?" (answer:
   anti-symmetry — `comparator(a,b)` and `comparator(b,a)` must have opposite signs (or both
   zero) — and transitivity; a comparator that violates these (e.g. compares by `id % 3` in a way
   that cycles) can make the "linear scan keeps the best" strategy return a non-deterministic or
   simply wrong answer depending on record order, which sorting would silently do too)
3. "Extend `extreme` to take a *list* of `(key, mode)` pairs for multi-key sort without writing a
   full custom comparator." (answer: build a tuple key per record —
   `tuple(extract(key, mode) for key, mode in fields)`, with `mode="max"` fields negated/reversed
   — and compare tuples; this is the natural middle ground between `extreme`'s single key and
   `extreme_with`'s fully general comparator)
4. "If records arrive as a live stream instead of a batch, how do you maintain the running
   extreme without recomputing from scratch?" (answer: for a single running min/max, keep one
   running `best` and update in `O(1)` per new record with the same comparator; for Part 4's
   "all tied" semantics under a stream, you additionally need to keep the full tied set and
   possibly evict members if a strictly better record arrives)
5. "Why `Decimal` instead of `float` for `amount`?" (answer: float equality/ordering on decimal
   literals like `0.1 + 0.2` is unreliable, and if this extreme-finder later feeds into anything
   that sums or rounds money, float accumulation drifts — `Decimal` matches the rest of the repo's
   money convention (see CONVENTIONS.md) even though this problem itself does no arithmetic)
6. "How would you make Part 4 support ties under a *comparator*, not just a `(key, mode)` pair,
   consolidating it with Part 3?" (answer: replace the equality check `value == extreme_value`
   with `comparator(record, best) == 0` after finding `best` via `extreme_with`'s scan — the
   function signature would become `extreme_all_with(records, comparator) -> list[str]`, and
   `extreme_all(records, key, mode)` could become a thin wrapper around it, mirroring how Part 4
   currently wraps Part 2's interface)

## Open points
- The only verified fact from the source is the four-part shape and its one-sentence description
  per part; the record schema, field names, exact tie-break rule, and all worked numbers are this
  report's reconstruction. If a transcript with sample I/O surfaces, reconcile it against the
  worked examples above.
