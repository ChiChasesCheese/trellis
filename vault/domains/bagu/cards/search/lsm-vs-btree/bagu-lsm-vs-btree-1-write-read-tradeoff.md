---
id: bagu-lsm-vs-btree-1-write-read-tradeoff
node: b.search.lsm-vs-btree
type: qa
step: 1
---
## Q
**LSM-Tree 与 B+ Tree · 本质区别**｜追问

面试官：「LSM-Tree 和 B+ Tree 的本质区别是什么？写多读少的时序指标和订单数据各选哪个？」

## A
**基本回答。** B+ 树优化读：找到目标页（随机 IO）就地插入，页满分裂，涉及多个随机页写；也先顺序写日志，但数据页最终就地更新；读写延迟平稳，点查范围查都快，适合 OLTP（InnoDB）。LSM 优化写：先顺序写 WAL，再写内存 MemTable，写满后刷成不可变的有序 SSTable，后台 compaction 逐层合并。代价：读要查 MemTable 和多层 SSTable（读放大），用 Bloom Filter（判断文件里一定没有 key）和块缓存减少，但不能消除；compaction 带来写放大（同一份数据被反复重写）、空间放大（新旧文件并存）和 IO 峰值（P99 抖动，要靠资源隔离和合并限速治理）。选型：写吞吐高、读相对少用 LSM（RocksDB、LevelDB）；点查、范围查和强一致事务为主用 B+ 树。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">B+ 树</text>
<text x="178" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">LSM-Tree</text>
<rect x="6" y="22" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找到目标页</text>
<text x="84" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（随机 IO）</text>
<line x1="84" y1="62" x2="84.0" y2="71.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84,78 80.8,71.0 87.2,71.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="78" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页内插入</text>
<text x="84" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页满则分裂</text>
<line x1="84" y1="118" x2="84.0" y2="127.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84,134 80.8,127.0 87.2,127.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="134" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="150.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">就地更新数据页</text>
<text x="84" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">多个随机页写</text>
<rect x="178" y="22" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先顺序写 WAL</text>
<text x="256" y="53.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（追加日志）</text>
<line x1="256" y1="62" x2="256.0" y2="71.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256,78 252.8,71.0 259.2,71.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="78" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入内存 MemTable</text>
<text x="256" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（保持有序）</text>
<line x1="256" y1="118" x2="256.0" y2="127.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256,134 252.8,127.0 259.2,127.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="134" width="156" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="150.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写满刷成 SSTable</text>
<text x="256" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不可变的有序文件</text>
<line x1="256" y1="174" x2="256.0" y2="183.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256,190 252.8,183.0 259.2,183.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="190" width="156" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后台 compaction</text>
<text x="256" y="221.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">逐层合并</text>
<text x="6" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读：O(log N) 次页读取</text>
<text x="6" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">延迟平稳，点查和范围查都快</text>
</svg>
左边是 B+ 树的写：找到位置就地改，会随机访问很多页；右边是 LSM 的写：只追加、攒一批再合并。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="6" y="6" width="84" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读放大</text>
<line x1="90" y1="25" x2="95.0" y2="25.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102,25 95.0,28.2 95.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="108" y="22" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">要查 MemTable 和多层 SSTable，</text>
<text x="108" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Bloom Filter 跳过没有的文件</text>
<rect x="6" y="52" width="84" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写放大</text>
<line x1="90" y1="71" x2="95.0" y2="71.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102,71 95.0,74.2 95.0,67.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="108" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同一份数据被 compaction</text>
<text x="108" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">逐层反复重写</text>
<rect x="6" y="98" width="84" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="121" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">空间放大</text>
<line x1="90" y1="117" x2="95.0" y2="117.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102,117 95.0,120.2 95.0,113.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="108" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧文件和新文件并存，</text>
<text x="108" y="130" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">合并完才删旧的</text>
<rect x="6" y="144" width="84" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="167" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">延迟抖动</text>
<line x1="90" y1="163" x2="95.0" y2="163.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102,163 95.0,166.2 95.0,159.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="108" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">合并时 IO 出现峰值，</text>
<text x="108" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">P99 变差</text>
</svg>
LSM 把写变快的代价：读、写、空间和延迟四个方面都要付钱。
**业务场景。** 时序指标每秒大量写入、读相对少，选 LSM 引擎；订单按主键点查、按时间范围查，选 B+ 树的 MySQL。
**容易错。**
- **以为 LSM 全面比 B+ 树快：** 只是写快，读有放大，compaction 让延迟抖动。
