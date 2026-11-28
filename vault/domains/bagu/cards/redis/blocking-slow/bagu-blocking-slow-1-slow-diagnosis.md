---
id: bagu-blocking-slow-1-slow-diagnosis
node: b.redis.blocking-slow
type: qa
step: 1
---
## Q
**Redis 变慢 · 排查顺序**｜追问

面试官：「凌晨 Redis 延迟突然从 1ms 升到 300ms，你按什么顺序排查？内存碎片是什么，怎么处理？」

## A
**基本回答。** 主线程串行，一条慢命令让后面全部排队。先分清某条命令慢还是整体卡：`SLOWLOG GET`（默认记超过 10ms 的命令，只含执行时间，不含排队和网络）和 `LATENCY DOCTOR`，再用 `INFO`、`LATENCY HISTORY` 把故障时间点和事件对齐。常见原因按顺序：O(n) 命令与大 key（`DEL` 500 万成员的 Set 约 260MB，在主线程同步释放，通常阻塞百毫秒量级，`UNLINK` 交后台线程不到 1 毫秒；`lazyfree-lazy-user-del` 默认 no，所以 `DEL` 默认同步）；AOF `everysec` 的 fsync 在磁盘忙时拖住主线程；fork（bgsave、AOF 重写）复制页表，实例越大越慢，透明大页（THP）放大写时复制代价；swap 最致命，延迟到毫秒甚至秒级；内存碎片；最后才是网络与连接数。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<rect x="8" y="8" width="324" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先看 SLOWLOG GET 与 LATENCY DOCTOR</text>
<line x1="170" y1="34" x2="170" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,46 166.8,39 173.2,39" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="46" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1. O(n) 命令、大 key</text>
<rect x="176" y="46" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2. AOF 刷盘（fsync）</text>
<rect x="8" y="78" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="95" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3. fork：bgsave、重写</text>
<rect x="176" y="78" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="95" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4. swap 换到磁盘</text>
<rect x="8" y="110" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5. 内存碎片</text>
<rect x="176" y="110" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6. 网络与连接数</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">碎片率 = used_memory_rss / used_memory</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大于 1.5 要处理；小于 1 说明在 swap</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">DEL 大 Set 阻塞百毫秒量级，UNLINK 不到 1 毫秒</text>
</svg>
先判断单条命令还是整体卡，再按编号逐项排查；底部三个数字最常用。碎片率 `mem_fragmentation_ratio` = `used_memory_rss` / `used_memory`：大于 1.5 要处理（`activedefrag yes`，默认关，或重启、主从切换），小于 1 说明部分内存被换到 swap，更严重。
**业务场景。** 凌晨延迟从 1ms 升到 300ms：慢日志里有定时任务的 `DEL` 删大 key，`LATENCY HISTORY` 显示同一时刻还有 AOF 重写的 fork 延迟尖峰，两件事叠加；把 `DEL` 换成 `UNLINK`，并让定时任务与 AOF 重写错开。
**容易错。**
- **以为慢日志包含全部延迟。**
- **以为碎片率越小越好。**
- **一上来就怀疑网络。**
