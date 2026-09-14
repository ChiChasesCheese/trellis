---
id: metadata-cache-where-clause-breaks-shortcut
node: cache.metadata-cache-pruning-stats
type: qa
tags: [grown]
---
## Q
`SELECT COUNT(*) FROM events` 秒回且不占用仓库，但加上 `WHERE status = 'error'` 之后同一查询却需要启动仓库并扫描数据，原因是什么？

## A
元数据只记录每个微分区（micro-partition）的整体统计（行数、每列 min/max、去重计数、空值计数），不记录「满足某个条件的行有多少」。加了过滤条件后，元数据最多只能用 min/max 排除肯定不含 `error` 的分区（剪枝，pruning），剩下的分区仍须逐行检查才能计数，因此必须由仓库读取数据文件。
