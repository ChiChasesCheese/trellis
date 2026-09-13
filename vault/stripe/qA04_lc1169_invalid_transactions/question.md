# qA04 · LC 1169 Invalid Transactions — amount cap, same-name/other-city within 60 min, reasons, streaming

LC 1169 · *Invalid Transactions* · Medium · https://leetcode.com/problems/invalid-transactions

## The problem (restated)
Each transaction is a string `name,time,amount,city` (time in minutes, amount integer, both ≥ 0).
A transaction is **invalid** when
* its amount is **strictly greater than 1000**, or
* another transaction with the **same name** in a **different city** happened **within 60 minutes
  inclusive** (`|t1 - t2| ≤ 60`) — both transactions of such a pair are invalid.
Return every invalid transaction (LC accepts any order; here: **input order**, duplicates kept).
LC limits: `≤ 1000` transactions, name ≤ 10 lowercase letters, `0 ≤ time ≤ 1000`, `0 ≤ amount ≤ 2000`.

## Context
This is Radar's simplest velocity rule: the same cardholder cannot be in two cities inside an hour, and
a single charge over a cap gets flagged regardless. Stripe's q01/q02 fraud problems grow exactly these
rules into MCC/dispute scoring; the tag data shows LC 1169 is the only Stripe-tagged problem seen in the
last six months, so it is the most likely warm-up to meet in 2026.

## Input (stdin)
```
PART n                        # 1..3
name,time,amount,city         # one transaction per line, input order matters
...
```
Blank lines ignored; spaces around commas tolerated.

## Output
* Part 1: invalid transactions, one per line, in input order (empty output if none).
* Part 2: `transaction | reason ; reason ...` per invalid transaction, input order.
* Part 3: one line per arrival that flags something: `arrival => flagged ; flagged ...`.

## Rules
### Part 1 — LC signature  `invalid_transactions(transactions) -> list[str]`
Group by name; sort each group by `(time, input index)`; slide a window `[t-60, t+60]` keeping a
counter of cities inside it — transaction `i` is city-invalid iff the window holds any transaction whose
city differs from `city_i` (`window_size - count[city_i] > 0`). OR with `amount > 1000`. Output in
input order; identical duplicate strings are each reported (a duplicate never conflicts with itself:
same city).

### Part 2 — reasons  `invalid_reasons(transactions) -> list[Verdict]`
`Verdict(index, transaction, reasons)` (NamedTuple) for each invalid transaction in input order.
`reasons` is a list of strings: `"amount>1000"` first if applicable, then one
`"city:<other transaction string>"` per conflicting transaction, ordered by `(time, input index)` of
the other. A valid transaction produces no Verdict.

### Part 3 — streaming  `TransactionStream(window=60, cap=1000).add(transaction) -> list[str]`
Transactions arrive in **non-decreasing time order** (raise `ValueError` if an arrival goes back in
time). `add` returns the transactions that become invalid **because of this arrival**, in the order
[earlier in-window conflicts by `(time, arrival order)`, then the arrival itself]; each transaction is
reported at most once overall. Per-name history older than `now - window` is evicted so memory is
bounded by the traffic of one window. `flagged` holds all reported transactions in report order.

## Worked examples
```
LC ex1  ["alice,20,800,mtv","alice,50,100,beijing"]  -> both (input order)
LC ex2  ["alice,20,800,mtv","alice,50,1200,mtv"]     -> ["alice,50,1200,mtv"]
LC ex3  ["alice,20,800,mtv","bob,50,1200,mtv"]        -> ["bob,50,1200,mtv"]
Part 2  ex1 -> [Verdict(0,"alice,20,800,mtv",["city:alice,50,100,beijing"]),
                Verdict(1,"alice,50,100,beijing",["city:alice,20,800,mtv"])]
        ["alice,20,1500,mtv","alice,80,100,sf","alice,81,100,la"] ->
          idx0: ["amount>1000", "city:alice,80,100,sf"]        (81-20 = 61 -> la is NOT a conflict)
          idx1: ["city:alice,20,1500,mtv", "city:alice,81,100,la"]
          idx2: ["city:alice,80,100,sf"]
Part 3  add("alice,20,800,mtv")     -> []
        add("alice,50,100,beijing")  -> ["alice,20,800,mtv", "alice,50,100,beijing"]
        add("alice,60,100,mtv")      -> ["alice,60,100,mtv"]      (conflicts with beijing@50; mtv@20 already reported)
        add("bob,70,2000,sf")        -> ["bob,70,2000,sf"]        (amount)
        add("alice,121,5,beijing")   -> []   (beijing@50 same city; mtv@60 is 61 min away -> no conflict)
        add("alice,120,5,la")        -> ValueError (time went backwards)
```
stdin `PART 1` + ex1 → two lines `alice,20,800,mtv` / `alice,50,100,beijing`.

## 关联知识点

- [[a05-hash-sort-record-validation|A05 哈希 + 排序做记录校验]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s12-time-and-dates|S12 时间与日期]]
- [[s16-sliding-window-token-bucket|S16 滑动窗口计数器 / 令牌桶]]
