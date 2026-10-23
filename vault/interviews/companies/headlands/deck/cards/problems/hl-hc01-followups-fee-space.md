---
id: hl-hc01-followups-fee-space
node: problems.hc01-stock-trading-dp
type: qa
step: 20
---
## Q
如果手续费改成买入时扣而不是卖出时扣，结果有区别吗？不限次数 + 冷却的纯利润数字空间能降到 O(1) 吗？

## A
**手续费位置**：不改引擎，`sell = oldHold + p` 去掉 fee，`buy = free[src] - p - fee`。结果**相同**：每笔**完成**的交易恰好扣一次，最终答案只看 `free` / `cool`（仍持有的不计入）；`plan` 的净利润公式也不变。

**O(1) 空间**（LC 309 标准解）：三个变量，每天都用昨天的值，先存旧值再更新：
```
free' = max(free, cool)
hold' = max(hold, free - p)
cool' = hold + p
```
答案 `max(free, cool)`。

对应的自测：`[2,1,4,5,2,9,7]`，k=2：1 买 5 卖赚 4、2 买 9 卖赚 7，`free[2] = 11`（1→9 一笔赚 8，不如两笔）。

另一个要会答的：`j` 改成从小到大，纯 Part 3 答案不变（同天同价「卖了又买」现金不变），加冷却就错（买入读到含「昨天卖出、今天冷却结束」的钱）。
