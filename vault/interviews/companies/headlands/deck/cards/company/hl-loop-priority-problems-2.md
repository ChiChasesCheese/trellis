---
id: hl-loop-priority-problems-2
node: company.loop
type: qa
step: 8
---
## Q
Headlands 电话面的订单簿、ticker 哈希表这两类题，典型追问链是什么？排在后面的还有哪几类？

## A
- **订单簿**：下单 / 撤单 / 最优价 → 撮合 → **零分配**（zero allocation）。
- **ticker 哈希表**：开放寻址 → 把 ticker 压进 **64 位整数** → 完美哈希。
- 后面的：寄存器位运算、订单序列 API（树状数组）。
- 最后一类是 job chain：你过了的那道 OA，面试官可能问你当时怎么写的。

追问的方向都落在性能直觉上：分配、缓存、整数化。
