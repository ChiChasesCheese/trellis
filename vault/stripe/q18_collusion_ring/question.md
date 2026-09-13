# q18 · Six Degrees of Collusion — fraud rings from shared identifiers

## Context
Stripe Radar looks for *collusion rings*: sets of customer accounts that share devices, cards
or contact details. Two accounts that share any identifier are directly linked; links are
transitive (A shares a device with B, B shares a card with C → A, B, C are one ring). Given
transaction records, you find who is directly linked to a suspect, measure the suspect's ring,
score each ring's risk, and decide whether to block.

## Input (stdin)
First line `PART n` (1–4). Records follow, one per line, blank lines ignored. Fields are
`:`-separated and trimmed. A customer may appear on many records. Up to 10^5 records.

* Parts 1–2: `customer:device_id[:credit_card_id]` — any number of identifier fields ≥ 1
  (`A:d1`, `A:d1:123`). Every non-customer field is an identifier; fields at the **same
  position** are compared (a device never links to a card). Empty fields link nothing.
* Part 3: `customer:device_id:credit_card_id:risk_factor` (`risk_factor` integer 0–100).
* Part 4: `user_id,name,email,company` (comma-separated, §24 record-linking variant).

Second line (after `PART n`): Part 1 `<target>`; Part 2 `<target> <K>`; Part 4 `<target> <threshold>`.

## Output
* Part 1: directly linked customers, **sorted, one per line**, `NONE` if none.
* Part 2: `<ring size> BLOCK` or `<ring size> ALLOW`.
* Part 3: one line per ring, `<members sorted, comma-joined> <risk>` (risk two decimals).
* Part 4: users linked to the target with confidence ≥ threshold, sorted, `NONE` if none.

## Rules
### Part 1 — direct links
`direct_links(records, target)` → sorted list of customers (≠ target, deduped) that share at
least one identifier value with the target **at the same field position**. Unknown target → `[]`.

### Part 2 — fraud ring size & block decision
`groups(records)` → the connected components of the link graph (union-find / BFS): customers
sharing an identifier are in the same group, transitively. `ring_size(records, target)` = size of
the target's component **including the target** (a customer with no links has ring size 1;
unknown target → 0). `largest_ring(records)` = max component size (0 for no records).
`should_block(records, target, k)` = `ring_size ≥ k` (non-strict).

### Part 3 — ring risk scoring
Each record now carries a `risk_factor`. A customer's risk = the risk on its **last** record
(records are chronological). Ring risk = **mean risk of the members after removing members
with risk 0** (they are treated as verified / not part of the scoring); a ring whose members all
have risk 0 scores `0`. `ring_risks(records)` returns one score per ring in order of the ring's
**first-appearing customer**.

### Part 4 — weighted link confidence (record-linking variant, phone screen)
Records `user_id,name,email,company`. Two users are linked with confidence
`Σ weight(field)` over the fields where both values are non-empty and equal
case-insensitively; default weights `name 0.2, email 0.5, company 0.3`, threshold `0.5`.
`weighted_links(records, target, weights=..., threshold=0.5)` → sorted user ids with
confidence ≥ threshold (non-strict; compare in integer thousandths so 0.2 + 0.3 ≥ 0.5 holds).

## Worked examples
Example 1 (LeetCode Q1 — groups):
```
PART 2                       records: A:d1  B:d2  C:d3  D:d2  B:d3
B 3                          -> groups {A}, {B,C,D}  -> "3 BLOCK"    (ring of B = 3 ≥ K=3)
```
Example 2 (LeetCode Q2 — largest ring; device OR card links):
```
records: A:d1:123  B:d2:456  C:d3:123  D:d2:789  E:d2:999
-> groups {A,C} (card 123), {B,D,E} (device d2) -> largest_ring = 3
PART 1 / target A -> C          PART 2 / "A 3" -> "2 ALLOW"
```
Example 3 (LeetCode Q3 — ring risk, zero-risk members dropped):
```
PART 3
A:d1:123:90  B:d2:456:50  C:d3:123:0  D:d2:789:100  E:d2:999:30
-> ring_risks = [90, 60]        stdout:   A,C 90.00
                                          B,D,E 60.00
```
Example 4 (Part 4 — linkjob weights):
```
PART 4
u1 0.5
u1,alice smith,alice@x.com,acme
u2,alice smith,other@x.com,acme      (name .2 + company .3 = .5  -> linked)
u3,bob,alice@x.com,zzz               (email .5                 -> linked)
u4,alice smith,,                     (name .2                  -> not linked)
-> u2
   u3
```

## 关联知识点

- [[a16-union-find-components|A16 并查集 / 连通分量]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
