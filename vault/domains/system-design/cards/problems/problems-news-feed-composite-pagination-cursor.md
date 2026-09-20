---
id: problems-news-feed-composite-pagination-cursor
node: problems.social.news-feed
type: qa
step: 6
tags: [grown]
---
## Q
In a ranked (not purely chronological) news feed, why is a plain timestamp an unreliable pagination cursor, and what cursor design fixes it?

## A
A ranked feed's display order is determined by a computed score, not strictly by creation time, so multiple items can share nearly the same timestamp while having different ranks; paginating on timestamp alone causes items at a shared or nearby timestamp to be duplicated or skipped as new posts keep being inserted concurrently. The fix is a composite cursor of (score, postId): the query compares both fields together, using postId to break ties deterministically when scores match, so the pagination boundary stays stable and consistent with the actual ranked order even under concurrent inserts.

## Q zh
在一个按算法排序（而非纯时间倒序）的信息流里，为什么单纯用时间戳做分页游标不可靠？什么样的游标设计能修复这个问题？

## A zh
算法排序的信息流的展示顺序由一个计算出来的分数决定，不是严格按创建时间排列，所以多条内容可能时间戳几乎相同却排序不同；只用时间戳分页，在新帖不断并发插入的情况下，时间戳相同或相近的条目会被重复展示或遗漏。修复方法是用 (score, postId) 复合游标：查询同时比较这两个字段，分数相同时用 postId 做确定性的平局裁决，这样即使在并发插入下，分页边界依然和真实的排序结果保持稳定一致。
