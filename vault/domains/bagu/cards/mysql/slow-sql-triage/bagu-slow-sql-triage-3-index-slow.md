---
id: bagu-slow-sql-triage-3-index-slow
node: a.mysql.slow-sql-triage
type: qa
step: 4
---
## Q
**EXPLAIN 显示走了索引，为什么还是慢**｜追问

面试官：「EXPLAIN 显示用上了索引，这条 SQL 还是很慢，可能有哪些原因？」

## A
**基本回答。** 「用了索引」不等于快，命中的行越多成本越高。常见八类原因：选择性差（区分度低，命中行占比高）；回表太多（改覆盖索引）；`Using filesort` / `Using temporary`；深分页（`LIMIT 1000000, 20` 要读出前一百万行再丢）；优化器选错索引（统计信息过期，先 `ANALYZE TABLE`，不行再临时 `FORCE INDEX` 或调联合索引）；在等锁（`Lock_time` 大，查 `innodb_trx`、`sys.innodb_lock_waits`）；冷数据不在缓冲池；`SELECT *` 读出 `TEXT`、`BLOB`。join 被驱动表的关联列没索引、两列类型或字符集不一致，也会拖慢。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">EXPLAIN 显示走了索引，仍慢的八类原因</text>
<rect x="8" y="22" width="159" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87.5" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选择性差</text>
<rect x="173" y="22" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252.5" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回表太多</text>
<rect x="8" y="62" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.5" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">filesort、临时表</text>
<rect x="173" y="62" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252.5" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">深分页</text>
<rect x="8" y="102" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.5" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">优化器选错索引</text>
<rect x="173" y="102" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252.5" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">在等锁</text>
<rect x="8" y="142" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.5" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">冷数据没命中缓存</text>
<rect x="173" y="142" width="159" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="252.5" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT * 读大字段</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">EXPLAIN 的 rows 是估算，真实可差几个数量级</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">用 EXPLAIN ANALYZE 看实际行数和耗时</text>
</svg>
八格是八个方向，第一格最常见。EXPLAIN 的 `rows` 只是估算，可差几个数量级；用 `EXPLAIN ANALYZE`（8.0.18 起）看 `actual time` 和实际行数，慢日志的 `Rows_examined` 才是真扫描行数。
**业务场景。** 排行榜明细用 `(anchor_id, status)` 索引，EXPLAIN 正常却耗时 3 秒：`EXPLAIN ANALYZE` 显示索引命中 20 万行、回表 20 万次，过滤后剩 30 行，因为 `status` 区分度低；改成 `(anchor_id, created_at, status)`，索引里直接过滤和排序，只读 30 行。
**容易错。**
- **看到 key 有值就放心：** 扫描行数可能仍很大。
- **相信 EXPLAIN 的 rows：** 它是估算。
- **选错索引就一直 FORCE INDEX：** 只是救火，先刷统计信息。
