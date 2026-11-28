---
id: bagu-redo-undo-binlog-2-wal-flush
node: a.mysql.redo-undo-binlog
type: qa
step: 2
---
## Q
**redo 与 WAL · 为什么它让写更快，刷盘参数怎么影响丢数据**｜必会

面试官：「redo log 为什么能提高写入性能？`innodb_flush_log_at_trx_commit` 取 0、1、2 分别怎样？」

## A
**基本回答。** redo 能提高写入性能，靠的是 WAL（Write-Ahead Logging，先写日志）：先在缓冲池里改数据页，同时顺序追加 redo；提交时只需要把 redo 刷到磁盘，脏页以后再慢慢刷。顺序写比分散的随机写快得多，崩溃后用 redo 重做。参数 `innodb_flush_log_at_trx_commit`：取 1（默认）每次提交都写盘并 fsync，掉电不丢；取 2 每次提交只写到系统缓存、每秒 fsync 一次，进程崩溃不丢、掉电会丢约 1 秒；取 0 每秒写一次并 fsync，进程崩溃也可能丢约 1 秒。配套的 `sync_binlog=1` 表示每次提交都 fsync binlog，两个都取 1 俗称「双一」。
组提交（group commit）把并发事务合成一次 fsync，高并发下双一的代价比想象的小。日志缓冲 `innodb_log_buffer_size` 默认 16MB。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一次提交，三种设置各走到哪一步</text>
<rect x="8" y="22" width="90" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">log buffer</text>
<rect x="125" y="22" width="90" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">系统缓存</text>
<rect x="242" y="22" width="90" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="287" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">磁盘</text>
<line x1="98" y1="38" x2="119" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="125.0,38.0 118.0,41.2 118.0,34.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="215" y1="38" x2="236" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="242.0,38.0 235.0,41.2 235.0,34.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进程内存</text>
<text x="125" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">操作系统</text>
<text x="332" y="72" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fsync 后才算落盘</text>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">=1 每次提交：写系统缓存并 fsync</text>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">    掉电不丢（默认）</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">=2 每次提交写系统缓存，每秒 fsync</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">    进程崩溃不丢，掉电丢约 1 秒</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">=0 每秒写并 fsync</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">    进程崩溃也可能丢约 1 秒</text>
</svg>
一次提交的日志要先后经过三个位置：MySQL 进程内的 log buffer、操作系统的缓存、磁盘。只有 fsync 之后才真正落盘，三种参数差别就在「什么时候做到哪一步」。
**举个例子。** 一次提交，分别看三种参数：
1. **事务提交：** 日志内容已在 log buffer 里。
2. **取 1：** 写到系统缓存，立刻 fsync，磁盘上有了才返回成功。此刻断电，重启后能重做这笔事务。
3. **取 2：** 写到系统缓存就返回成功，磁盘上可能还没有。MySQL 进程被杀，数据在系统缓存里，不丢；机房断电，系统缓存丢失，最后一秒内提交的事务会丢。
4. **取 0：** 只写进 log buffer 就返回成功，每秒才写盘。进程被杀，buffer 里的内容就丢了。
5. **脏页怎么办：** 无论哪种取值，脏页都不在提交路径上，后台线程慢慢刷。
**容易错。**
- **以为 WAL 多写了一份所以更慢：** 多写的是顺序写、体积很小的 redo，省掉的是随机写的整页 16KB，合起来反而更快。
- **以为取 2 掉电也不丢：** 取 2 只防进程崩溃，系统缓存还没落盘时掉电，仍会丢约 1 秒。
- **以为取 0 和取 2 一样：** 取 0 连系统缓存都没到，进程崩溃就丢；取 2 进程崩溃不丢。
- **只改 redo 参数不管 binlog：** 要不丢数据，两个都要取 1；只设一个，另一份日志仍可能丢。
**业务场景。** 支付库为吞吐把参数改成 2，机房断电后丢了最后一秒的几百笔已提交支付，而用户已收到成功通知；账务库必须保持「双一」，吞吐靠批量提交、组提交和更好的 SSD。
