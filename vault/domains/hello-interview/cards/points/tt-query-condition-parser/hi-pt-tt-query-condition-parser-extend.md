---
id: hi-pt-tt-query-condition-parser-extend
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 14
---
## Q
**条件解析与内存表查询 · JOIN 和 GROUP BY 怎么演进**｜加分 · 出自：条件解析与内存表查询 › 取舍与追问

现在只有单表过滤，要加 `JOIN`、`GROUP BY`，结构怎么改？

## A
**要点。** 执行层改成算子链：扫描 → 过滤 → 连接 → 聚合 → 排序 → 投影，每层一个迭代器。

**过滤下推。** 先过滤再连接，减少中间结果。60 分钟内一般只要口述。
