---
id: hl-javaq-f-q29-main
node: java-questions.f-concurrency
type: qa
step: 14
---
## Q
`HashMap` 内部是怎么工作的？讲扩容、冲突、树化，以及为什么容量取 2 的幂。
How does `HashMap` work internally? Resizing, collisions, treeification, why is the capacity a power of two?

## A
一句话：**数组 + 链表 / 红黑树**。`index = (n-1) & (h ^ (h >>> 16))`；**负载因子 0.75** 触发翻倍扩容；同一桶链表 ≥ 8 且表容量 ≥ 64 时转红黑树（≤ 6 退回）。

- **容量取 2 的幂**：用位与 `hash & (n-1)` 代替取模，更快；扩容时每个节点要么留在原位置、要么移到 `原位置 + 旧容量`（看新增的一位），不用重新算 hash。
- **spread**：高 16 位异或进低 16 位，否则只用低位，高位信息浪费。
- put 流程：桶空 → 放 `Node`；非空 → 比较 hash 与 `equals`，相同覆盖，否则挂链尾。
