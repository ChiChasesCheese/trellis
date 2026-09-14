---
id: s04-group-then-aggregate
node: stripe.modeling
type: qa
---

## Q
商户评分类题目最常见的错因是什么？题面出现 "a merchant with more than one X gets a bonus"、"apply the penalty once per account" 这类描述时，为什么不能在遍历交易的循环里直接加分？

## A
**为什么考**：商户评分类题目的头号错因 —— 加分项被按行重复计算。

**怎么识别**：题面出现 "a merchant with more than one X gets a bonus"、
"apply the penalty once per account"、"repeat customers"。

**标准做法**：先分组，再对**组**应用规则：

```python
by_merchant = defaultdict(list)
for tx in txs:
    by_merchant[tx.merchant].append(tx)

for m, group in by_merchant.items():
    score = sum(base(t) for t in group)          # 每行一次的部分
    if len({t.customer for t in group}) < len(group):
        score += REPEAT_BONUS                     # ← 每组一次，只加一遍
```

**判断准则**：把规则的主语读出来。主语是"这笔交易"→ 每行一次；
主语是"这个商户 / 这个用户 / 这一天"→ 每组一次。

**典型翻车**：在遍历交易的循环里写 `if seen_before: score += BONUS`，
于是有 5 笔重复交易就加了 5 次。
