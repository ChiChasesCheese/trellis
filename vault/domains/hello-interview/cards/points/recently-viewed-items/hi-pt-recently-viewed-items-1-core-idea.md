---
id: hi-pt-recently-viewed-items-1-core-idea
node: qb.lld.recently-viewed-items.points
type: qa
step: 1
---
## Q
**"最近浏览"记录 · 核心思路**｜出自："最近浏览"记录 › 需求

设计"最近浏览"组件：构造时给定 limit，每位客户最多保留最近 limit 个商品，重复浏览只提前不占两个位置，超限丢最久未浏览的。核心设计是什么？

## A
**要点。** 每个客户一个定长 LRU：用按插入顺序排列且能 O(1) 摘除任意元素的结构（哈希表加双向链表，即语言里的有序字典）。
**操作。** 重复浏览是摘下来放到队尾，超限是丢掉队头。
**复杂度。** view 与查重都是 O(1)，recent 是 O(返回个数)。
