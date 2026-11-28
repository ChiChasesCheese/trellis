---
id: bagu-slow-sql-triage-5-billions
node: a.mysql.slow-sql-triage
type: qa
step: 5
---
## Q
**几十亿数据 · 索引加了效果仍不好，整条链路怎么优化**｜追问

面试官：「表里几十亿行，索引都加了查询还是慢，你怎么从整条链路优化？」

## A
**基本回答。** 几十亿行时 B+ 树更高、缓冲池放不下热页，单靠索引不够，要减少要查的数据并换合适的存储：冷热分离、归档、按时间分区、限制查询时间窗口；按最常带的列（如 `user_id`）分库分表，让多数查询落在一个分片；多条件任意筛选和全文检索交给 Elasticsearch，大范围聚合交给 ClickHouse（数据经 binlog 同步），MySQL 只做按主键、按用户的点查；统计类预聚合成结果表。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="8" y="8" width="112" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户侧</text>
<text x="64" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">「我的打赏」点查</text>
<rect x="196" y="8" width="136" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="264" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MySQL 近 90 天</text>
<text x="264" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按 anchor_id 分表</text>
<line x1="120" y1="27" x2="190" y2="27" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,27.0 189.0,30.2 189.0,23.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="118" width="112" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">运营后台</text>
<text x="64" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">任意条件筛选统计</text>
<rect x="196" y="118" width="136" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="264" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ClickHouse</text>
<text x="264" y="148.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全量 60 亿行</text>
<line x1="120" y1="137" x2="190" y2="137" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196.0,137.0 189.0,140.2 189.0,133.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="264" y1="46" x2="264" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="264.0,118.0 260.8,111.0 267.2,111.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="256" y="86" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">binlog 同步</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">缩范围：冷热分离、归档、按时间分区</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">点查走 MySQL，分析走 ClickHouse 或 ES</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分页用游标，不取精确 count(*)</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">入口加缓存、限流，保护数据库</text>
</svg>
同一批数据两条路：用户侧点查走 MySQL，运营侧任意筛选走 ClickHouse，靠 binlog 同步，互不影响。查询方式也要改：游标分页，不取精确 `count(*)`（用估算或缓存），缓存和限流保护数据库，非关键写入先进消息队列再批量落库。
**业务场景。** 打赏流水三年累计 60 亿行，运营后台要按主播、时间、金额、礼物、状态任意组合筛选：MySQL 只留近 90 天并按 `anchor_id` 分表供「我的打赏」点查，全量流水同步到 ClickHouse 供运营筛选统计。
**容易错。**
- **以为继续加索引就行：** 树更高，缓存放不下。
- **让 MySQL 承担所有查询：** 任意条件筛选和大范围聚合要交给 ES、ClickHouse。
- **只看数据库不看链路：** 先用链路追踪确认瓶颈确实在数据库，并明确 QPS、P99、新鲜度目标。
