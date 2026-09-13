---
id: leetcode-c-postgresql-booking-difference-events-application
node: topics.uncategorised
type: qa
anki: 1787361365723
tags: [algorithm::difference-array, algorithm::prefix-sum, algorithm::sweep-line, application, case, case::postgresql-booking-difference-events, category::storage-databases, chapter::08, chapter::14, leetcode, system::postgresql]
---
## Q
预约容量为什么用 start `+units`、end `-units` 就能重建整条占用曲线？

## A
区间内部状态不变，只在边界发生增减。按时间聚合 delta 后做 ordered prefix sum，就得到每个边界后的当前占用；使用 [start,end) 可让相邻区间正确衔接。

**Evidence**

PostgreSQL 官方 range types 定义半开区间语义，window SUM 提供有序累计；差分事件是基于这些 primitive 的生产建模。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FPostgreSQL%20%E9%A2%84%E7%BA%A6%E5%AE%B9%E9%87%8F%EF%BC%9A%E8%BE%B9%E7%95%8C%E4%BA%8B%E4%BB%B6%E5%B7%AE%E5%88%86%E4%B8%8E%E7%AA%97%E5%8F%A3%E5%89%8D%E7%BC%80%E5%92%8C)
