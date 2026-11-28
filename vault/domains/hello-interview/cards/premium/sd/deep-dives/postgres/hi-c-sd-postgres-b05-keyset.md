---
id: hi-c-sd-postgres-b05-keyset
node: sd.deep-dives.postgres.beyond
type: qa
step: 5
---
## Q
**PostgreSQL · 深分页与执行计划**｜拓展 · 加分

为什么 `OFFSET` 分页越翻越慢？怎么确认索引真的被用上了？

## A
- **OFFSET 的代价：** `OFFSET 100000 LIMIT 20` 仍要先走过前 10 万行再丢掉，翻得越深越慢，而且并发写入时翻页时的内容会漂移（重复或漏项）。
- **键集分页（keyset pagination）：** 记住上一页最后一行的排序键，下一页用 `WHERE (created_at, id) < (:t, :id) ORDER BY created_at DESC, id DESC LIMIT 20`，借助索引直接定位，成本不随翻页深度增长。要求排序键唯一，所以带上 `id`。
- **代价：** 只能顺序翻页，不能随机跳到第 N 页。
- **确认索引：** 用 `EXPLAIN (ANALYZE)` 看实际执行计划，确认走的是索引扫描还是顺序扫描，以及估计行数和实际行数是否接近。
- **索引没被用的常见原因：** 列上套了函数、类型不匹配、统计信息过期（先运行 `ANALYZE`）、命中的行占比太大。
