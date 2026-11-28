---
id: bagu-rdb-aof-5-lose-hybrid
node: a.redis.rdb-aof
type: qa
step: 5
---
## Q
**为什么开了 AOF 仍可能丢数据，混合持久化解决什么**｜追问

面试官：「开了 AOF 数据也可能丢，哪些情况会丢？混合持久化是什么？」

## A
**基本回答。** 开了 AOF 仍会丢的四种：`everysec`/`no` 下掉电丢未 fsync 的页缓存；命令执行后、写日志前宕机；磁盘卡住使窗口拉长到约 2 秒；主从异步复制，主库宕机时没传出的写在提升从库后就丢了（这是复制的特性，与 AOF 无关）。混合持久化（`aof-use-rdb-preamble`，4.0 引入默认 no，5.0 起默认 yes）：重写生成的基础文件是 RDB 格式、重写那一刻的全部数据，其后追加增量命令；恢复先整块装 RDB（快）再重放增量（完整），比纯 AOF 恢复快、比纯 RDB 丢得少，但丢失窗口仍由 `appendfsync` 决定。7.0+ 目录：`appendonly.aof.1.base.rdb` 是 RDB 基础文件，`.incr.aof` 是命令文本增量，清单文件按序列出。更强保障：`always`、`WAIT` 等从库确认、权威数据放数据库。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">混合持久化：重写后的基础文件</text>
<rect x="8" y="26" width="170" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="93" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RDB 部分</text>
<text x="93" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重写那一刻的全部数据</text>
<rect x="178" y="26" width="154" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">增量命令</text>
<text x="255" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重写之后追加的 AOF</text>
<text x="93" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 先装载（快）</text>
<text x="255" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 再重放（完整）</text>
<text x="8" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">开了 AOF 仍会丢的四种情况：</text>
<text x="14" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">· 掉电丢未 fsync 的页缓存</text>
<text x="14" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">· 命令执行后、写日志前宕机</text>
<text x="14" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">· 磁盘卡住，窗口拉长到约 2 秒</text>
<text x="14" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">· 主从异步复制，没传出的写丢</text>
</svg>
基础文件前段是 RDB、后段是增量命令；下面列的是开了 AOF 仍会丢的四种情况。
**业务场景。** 缓存实例开混合持久化、每天凌晨重写：3:00 子进程把 500 万个 key 存成 `appendonly.aof.2.base.rdb`，同时新建 `.incr.aof` 接收之后的写；15:00 宕机重启，先装 RDB 再重放几十万条增量，数据恢复到宕机前约 1 秒；纯 AOF 则 500 万个 key 要逐条重新执行，慢得多。记录「回调已处理」标记的 Redis 掉电丢最后一秒，同一笔回调会被当新请求，所以幂等要有数据库唯一键兜底。
**容易错。**
- **以为开了 AOF 就不丢。**
- **以为混合持久化消除了丢失窗口：** 它改善的是恢复速度。
