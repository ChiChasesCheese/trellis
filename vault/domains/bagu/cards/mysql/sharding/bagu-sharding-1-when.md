---
id: bagu-sharding-1-when
node: a.mysql.sharding
type: qa
step: 1
---
## Q
**分库分表 · 什么时候该拆**｜必会

面试官：「订单表有 8000 万行，查询开始变慢，是不是该分库分表了？」

## A
**基本回答。** 不急着拆。先加索引、优化 SQL，再读写分离、加缓存、归档冷数据；都做完仍扛不住才拆，因为一拆就有跨分片查询、分布式事务、全局 ID、数据迁移，而且基本不可逆。8000 万行变慢，多半是索引或 SQL 的问题，不是行数的问题。真要拆的信号：索引树变高、改表结构和备份困难、单机写 QPS 或磁盘到顶。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16KB 页的 B+ 树，行 1KB，3 层能放多少行</text>
<rect x="110" y="22" width="120" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根页：1170 个指针</text>
<line x1="150" y1="50" x2="95.6333" y2="69.9345" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,72.0 95.5,66.6 97.7,72.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="50" x2="170" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,72.0 166.8,65.0 173.2,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="190" y1="50" x2="244.367" y2="69.9345" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,72.0 242.3,72.6 244.5,66.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="72" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第二层：1170 个页，各 1170 个指针</text>
<line x1="90" y1="100" x2="90" y2="114" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,120.0 86.8,113.0 93.2,113.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="100" x2="170" y2="114" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,120.0 166.8,113.0 173.2,113.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="250" y1="100" x2="250" y2="114" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,120.0 246.8,113.0 253.2,113.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="120" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶子页：每页 16 行（行 1KB）</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1170 × 1170 × 16 ≈ 2190 万行</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">行 5KB：每页 3 行，约 411 万行</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">4 层要 256 亿行，3 层是合理上限</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先优化，再读写分离、缓存、归档，最后才拆</text>
</svg>
单表上限由 3 层 B+ 树算出：16KB 页的非叶节点每项约 14 字节（8 字节主键加 6 字节指针），一页约 1170 个指针（估算，实测约 900）；叶子页存整行，所以行宽决定上限。3 层足够，根页常驻内存，查一次只要 3 次页访问；「2000 万行」只是行 1KB 时的经验值。
**业务场景。** 打赏流水表 8000 万行变慢：慢日志显示按主播加时间查询缺联合索引，补上并把半年前的流水归档到冷表，查询恢复，没拆库。
**容易错。**
- **看到几千万行就分表：** 先查索引和 SQL。
- **把 2000 万当硬上限：** 行 5KB 时 3 层只有约 411 万行。
- **以为拆了就解决：** 拆了带来跨分片查询、分布式事务和运维成本。
- **忽略归档：** 多数数据是冷数据，归档比拆分便宜得多。
