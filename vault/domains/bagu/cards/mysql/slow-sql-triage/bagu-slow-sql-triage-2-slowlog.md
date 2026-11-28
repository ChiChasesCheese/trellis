---
id: bagu-slow-sql-triage-2-slowlog
node: a.mysql.slow-sql-triage
type: qa
step: 2
---
## Q
**慢日志 · 怎么开启，怎么分析，怎么发现这条 SQL**｜必会

面试官：「慢查询日志怎么开？哪些字段最有用？线上有几千种 SQL，怎么找出最该优化的几条？」

## A
**基本回答。** 开关 `slow_query_log`，阈值 `long_query_time`（秒，默认 10，线上设 0.5 到 1）；`log_queries_not_using_indexes` 小表全扫也记，噪声大要慎用；`min_examined_row_limit` 过滤扫描很少的语句；8.0 用 `SET PERSIST` 重启不丢。线上几千种 SQL，用 `pt-query-digest`（或自带的简化版 `mysqldumpslow`）去掉常量按模板聚合，按**总耗时**排序，再优化最前面的几条。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">慢日志里的一条记录</text>
<rect x="8" y="22" width="324" height="92" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="18" y="42" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Query_time：2.1 秒（总耗时）</text>
<text x="18" y="62" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Lock_time：0.0 秒（等锁）</text>
<text x="18" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Rows_examined：500000（扫了多少行）</text>
<text x="18" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Rows_sent：20（返回多少行）</text>
<line x1="120" y1="114" x2="120" y2="128" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,134.0 116.8,127.0 123.2,127.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="130" y="129" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">相差悬殊 → 索引没起过滤</text>
<rect x="8" y="138" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成千上万条</text>
<rect x="120" y="138" width="100" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按模板聚合</text>
<rect x="232" y="138" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">总耗时排序</text>
<line x1="108" y1="152" x2="114" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,152.0 113.0,155.2 113.0,148.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220" y1="152" x2="226" y2="152" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,152.0 225.0,155.2 225.0,148.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">A：每次 20 毫秒 × 每秒上千次</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B：每次 5 秒 × 一天一次</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">总耗时 A 远大于 B，先优化 A</text>
</svg>
上半是一条记录要盯的四个字段：`Query_time` 总耗时；`Lock_time` 占大头就是锁等待，不是索引问题；`Rows_examined` 远大于 `Rows_sent` 说明索引没起过滤作用。下半是挑目标：每次 20 毫秒、每秒上千次的语句，总耗时远大于一天一次的 5 秒报表。
**免读日志。** `performance_schema.events_statements_summary_by_digest` 直接按模板聚合；`sys.statements_with_full_table_scans` 列出全表扫描模板；8.0.14 起 `log_slow_extra` 多记几个字段。`long_query_time` 设 0 等于记全部语句，只能短时间采样，因为写盘有成本。
**业务场景。** 大促前一周在压测环境设 `long_query_time=0.2` 采一小时，`pt-query-digest` 聚合后第一名是「按主播查今日打赏流水」，占总耗时 40%，每次扫 8 万行返回 50 行，缺 `(anchor_id, created_at)` 索引；补上后整体耗时降得最多。
**容易错。**
- **只看单次最慢：** 高频小慢查询总耗时才大。
- **长期开未走索引日志或阈值设 0：** 刷屏且有写盘成本。
- **Lock_time 大还去加索引：** 它说明在等锁，要查谁占着。
