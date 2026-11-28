---
id: bagu-distributed-id-1-snowflake-segment
node: b.distributed.distributed-id
type: qa
step: 1
---
## Q
**分布式 ID · 雪花、号段、UUID 怎么选**｜追问

面试官：「订单号要全局唯一、趋势递增，又不能暴露日订单量。雪花算法的结构是什么，时钟回拨怎么办？号段模式为什么适合做主键？」

## A
**基本回答。** 雪花（Snowflake）64 位：1 位符号 + 41 位毫秒时间戳 + 10 位机器号 + 12 位序列号。本地生成、趋势递增，每台每毫秒最多 4096 个。号段模式一次从数据库取一批号放内存，用完再取，数据库压力小。UUID 无序，作主键会让 B+ 树随机插入、频繁页分裂。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">雪花 64 位：本地生成，趋势递增</text>
<rect x="10" y="26" width="22" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="21.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="32" y="26" width="130" height="32" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="97.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">41 位毫秒时间戳</text>
<rect x="162" y="26" width="88" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="206.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 位机器号</text>
<rect x="250" y="26" width="80" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12 位序列</text>
<text x="97" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 69.7 年</text>
<text x="206" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最多 1024 台</text>
<text x="290" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每毫秒 4096 个</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">号段：一次取一批，用完再取</text>
<rect x="10" y="124" width="150" height="58" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库号段表</text>
<text x="85.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">current_max_id</text>
<text x="85.0" y="172.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000 → 2000</text>
<line x1="162" y1="153" x2="198" y2="153" stroke-width="1.2" stroke="currentColor"/>
<polygon points="198.0,153.0 191.0,156.2 191.0,149.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="200" y="124" width="130" height="58" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="265.0" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用内存</text>
<text x="265.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发 1001~2000</text>
<text x="265.0" y="172.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用完再取</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">快用完时后台预取下一段（双号段）</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UUID 无序，作主键 B+ 树随机插页</text>
</svg>
上半部分是雪花 64 位的分段：符号位、毫秒时间戳、机器号、序列号；下半部分是号段：数据库里的 `current_max_id` 从 1000 加到 2000，应用在内存里发 1001 到 2000。
**容易错。**
- **以为雪花不会重复：** NTP 或人工调时让时钟回拨会产生重复号：小幅回拨就等待追回，超过阈值拒绝发号，并持久化最后一次时间戳。10 位机器号最多 1024 个节点且必须唯一：用 ZooKeeper 临时节点、Redis 或数据库分配并带租约，租约要续期，否则重启的实例可能拿到别人的号。
- **以为号段 ID 是连续的：** 重启会丢掉没用完的号，有空洞，只保证不重复；用 `UPDATE ... SET current_max_id = current_max_id + step, version = version + 1 WHERE version = ?` 乐观更新取号，影响行数 0 说明被抢先要重试；双号段预取，消耗到约 10% 时后台取下一段，用完直接切换。
- **订单号完全连续：** 对手相减就能算出日单量，要加业务位或打散。
- **以为 UUID 做主键无所谓：** 无序、占 16 字节，插入 InnoDB 聚簇索引落在随机页上，页分裂、碎片、缓存命中下降，所有二级索引也跟着变大；分库分表后自增加步长扩容困难，所以用雪花或号段。

**业务场景。** 订单号既要唯一又不能被对手用相邻两单推算出日单量：用雪花生成，低位混入业务类型，不直接暴露自增序号。
