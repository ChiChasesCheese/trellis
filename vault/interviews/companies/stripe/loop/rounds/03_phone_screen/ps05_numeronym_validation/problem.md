# ps05 · Numeronym validation

**Type:** phone screen (technical) · **Stage:** 45 min technical phone screen · **Last asked:** report undated, page live 2026 (FinalRound); Exponent lists it as a coding-round sample question
**Frequency:** 2 independent mentions (FinalRoundAI question page, Exponent interview guide) · **Confidence:** medium (exact I/O contract not published by either source — reconstructed here from the term's standard definition and Stripe's usual "validate → expand → generate" progression)

## Context
A numeronym is an abbreviation formed from a word by keeping the first and last letter and
replacing the omitted middle letters with their count: `internationalization` → `i18n`
(18 omitted letters), `accessibility` → `a11y`, `kubernetes` → `k8s`. Stripe's internal tooling
(and plenty of open-source projects) use them as short aliases for long identifiers. This
question asks you to validate the *form* of a numeronym, then check it against a real dictionary,
then go the other direction and generate numeronyms for a dictionary — including what happens
when two different words would generate the *same* numeronym.

## Input (stdin, for `main()`)
First line is `PART 1`, `PART 2`, or `PART 3`. Remaining lines are part-specific (below). Blank
lines are ignored everywhere.

## Output
One line per output item, exact case, `main()` prints them newline-joined with a trailing
newline (nothing printed when there is no output).

## Rules

### Part 1 — `is_valid(numeronym: str) -> bool`
A numeronym is valid iff it matches `^[a-z][1-9][0-9]*[a-z]$`:
- exactly one leading lowercase letter, exactly one trailing lowercase letter;
- one or more ASCII digits in between, parsed as the count of omitted letters;
- the digit count must be **≥ 1** and have **no leading zero** (`i018n` is invalid even though
  `18 == 018` numerically — the *string* must not start with `0`);
- case-sensitive: any uppercase letter anywhere makes it invalid.

stdin body: one candidate string per line. Output: `VALID` or `INVALID` per line, in input order.

### Part 2 — dictionary expansion
Given a numeronym and a dictionary, find every dictionary word the numeronym could be short for.
A word `w` matches numeronym `n` iff:
- `w[0] == n[0]` and `w[-1] == n[-1]` (same first/last letter), **and**
- `len(w) == digits(n) + 2` (first letter + omitted middle + last letter).

stdin body: line 1 is the numeronym, remaining lines are dictionary words (one per line, assumed
lowercase `[a-z]+`; a line that isn't `[a-z]+` is skipped as malformed — it can never be a real
word; duplicate lines for the same word count once, as in Part 3). If the numeronym itself is structurally invalid (fails Part 1), there is nothing it could
validly stand for: output `NONE`. Output every matching word, **sorted lexicographically**, one
per line; if there are no matches, output exactly one line: `NONE`.

### Part 3 — generate numeronyms for a dictionary, resolving collisions
For each dictionary word, generate its numeronym:
1. **Words shorter than 3 characters** cannot have an omitted-letter count ≥ 1, so they map to
   **themselves** (no compression possible) — e.g. `ok -> ok`.
2. **Words of length ≥ 3**: the base form is `word[0] + str(len(word) - 2) + word[-1]`.
3. **Collisions**: if two or more dictionary words produce the *same* base form (same first
   letter, same last letter, same length), disambiguate by keeping more of the literal prefix.
   Try prefix length 2, 3, … (form = `word[:p] + str(len(word) - p - 1) + word[-1]`) until every
   word in the colliding group has a distinct form. Prefix length is capped at `len(word) - 2` —
   one below that would drive the digit to 0, which Part 1 forbids.
4. **Irreducible collision**: if two words are still identical once the digit has been driven
   down to 1 (i.e. they differ *only* in the character immediately before the last character —
   e.g. `flap`/`flip`), no valid numeronym (digit ≥ 1) can tell them apart. Every word in that
   group falls back to **itself** (its full literal spelling), same as rule 1.
5. Duplicate lines for the same word collapse into one dictionary entry (a dictionary has no
   duplicate words).

Output: `word -> numeronym` for every distinct word, **sorted by word** (plain string order).

## Worked examples
```
PART 1
i18n
a11y
k8s
i018n
I18n
i18N
i0n
in
i1
ab12cd
->
VALID
VALID
VALID
INVALID   (leading zero: "018")
INVALID   (uppercase first letter)
INVALID   (uppercase last letter)
INVALID   (digit count is 0)
INVALID   (no digit segment at all)
INVALID   (missing trailing letter)
INVALID   (more than one letter before the digits)
```
```
PART 2
i18n
internationalization
international
interpretation
->
internationalization
```
(`internationalization` has length 20 = 18 + 2, starts `i` ends `n`. `international` ends in
`l`, not `n`. `interpretation` has length 14, not 20.)
```
PART 2
k8s
kilobytes
->
NONE
```
(`kilobytes` has length 9, but `k8s` needs length 10 — `kubernetes` would have matched.)
```
PART 3
cart
cost
cyst
few
internationalization
->
cart -> ca1t
cost -> co1t
cyst -> cy1t
few -> f1w
internationalization -> i18n
```
(`cart`/`cost`/`cyst` all base to `c2t` — length 4, starts `c`, ends `t`. Prefix length 2 gives
`ca`/`co`/`cy`, all distinct, so the disambiguated forms are `ca1t`/`co1t`/`cy1t`.)
```
PART 3
flap
flip
->
flap -> flap
flip -> flip
```
(Both base to `f2p`; the only prefix length available before the digit would hit 0 is 2 (`fl`
for both) — still colliding, so both fall back to their literal spelling.)

## Edge cases
- leading zero in the digit segment (`i018n`) — invalid even though the numeric value is fine
- digit count exactly 0 (`i0n`) — invalid, not "empty compression"
- uppercase anywhere — invalid, independent of digit rules
- numeronym with no digits at all, or digits but missing one of the letters
- Part 2: numeronym structurally invalid → `NONE`, not an exception
- Part 2: dictionary word whose length matches but first/last letter doesn't
- Part 2: dictionary line that isn't `[a-z]+` (digits, punctuation, uppercase) — skipped
- Part 2: empty dictionary → `NONE`
- Part 2: the same matching word listed twice → printed once
- Part 3: word length exactly 3 (minimum length that has a numeronym at all)
- Part 3: three-way collision (not just pairwise) resolved at the same prefix length
- Part 3: irreducible collision (differ only in the second-to-last character) → both fall back to
  themselves
- Part 3: duplicate word lines in the dictionary → one output entry
- Part 3: very large dictionary (10^5 words) — algorithm must stay near-linear despite grouping

## Variants seen in the wild
- Exponent's guide frames the same idea as one of several "validate a compact encoding" coding
  practice problems (no published Part 2/3 — the expansion-against-a-dictionary and
  collision-resolution extensions here follow Stripe's usual "validate → apply against real data
  → handle conflicts" three-part shape used across its other phone-screen questions.
- Some retellings ask for the reverse direction only ("given a word, produce its numeronym") with
  no dictionary — that is exactly Part 3 minus the collision step.

## What this tests
skills: S02 parsing/regex discipline · S08 deterministic sort with a stated tie-break ·
S09 exact string formatting (`word -> numeronym`) · S14 string canonicalization / case rules ·
S18 validation and error paths · S19 incremental design (Part 3 reuses Part 1's validity notion)

## Sources
- https://www.finalroundai.com/interview-questions/stripe-tech-numeronyms-validation (FinalRound
  AI, Stripe technical interview question bank, page live as of 2026 scrape)
- Exponent interview guide, "Stripe coding round" sample-question list (numeronym validation
  cited alongside "parse transaction logs into balances" and "implement rate limiters" as
  representative Stripe phone-screen style — no separate URL captured, cited via
  `loop/raw/en_forums.md` §3.3 P16 and skills_matrix.md A-row "Numeronym validation")

## 面试官会怎么追问
1. Part 1 的正则你会怎么手写一个不用 `re` 模块的版本？（练字符扫描，面试官常见的"别用库"追问）
2. 如果同一个 numeronym 在词典里匹配到多个词，你怎么判断哪个是"正确"的那个？（答案：本题定义为返回全部匹配，追问会引导到"如果必须唯一，你需要什么额外信息"）
3. Part 3 的前缀扩展算法最坏情况复杂度是多少？如果一个组里有 10 万个长度相同、只在最后一个字符前一位不同的词会怎样？（引导到我们定义的"不可消歧退化为字面词"规则，以及它的复杂度上界）
4. 如果词典是流式给的（不能一次性读进内存），Part 2/Part 3 怎么改？
5. 大小写不敏感的版本怎么改？如果 numeronym 允许 Unicode 字母呢（`café` 这种）？
6. 如果要求"生成的 numeronym 必须比原词短"（避免 `ok -> ok` 这种退化），你会加什么约束，对现有 API 影响多大？
7. 你会怎么给 Part 1 的校验写一个模糊测试（property-based test）来自动发现我们手写规则里的漏洞？
