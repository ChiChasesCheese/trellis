---
id: s05-threshold-semantics
node: stripe.balances-limits
type: qa
---

## Q
一个 `>` 写成 `>=` 会翻掉多少隐藏测试？英文题面里的 "exceeds"、"at least"、"up to" 分别对应哪个比较符？怎么区分计数阈值和比例阈值，比例阈值为什么必须配一个最小量门槛？

## A
**为什么考**：一个 `>` 写成 `>=`，翻掉的隐藏测试往往不止一个（"恰好等于"是必测的）。

**英文 → 比较符对照表**（背下来）：

| 英文 | 含义 |
|---|---|
| exceeds N / more than N / above N | `> N` |
| at least N / N or more / no fewer than N | `>= N` |
| up to N / at most N / no more than N | `<= N` |
| fewer than N / below N / under N | `< N` |
| reaches N / hits N | `>= N` |
| between A and B（未说明） | **歧义**，默认 `A <= x <= B`，写注释 |

**计数阈值 vs 比例阈值**：有些题用字面量的**形状**区分 ——
`3` 是计数阈值，`0.25` 甚至 `1.0` 是比例阈值。判断方法是**看有没有小数点**，不是看值：

```python
is_ratio = "." in literal            # "1.0" → 比例；"1" → 计数
```

**最小量门槛（min volume）**：比例阈值几乎总是配一个"至少要有 N 笔才判定"的门槛，
否则第一笔就是欺诈的商户会 1/1 = 100% 立刻被封。门槛用 `>=`：
`total >= min_count and fraud * den >= num * total`。

**典型翻车**：
- `total == 0` 时算比例 → 除零；正确答案是"永不判定"。
- 门槛用了 `>` 而不是 `>=`。
- 比例用浮点比较（见 S06 / `04-money-and-rounding.md`）。
