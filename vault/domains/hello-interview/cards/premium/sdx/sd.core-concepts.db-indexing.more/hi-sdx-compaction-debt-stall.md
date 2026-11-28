---
id: hi-sdx-compaction-debt-stall
node: sd.core-concepts.db-indexing.more
type: qa
step: 4
---
## Q
**压测很漂亮，线上周期性卡顿**｜补充 · 数据库索引 · 追问

面试官：「一个 LSM 存储压测时表现很好，上线后出现周期性延迟尖刺，持续高写入时吞吐还会塌掉。解释压实干扰的机制，引擎怎么应对？」

## A
**结论。** 前台写入（预写日志加内存表刷盘）、后台压实和读，共用同一块磁盘带宽。写入比压实便宜，持续写入时压实追不上，未合并的文件越积越多，读要查的文件越来越多。引擎的办法是主动限速、停写。

**要点。**
- **延迟尖刺：** 大压实一跑，读和压实抢 I/O，还会把热数据挤出缓存，高分位延迟排在压实后面。
- **压测漏掉：** 短时间的压测几乎触发不了压实，数据量还没长到需要合并。
- **吞吐塌陷：** 每个写入的字节之后还要被重写多次，持续写入可以无限快于压实，欠账（pending compaction bytes）不断增长。
- **欠账后果：** 文件数增加，读放大上升，直到系统基本不可用。
- **引擎应对：** 欠账超过阈值时限速或停写，主动牺牲峰值写入来保稳定。RocksDB 默认 L0 文件到 20 个开始限速、到 36 个停写；同时限制压实的 I/O 速率。
- **监控：** 看每层文件数和待压实字节，不要只看写 QPS。
- **2026 亮点：** 字节的云原生数仓 ByteHouse 把压实强度做成反馈控制：表由不可变的列存稳定段和记录近期修改的增量段组成，后台按增量段数量自适应调节压实强度，而不是固定速率；写入先进带 WAL 的 KV 暂存区，再按大小或时间阈值刷成列存。压实太勤会放大写 I/O、和前台抢带宽，太懒会让扫描碎片化，和上面的限速停写是同一个取舍。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 330">
<rect x="30" y="8" width="280" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="32.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持续写入快于压实</text>
<polyline points="170,48 170.0,67.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,74 166.8,67.0 173.2,67.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="30" y="74" width="280" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="98.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">欠账和 L0 文件数持续增长</text>
<polyline points="170,114 170.0,133.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,140 166.8,133.0 173.2,133.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="30" y="140" width="280" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="164.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读要查的文件越来越多</text>
<polyline points="170,180 170.0,199.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,206 166.8,199.0 173.2,199.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="30" y="206" width="280" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="230.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RocksDB：20 个限速，36 个停写</text>
<text x="8" y="282" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写入比压实便宜，欠账不会自己消</text>
<text x="8" y="300" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">监控待压实字节和每层文件数，</text>
<text x="8" y="318" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">压测要跑到压实进入稳态</text>
</svg>

**面试里这样说。** 「持续写入下压实欠账会越积越多，读放大随之上升，引擎靠限速和停写保稳定。所以我会压测足够长的时间让压实进入稳态，并监控待压实字节和每层文件数。」

**易错。**
- **压测只跑几分钟：** 看不到压实欠账，吞吐数字虚高。
- **只扩容读：** 瓶颈是压实 I/O，加读副本不解决写入侧的欠账。
