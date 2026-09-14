---
id: cc-toolbox-hash-counter
node: toolbox.hash
type: qa
---
## Q
You need per-merchant transaction counts, then the three largest. What does `Counter` give you, and where must you not trust it?

## A
**`Counter` is a dict with `+= 1` on missing keys plus multiset arithmetic**: `c1 + c2`, `c1 - c2` (drops non-positives), `c.total()`, `Counter(iterable)` as a one-line group-count.

- `most_common(k)` sorts by count descending and **breaks ties in insertion order** — an implementation detail, not a specified tie-break. If ties matter, sort explicitly: `sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))` ([[cc-output-ordering-total-order]]).
- `c[missing]` returns 0 **without inserting**, which makes probing safe — unlike `defaultdict`.
- `Counter(a) - Counter(b)` answers "what is still missing" for covering problems; `&` gives the per-key minimum.
- Negative counts are legal and `most_common` will happily rank them; if a count can go negative, that is a modelling signal, not a `Counter` feature to lean on.

## Q zh
你需要按商户统计交易数，然后取最大的三个。`Counter` 提供了什么，哪里不能信它？

## A zh
**`Counter` 是一个对缺失 key 支持 `+= 1` 的 dict，外加多重集合运算**：`c1 + c2`、`c1 - c2`（丢掉非正值）、`c.total()`，以及一行完成分组计数的 `Counter(iterable)`。

- `most_common(k)` 按计数降序排序，并且**并列时按插入顺序**决出 —— 这是实现细节，不是被规定的 tie-break。如果并列重要，就显式排序：`sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))`（[[cc-output-ordering-total-order]]）。
- `c[missing]` 返回 0 且**不插入**，所以探测是安全的 —— 这点与 `defaultdict` 不同。
- `Counter(a) - Counter(b)` 回答覆盖类问题的「还缺什么」；`&` 给出每个 key 的最小值。
- 负计数是合法的，`most_common` 也会照样排它们；如果某个计数可能变负，那是建模信号，而不是可以依赖的 `Counter` 特性。
