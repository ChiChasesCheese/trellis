---
id: s01-read-full-spec-first
node: stripe.solving
type: qa
---

## Q
为什么 Stripe OA 题不能上来就闷头实现 Part 1？题面出现哪些信号说明必须先读完整份规格、为 Part N+1 预留设计空间？

## A
**为什么考**：这类题的每个 part 都是在同一个程序上继续加需求。上来就闷头实现 Part 1，
到 Part 4 发现状态形状不对，只能重写 —— 时间就是这么没的。

**怎么识别**：题面出现 "Part 1 / Part 2 / ..."、"the following parts build on this"、
或者输入第一行是 `PART n`。

**标准做法**：见 `01-solving-framework.md` §2 的"倒着设计三问"。核心一句：
**保留原始记录，聚合值从它派生**，因为撤销类需求必须能回头找到那一条。

**典型翻车**：Part 2 只存 `count`，Part 4 要求"撤销某笔交易"→ 不知道该减哪个计数器。
