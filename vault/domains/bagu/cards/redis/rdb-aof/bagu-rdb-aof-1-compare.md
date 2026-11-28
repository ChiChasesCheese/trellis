---
id: bagu-rdb-aof-1-compare
node: a.redis.rdb-aof
type: qa
step: 1
---
## Q
**持久化 · RDB 和 AOF 的区别与选择**｜必会

面试官：「Redis 有哪两种持久化？RDB 和 AOF 怎么工作，优缺点是什么，线上怎么选？」

## A
**基本回答。** RDB 记状态：某一刻内存的二进制快照，紧凑、装载快（像 `mysqldump` 全量），两次快照之间的数据会丢（分钟级）。AOF 记操作：每条写命令追加到日志（像 binlog 增量），按 `appendfsync` 最多丢约 1 秒，但冗长、恢复要把命令重放一遍，要定期重写。RDB 触发：`SAVE`（主线程同步，阻塞所有请求，线上不用）、`BGSAVE`（子进程）、或 `save` 规则，7.0 默认 `3600 1 300 100 60 10000`（1 小时 1 次修改、5 分钟 100 次、1 分钟 10000 次，满足任一条）。两者都开时重启优先读 AOF（更完整）；7.0 起 AOF 拆成基础、增量、清单文件（multi-part AOF）；开了混合持久化，基础文件本身就是 RDB 格式。选择：只当缓存可以都关；要保数据用 AOF `everysec` 加混合持久化；一条都不能丢的数据落数据库。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<rect x="8" y="8" width="156" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="25.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RDB：拍快照</text>
<rect x="176" y="8" width="156" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="25.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">AOF：记日志</text>
<rect x="8" y="52" width="156" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存（某一刻）</text>
<line x1="86" y1="84" x2="86" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86,106 82.8,99.0 89.2,99.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="106" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dump.rdb 紧凑</text>
<rect x="176" y="52" width="156" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每条写命令</text>
<line x1="254" y1="84" x2="254" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254,106 250.8,99.0 257.2,99.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="106" width="156" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">appendonly 完整</text>
<text x="12" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">恢复：装载，快</text>
<text x="12" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">丢：快照间隔内</text>
<text x="12" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（分钟级）</text>
<text x="180" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">恢复：重放，慢</text>
<text x="180" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">丢：最多约 1 秒</text>
<text x="180" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（everysec）</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">缓存可全关；要保数据用 AOF + 混合</text>
</svg>
左边某一刻内存存成一个文件，右边每条写命令都追加；下方是恢复方式和丢数据的窗口。
**业务场景。** 支付对账缓存存的是从账务库拉来的中间结果，丢了可重算，RDB 加 AOF everysec 就够；若把「已扣款未入账」状态只记在 Redis，10:04 掉电时只开 RDB 会丢 10:00 之后 4 分钟的写入，everysec 也丢最后不到 1 秒，资金对不上。
**容易错。**
- **以为 AOF 不会丢：** `no` 交给系统约 30 秒，主从切换还丢没复制出去的写。
- **以为两者二选一。**
- **在线上用 SAVE。**
