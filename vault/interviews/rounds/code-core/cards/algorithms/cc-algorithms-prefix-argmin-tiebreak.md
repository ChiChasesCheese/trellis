---
id: cc-algorithms-prefix-argmin-tiebreak
node: algorithms.prefix
type: qa
---
## Q
Several split points achieve the same minimum. The spec says "the earliest". Which comparison — and what if it said "the latest"?

## A
**Strict `<` keeps the first optimum; `<=` keeps the last.**

- Scanning left to right, `if cur < best:` never replaces on a tie → the earliest wins. `if cur <= best:` replaces on every tie → the latest wins. One character, one whole hidden-test group.
- Same rule for maxima: `>` keeps the earliest maximum, `>=` the latest.
- `min(range(n), key=f)` returns the earliest minimum — but only if `f` is the *entire* key. A second criterion needs an explicit tuple: `min(range(n), key=lambda j: (cost[j], j))`.
- When the reported answer is an index rather than a value, state the tie rule in a comment; readers cannot infer it from `<`, and neither can you three parts later.

## Q zh
多个分割点取到相同的最小值。spec 说取「最早的」。用哪个比较符 —— 如果它说「最晚的」呢？

## A zh
**严格 `<` 保留第一个最优解；`<=` 保留最后一个。**

- 从左向右扫描时，`if cur < best:` 在并列时从不替换 → 最早的胜出。`if cur <= best:` 每次并列都替换 → 最晚的胜出。一个字符，一整组隐藏测试。
- 最大值同理：`>` 保留最早的最大值，`>=` 保留最晚的。
- `min(range(n), key=f)` 返回最早的最小值 —— 但前提是 `f` 是*完整*的 key。有第二判据时需要显式 tuple：`min(range(n), key=lambda j: (cost[j], j))`。
- 当报告的答案是下标而非值时，把并列规则写进注释；读者无法从 `<` 推断出来，三个 part 之后的你也一样。
