---
id: problems-stack-overflow-tag-reverse-index
node: problems.social.stack-overflow
type: qa
step: 5
tags: [grown]
---
## Q
问答社区设计里，按标签查问题（`by_tag`）为什么要维护一个 `dict[str, set[str]]`（标签到问题 id 集合）的倒排索引，而不是每次查询时扫描全部问题过滤标签？

## A
标签检索是这道题里被反复触发的高频查询，扫描全表随问题总数线性增长，标签命中率越低浪费越大。倒排索引把“开一个问题”时的一次性代价（往每个标签对应的集合里加一次 id）换成了之后每一次查询的 O(1) 直接命中，这和数据库里给外键列建索引是同一个权衡：把成本从读的一侧移到写的一侧，因为读的次数远多于写。
