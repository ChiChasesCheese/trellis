# q06 · Atlas Company Name Availability — normalize, register, reclaim

## Context
Stripe Atlas incorporates companies in Delaware, where a name must be "distinguishable upon the
records" — small differences in case, punctuation, entity suffix (`Inc.`, `LLC`) or a leading
article do not make a name distinct. This exercise models the availability check: every name is
reduced to a canonical form and compared against the canonical forms of registered names. Later
parts turn the check into a persistent registry (an accepted name is taken from then on) and add
dissolution (`RECLAIM`), which frees a name — but only when the original registrant asks.

## Normalization (applies to registered and proposed names alike)
1. lowercase
2. `&` and `,` become spaces
3. split on whitespace (this collapses runs of spaces)
4. remove trailing entity-suffix tokens **repeatedly** while the last token is one of
   `inc` `inc.` `corp` `corp.` `llc` `l.l.c.` `llc.` (case-insensitive)
5. drop a leading article `the` / `a` / `an` (one token, once)
6. drop every `and` token **except when it is the first token** (after step 5)
7. in the remaining tokens, any other punctuation (`.`, `-`, `'`, `/`, …) becomes a space and the
   tokens are re-split *(reconstructed: sources only spell out `&` and `,`; flag
   `strip_punctuation=False` disables this step)*
8. join with single spaces. **Empty result → the name is Not Available** (and never registered).

`The Llama, Inc.` → `llama`; `Llama And Friend, Inc.` → `llama friend`; `And Llama Friend` →
`and llama friend` (distinct); ` &Co, LLC.` → `co`; `The Inc.` → `` (unavailable).

## Input (stdin)
First line `PART n` (n ∈ 1..3; optional, default 3). Then an optional block
**REGISTERED**

| 格式 | 说明 |
|---|---|
| `<one already-registered name per line>` | (no account — nobody can reclaim these) |

**REQUESTS**
followed by one request per line. Without the headers every line is a request. Blank lines are
ignored; leading/trailing whitespace of a line is stripped, interior spacing is significant only
up to normalization. Request forms:
- `account_id|proposed_name` — availability request (Parts 1–3)
- `RECLAIM,account_id,original_proposed_name` — dissolution (Part 3; the name may itself contain
  commas — split on the first two commas only)

## Output
One line per availability request, in input order: `account_id|Name Available` or
`account_id|Name Not Available`. `RECLAIM` lines print nothing.

## Rules
### Part 1 — basic availability check (stateless)
A proposed name is available iff its normalized form is non-empty and not equal to the normalized
form of any name in the `REGISTERED` block. Requests do not affect each other.
*(The repo statement already says "register it immediately"; that behaviour is Part 2. Use
`part1(lines, persist=True)` if a grader expects Part 1 to register.)*

### Part 2 — persistent registration
Part 1, plus: an **accepted** name is registered to the requesting account immediately and is
Not Available for every later request — from any account, **including the account that
registered it** (re-submitting your own name is Not Available). Rejected requests register nothing.

### Part 3 — reclamation
`RECLAIM,account_id,original_proposed_name`: if the normalized name is registered **and its
registrant is `account_id`**, remove it (the name becomes available to anyone, including the
former owner). Otherwise ignore the line: wrong account, name not registered, or a name from the
`REGISTERED` block (which has no registrant). Reclaiming never prints anything.

## Worked examples
Example 1 (Part 1 — stateless):
```
PART 1
REGISTERED
Llama, Inc.
Acme & Sons Corp.
REQUESTS
1|The Llama
2|acme and sons
3|Llama Friends
4|Llama Friends
5|The Inc.
```
→ `1|Name Not Available`, `2|Name Not Available` (`acme sons` both), `3|Name Available`,
`4|Name Available` (Part 1 does not register), `5|Name Not Available` (normalizes to empty).

Example 2 (Part 2 — persistent):
```
PART 2
1|Llama, Inc.
2|The Llama
3|Llama And Friend, Inc.
4|And Llama Friend, Inc.
5|Llama,  Inc.
6| &Co, LLC.
1|LLAMA
```
→ `1|Name Available`, `2|Name Not Available`, `3|Name Available`, `4|Name Available`,
`5|Name Not Available`, `6|Name Available`, `1|Name Not Available` (own name, still taken).

Example 3 (Part 3 — verbatim repo sample):
```
PART 3
1|Llama, Inc.
2|The Llama
3|Llama And Friend, Inc.
4|And Llama Friend, Inc.
5|Llama,  Inc.
6| &Co, LLC.
RECLAIM,1,Llama, Inc.
7|Llama
8|Co
9|and co
RECLAIM,6, &Co, LLC.
10|Co
```
→
```
1|Name Available
2|Name Not Available
3|Name Available
4|Name Available
5|Name Not Available
6|Name Available
7|Name Available
8|Name Not Available
9|Name Available
10|Name Available
```
(after `RECLAIM,1` the name `llama` is free so 7 gets it; 8 collides with 6's `co`; 9 keeps its
leading `and`; after `RECLAIM,6` 10 gets `co`.)

Example 4 (Part 3 — reclaim by the wrong account is ignored):
```
PART 3
1|Acme
RECLAIM,2,Acme
2|ACME
RECLAIM,1,acme inc
2|Acme
```
→ `1|Name Available`, `2|Name Not Available`, `2|Name Available` (reclaim by the registrant
matched on the normalized form `acme`; the former owner's name is free for anyone).

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s14-string-normalization|S14 字符串归一化 / 规范化]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
