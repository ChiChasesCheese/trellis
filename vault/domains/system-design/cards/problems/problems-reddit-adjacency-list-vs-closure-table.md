---
id: problems-reddit-adjacency-list-vs-closure-table
node: problems.social.reddit
type: qa
step: 4
tags: [grown]
---
## Q
For storing a Reddit-style nested comment tree where the dominant read pattern is 'fetch one page of a given comment's direct children, sorted by score' rather than 'fetch an entire subtree', why is an adjacency list (a `parentId` pointer per row, with a composite index on `(parentId, score)`) preferred over a closure table (storing every ancestor-descendant pair), even though the closure table makes subtree queries O(1)?

## A
A closure table's O(1) subtree lookup comes at the cost of write amplification: inserting one comment requires writing one row per ancestor, so a 50,000-comment thread with an average nesting depth of 6 produces about 300,000 closure-table rows — roughly 6x the row count of the adjacency list's 50,000 rows — for a query pattern (whole-subtree fetch) that this workload rarely needs. The adjacency list's composite index already answers the actually-common query ('one sorted page of a node's direct children') in O(log N + K), so the closure table's extra write cost buys a capability this design doesn't use.

## Q zh
在存储 Reddit 式嵌套评论树时，如果主要的读取模式是「取某条评论按分数排序的一页直接子评论」而不是「取整棵子树」，为什么邻接表（每行一个 `parentId` 指针，配合 `(parentId, score)` 复合索引）优于闭包表（存储全部祖先-后代对），即便闭包表能把子树查询做到 O(1)？

## A zh
闭包表 O(1) 的子树查询是用写放大换来的：插入一条评论需要为每个祖先各写一行，一个 5 万条评论、平均嵌套深度 6 层的帖子会产生约 30 万行闭包表记录——约是邻接表 5 万行的 6 倍——而这换来的能力（整棵子树查询）在这个工作负载里很少用到。邻接表的复合索引已经能以 O(log N + K) 回答真正常见的查询（「某节点按分数排序的一页直接子评论」），闭包表额外的写入成本买到的是这个设计用不上的能力。
