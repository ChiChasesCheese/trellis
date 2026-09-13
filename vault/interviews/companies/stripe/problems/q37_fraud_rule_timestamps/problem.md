# q37 · Fraud Rule Timestamps — authorization requests vs rule effective time

**Type:** phone screen (live coding, ~35 min) · **Stage:** Stripe phone interview · **Last asked:** 2021-06 (adonais0 write-up)
**Frequency:** 1 independent source (adonais0.github.io interview write-up) · **Confidence:** medium

## Context
Stripe Radar lets a business write rules such as "block any authorization where the merchant is
`bobs_burgers`". Rules are edited over time, so every rule version has an **effective-from**
timestamp; a rule created on Tuesday must not retroactively flag Monday's authorizations, and a
rule that was later relaxed must be applied in the version that was live at the moment of each
request. The task: replay a batch of authorization requests against the rule history and print
each decision.

## Input (stdin)
One record per line, either kind, in any order (one accumulating program; no `PART` line):
```
RULE,<name>,<effective_from>,<condition>                 (Parts 1–2)
RULE,<name>,<effective_from>,<effective_to>,<condition>  (Part 3; 5 fields)
AUTH,<id>,<timestamp>,<merchant>,<amount>
```
Timestamps are non-negative integers; `amount` is an integer in minor units. A condition is
`<field><op><value>` with `field ∈ {merchant, amount}`, `op ∈ {=, !=, >, >=, <, <=}` (numeric
ops only for `amount`), or the literal `none` (rule switched off from that version on).

## Output
One line per `AUTH`, `timestamp,id,amount,DECISION` with `DECISION ∈ {APPROVE, REJECT}`, sorted
by `(timestamp, id)` — plain string order for `id`.

## Rules
### Part 1 — one rule, effective-from
A request is `REJECT` if a rule whose `effective_from ≤ timestamp` matches it (`==` applies).
Requests before the rule's effective time are `APPROVE` even if they match — no retroactive
flagging.

### Part 2 — several rules and rule versions
Different names are independent: **any** in-force matching rule rejects. Lines with the same
name are **versions** of one rule; the version in force at `t` is the one with the **largest
`effective_from ≤ t`** (tie: the later line). Only that version is evaluated. Condition `none`
switches the rule off from that version's effective time.

### Part 3 — expiry (`effective_to`)
A 5-field `RULE` line is in force for `effective_from ≤ t < effective_to` (**end exclusive**).
Version selection is unchanged: if the selected version has expired at `t` the rule is off —
it does **not** fall back to an older version.

### Part 4 — out-of-order arrivals (reconstructed)
`RULE` and `AUTH` lines may appear in any order in the file; versions are ordered by
`effective_from`, never by line position; output is sorted by `(timestamp, id)`.

## Worked examples
```
RULE,burgers,100,merchant=bobs_burgers
AUTH,a1,50,bobs_burgers,1200
AUTH,a2,100,bobs_burgers,1200
AUTH,a3,150,alice_cafe,1200
->
50,a1,1200,APPROVE
100,a2,1200,REJECT
150,a3,1200,APPROVE
```
```
RULE,big,0,amount>1000
RULE,big,300,amount>5000
RULE,big,400,none
RULE,burgers,100,merchant=bobs_burgers
AUTH,b1,250,shop,2000
AUTH,b2,300,shop,2000
AUTH,b3,300,shop,6000
AUTH,b4,400,shop,6000
AUTH,b5,400,bobs_burgers,1
->
250,b1,2000,REJECT
300,b2,2000,APPROVE
300,b3,6000,REJECT
400,b4,6000,APPROVE
400,b5,1,REJECT
```
```
RULE,promo,100,200,merchant=bobs_burgers
AUTH,c1,199,bobs_burgers,10
AUTH,c2,200,bobs_burgers,10
->
199,c1,10,REJECT
200,c2,10,APPROVE
```
```
AUTH,d2,10,shop,900
RULE,late,0,amount>=900
AUTH,d1,10,shop,899
->
10,d1,899,APPROVE
10,d2,900,REJECT
```

## Edge cases hidden tests are known to target
- `timestamp == effective_from` → rule applies; `timestamp == effective_to` → expired
- a request matching an older version but not the version in force (and vice versa)
- an expired newer version does not revive an older one
- `none` version; `!=` and `<=` operators; `amount` compared numerically (`900 > 1000` false)
- two rules where only the second matches; rules declared after the requests in the file
- output tie-break: same timestamp → id string order (`b2` < `b3`, `a10` < `a2`)
- no rules at all → everything `APPROVE`; no requests → no output

## Variants seen in the wild
- The write-up phrases the rule as prose ("any Authorization Request with merchant of
  `bobs_burgers` is fraudulent") — the condition mini-language here is a reconstruction.
- Distinct from q01/q12 (Radar ALLOW/BLOCK rules with a full expression language): this one is
  about **time**, not expression parsing.

## What this tests
skills: S02 parsing · S03 domain modeling · S05 strict vs non-strict comparisons · S08 deterministic sort · S10 event streams · S12 time handling · S13 inclusive/exclusive boundaries

## Sources
- https://adonais0.github.io/20210603/interview-stripe/ (phone screen write-up, 2021-06-03)
