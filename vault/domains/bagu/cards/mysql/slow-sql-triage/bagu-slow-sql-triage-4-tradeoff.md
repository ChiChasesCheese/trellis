---
id: bagu-slow-sql-triage-4-tradeoff
node: a.mysql.slow-sql-triage
type: qa
step: 3
---
## Q
**优化手段 · 加索引、改写、拆查询、加缓存各自的取舍**｜必会

面试官：「一条慢 SQL 有哪几种优化办法？各自代价是什么，怎么选？」

## A
**基本回答。** 按代价从低到高选：改写 SQL（只取需要的列、不在列上套函数、深分页改游标）；加或改索引（占空间、拖慢每次写，大表用在线 DDL，优先覆盖索引）；拆查询（先查主键再批量取详情，多几次往返，一致性自己保证）；加缓存（一致性、穿透、击穿）；读写分离（主从延迟，刚写完读到旧数据）；归档冷数据；分库分表最后，基本不可逆。原则：先便宜、可逆、没副作用的。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">优化手段：从上到下代价递增</text>
<rect x="8" y="22" width="120" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改写 SQL</text>
<text x="138" y="39" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">随时可回滚</text>
<rect x="8" y="53" width="120" height="25" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加或改索引</text>
<text x="138" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">占空间，拖慢写</text>
<rect x="8" y="84" width="120" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="100.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拆查询</text>
<text x="138" y="101" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">多几次往返</text>
<rect x="8" y="115" width="120" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加缓存</text>
<text x="138" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一致性、穿透</text>
<rect x="8" y="146" width="120" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读写分离</text>
<text x="138" y="163" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有主从延迟</text>
<rect x="8" y="177" width="120" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">归档冷数据</text>
<text x="138" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要迁走旧数据</text>
<rect x="8" y="208" width="120" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="224.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分库分表</text>
<text x="138" y="225" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最后手段，难回头</text>
</svg>
从上到下是尝试顺序，右边是每步的主要代价；索引最常用也最易滥用，加之前用 `sys.schema_unused_indexes` 清理没用的旧索引。每步都对比前后 `rows` 和耗时；`FORCE INDEX` 或 optimizer hint 只是救火。
**业务场景。** 打赏流水明细页「按主播查最近 7 天」每天几千万行：先只取展示列并改游标分页，再建 `(anchor_id, created_at)` 覆盖索引，主播汇总放 Redis 缓存 1 分钟，一年以上流水迁归档库；仍快速增长才考虑按 `anchor_id` 分表。
**容易错。**
- **一上来就分库分表：** 最贵最难回头。
- **只加索引不看写入代价：** 每个索引都拖慢写。
- **加缓存当万能药：** 只适合读多写少、能容忍短暂旧数据。
