---
id: hi-pt-tt-query-condition-parser-14-extend
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 14
---
## Q
**条件解析与内存表查询 · 要支持 JOIN 和 GROUP BY 怎么扩展**｜出自：条件解析与内存表查询 › 取舍与追问

现在只有单表过滤。要加 `JOIN`、`GROUP BY`，结构怎么演进？

## A
**要点。** 执行层改成算子链：扫描 → 过滤 → 连接 → 聚合 → 排序 → 投影，每层是一个迭代器，从下层取行。

**过滤下推。** 尽量先过滤再连接，减少中间结果。

**连接算法。** 小表建哈希表，大表逐行探测（Hash Join）。
