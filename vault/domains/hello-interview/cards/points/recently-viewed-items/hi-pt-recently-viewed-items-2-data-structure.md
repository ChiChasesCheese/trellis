---
id: hi-pt-recently-viewed-items-2-data-structure
node: qb.lld.recently-viewed-items.points
type: qa
step: 3
---
## Q
**"最近浏览"记录 · 数据结构选择**｜必会 · 出自："最近浏览"记录 › 深入 1

"最近浏览"用数组、还是哈希表加双向链表（有序字典）？为什么？

## A
**数组。** 查重和移动是 O(limit)，limit 小可用，但不是 O(1)。
**有序字典。** 查找、摘除、追加、丢队头全是 O(1)，是 LRU 的标准结构。
**手写。** 面试要求自己实现时，就用哈希表加双向链表，哨兵头尾节点简化边界。
