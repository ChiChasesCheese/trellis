---
id: hl-loop-priority-problems
node: company.loop
type: qa
step: 7
---
## Q
Headlands 电话面按出现频率应优先练的编码题是哪几道？前四道各有怎样的追问链？

## A
1. **递归求和**：溢出 → 栈深度 → 尾递归 → 并行。
2. **带快照的 queue mean**：O(1) 精确均值 → 快照 → 单写多读。
3. **买卖股票 DP**：一次交易 → 不限次数 → 最多 k 次 → 冷冻期 / 手续费。
4. **合并 K 路有序流**：堆 → 惰性迭代 → 多线程无阻塞。

之后依次是订单簿、ticker 哈希表、寄存器位运算与订单序列 API，最后是你已通过的 job chain OA（面试官可能问你当时怎么写的）。
