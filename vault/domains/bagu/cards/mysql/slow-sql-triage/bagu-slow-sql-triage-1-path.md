---
id: bagu-slow-sql-triage-1-path
node: a.mysql.slow-sql-triage
type: qa
step: 1
---
## Q
**慢 SQL 排查 · 线上一条 SQL 突然变慢，你按什么顺序查**｜必会

面试官：「大促时订单列表接口 P99 从 80 毫秒涨到 2 秒，你怀疑数据库。一条 SQL 突然变慢，怎么一步步排查？」

## A
**基本回答。** 先分清是「一条 SQL 慢」还是「所有查询都慢」；分错方向就会盲目加索引，白增写入成本。一条慢：从慢日志或语句摘要找总耗时最大的 SQL 模板，`EXPLAIN` 看 `type=ALL`、`key` 是否为空、`rows` 是否很大、有无 `Using filesort` / `Using temporary`，对症加索引或改写，改完对比前后 `rows` 和耗时；大表建索引用在线 DDL 或 gh-ost。所有都慢：先看长事务和元数据锁，再看磁盘 IO、缓冲池命中率、主从延迟、连接数、有无批处理或备份。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<rect x="90" y="6" width="160" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接口 P99 变慢</text>
<line x1="120" y1="34" x2="85.2573" y2="53.1085" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,56.0 84.6,49.8 87.7,55.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220" y1="34" x2="254.743" y2="53.1085" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260.0,56.0 252.3,55.4 255.4,49.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="56" width="156" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只有一条 SQL 慢</text>
<rect x="176" y="56" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">所有查询都慢</text>
<rect x="8" y="96" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">慢日志找最耗时模板</text>
<rect x="8" y="130" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">EXPLAIN 看 key、rows</text>
<rect x="8" y="164" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对症：索引或改写</text>
<rect x="8" y="198" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改完对比 rows 与耗时</text>
<rect x="176" y="96" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长事务、元数据锁</text>
<rect x="176" y="130" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘 IO、缓冲池命中率</text>
<rect x="176" y="164" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主从延迟、连接数</text>
<rect x="176" y="198" width="156" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批处理、备份在跑吗</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一条慢看执行计划，全部慢看资源和锁</text>
</svg>
先分叉：左边是执行计划问题，按四步走；右边是资源或锁的问题，逐项查；给右边加索引没用。
**元数据锁。** 一条 DDL 被没结束的长事务挡住，之后所有对这张表的查询都排在这条 DDL 后面，状态 `Waiting for table metadata lock`。工具：`SHOW PROCESSLIST`、`information_schema.innodb_trx`（长事务）、`SHOW ENGINE INNODB STATUS`（锁等待、`History list length`）、`iostat`。
**业务场景。** 订单列表接口 P99 从 80 毫秒涨到 2 秒：库 CPU 不高、无长事务，只有这个接口慢；慢日志里 `Rows_examined` 50 万而 `Rows_sent` 只有 20，`type=ALL`；补 `(user_id, created_at)` 后 P99 回到 60 毫秒。
**容易错。**
- **一变慢就加索引：** 全部变慢多是锁或资源问题，加索引没用还拖慢写入。
- **只看 EXPLAIN 不验证：** 改完要对比前后 `rows` 和耗时。
- **大表直接建索引：** 要用在线 DDL 或 gh-ost。
