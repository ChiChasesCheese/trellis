---
id: bagu-rdb-aof-4-aof-rewrite
node: a.redis.rdb-aof
type: qa
step: 4
---
## Q
**AOF 重写 · 为什么需要，怎么做，期间主线程为什么不被阻塞**｜追问

面试官：「AOF 文件越来越大，Redis 怎么重写？重写期间的新写命令怎么办？」

## A
**基本回答。** AOF 只追加不删除，文件越来越大，恢复要重放，而同一 key 的历史命令大多无用：`INCR counter` 一百万次只需一条 `SET counter 1000000`。重写不是压缩旧文件，而是按当前内存为每个 key 生成最短命令写成新 AOF 替换旧的；由 fork 的子进程做，读 fork 时刻的内存、不读旧 AOF，主线程不被阻塞。重写期间新命令：7.0 之前同时写 AOF 缓冲区和重写缓冲区，子进程完成后主线程把重写缓冲追加到新文件再改名，这一步在主线程，缓冲大时阻塞一次；7.0 起重写一开始就切到新的增量文件，子进程只生成新基础文件，完成后原子更新清单，不再需要重写缓冲区。触发：`BGREWRITEAOF`，或文件超过 `auto-aof-rewrite-min-size`（64MB）且比上次重写后增长 `auto-aof-rewrite-percentage`（100%）。重写也要 fork，写时复制和 fork 阻塞风险同样适用，大 key 让重写更慢。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="22" width="146" height="100" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧 AOF</text>
<text x="81" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INCR counter</text>
<text x="81" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INCR counter</text>
<text x="81" y="90.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INCR counter</text>
<text x="81" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…共 100 万条</text>
<text x="180" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重写</text>
<line x1="154" y1="80" x2="206" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="206,80 199.0,83.2 199.0,76.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="208" y="52" width="124" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新 AOF</text>
<text x="270" y="86.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET counter</text>
<text x="270" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000000</text>
<rect x="8" y="142" width="324" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子进程按 fork 时的内存生成</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不读旧 AOF，主线程不被阻塞</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7.0 起：开始就切新增量文件，</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">完成后原子更新清单</text>
</svg>
左边是越记越长的旧日志，右边是按当前内存生成的最短版本，生成由子进程做。
**业务场景。** 打赏计数器每秒 `INCR` 上万次，AOF 一天涨几十 GB，恢复要重放几十分钟；重写后每个计数器只剩一条命令，重写期间又来的 100 次 `INCR` 进新的增量文件不丢，恢复只需一条 `SET` 加 100 条增量命令。
**容易错。**
- **以为重写是读旧 AOF 再压缩。**
- **以为重写期间主线程完全不受影响。**
