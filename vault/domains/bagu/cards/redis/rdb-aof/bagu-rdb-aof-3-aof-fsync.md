---
id: bagu-rdb-aof-3-aof-fsync
node: a.redis.rdb-aof
type: qa
step: 3
---
## Q
**AOF · 三种写回策略，everysec 最多丢多少**｜必会

面试官：「`appendfsync` 有哪三个值？`everysec` 最多丢多少数据？」

## A
**基本回答。** Redis 先执行命令，再追加到 AOF 缓冲区，`write()` 进页缓存（内核在内存里替磁盘攒的缓冲），最后 `fsync()` 才真正刷盘；三个策略只控制 fsync 时机。先执行的好处是不检查语法、不记错误命令，代价是执行成功后、写日志前宕机，这条命令就丢了。`always` 每条都刷，几乎不丢但吞吐被拖得很低；`everysec`（默认）后台线程每秒刷，几乎不拖主线程，掉电最多丢约 1 秒，但磁盘繁忙、上次 fsync 没做完时写入最多推迟约 2 秒，窗口可到 2 秒；`no` 交给系统，Linux 通常约 30 秒。进程崩溃但机器没掉电时，已 write 进页缓存的数据不丢，只有掉电或系统崩溃才丢未落盘的部分。与 MySQL 的 `innodb_flush_log_at_trx_commit`、`sync_binlog` 是同类取舍。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 264">
<rect x="8" y="8" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 执行命令</text>
<line x1="83" y1="38" x2="83" y2="50" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83,50 79.8,43.0 86.2,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="50" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="68.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 追加到 AOF 缓冲区</text>
<line x1="83" y1="80" x2="83" y2="92" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83,92 79.8,85.0 86.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="92" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ write() 进页缓存</text>
<line x1="83" y1="122" x2="83" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83,134 79.8,127.0 86.2,127.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="134" width="150" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ fsync() 刷到磁盘</text>
<line x1="83" y1="164" x2="83" y2="176" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83,176 79.8,169.0 86.2,169.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="176" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<line x1="158" y1="149" x2="172" y2="149" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="172" y1="98" x2="172" y2="166" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="172" y1="98" x2="180" y2="98" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="172" y1="132" x2="180" y2="132" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="172" y1="166" x2="180" y2="166" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="180" y="84" width="152" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="101.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">always：每条都刷</text>
<rect x="180" y="118" width="152" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="135.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">everysec：每秒刷</text>
<rect x="180" y="152" width="152" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">no：交给系统</text>
<text x="180" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 30 秒（Linux）</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进程崩溃不丢已 write 的，掉电才丢</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">策略只决定 fsync 什么时候做</text>
</svg>
一条写命令经执行、AOF 缓冲区、页缓存、磁盘；策略只决定第四步 fsync 的时机，everysec 是默认。
**业务场景。** `appendfsync everysec`，12:00:00.000 刚 fsync 过；.300 执行 `SET order:1 paid` 只在页缓存，.800 断电，这 0.8 秒的写入全丢；换 `always` 则 `order:1` 已在磁盘，代价是每条都等一次磁盘；若只是进程被杀，页缓存还在，不丢。所以对账缓存要能识别缺失并重拉，幂等判断要有数据库唯一键兜底。
**容易错。**
- **以为 everysec 最多丢 1 秒是绝对的。**
- **以为 write 了就落盘了。**
- **以为进程崩溃也会丢。**
