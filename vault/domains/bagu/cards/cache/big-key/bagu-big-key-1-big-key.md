---
id: bagu-big-key-1-big-key
node: b.cache.big-key
type: qa
step: 1
---
## Q
**大 key · 危害、发现与处理**｜必会

面试官：「把某优惠券所有领取用户存进一个 Set，会有什么问题？大 key 怎么发现、怎么拆、怎么安全删除？」

## A
**基本回答。** 这会变成百万元素的大 key。经验上 String 超 10KB、集合超 5000 个元素或超 1MB 就要警惕，超 10MB 必须处理。危害：单次读写慢、阻塞单线程，占满网卡，删除和过期时释放内存卡顿，主从复制、集群迁移卡住，分片倾斜。处理：拆分（大 Hash 按 `hash(field) % N` 拆成 N 个小 Hash，大 List 按时间或序号分段）、压缩（gzip 或 snappy）、`UNLINK` 异步删除、分批删除（`SSCAN`、`HSCAN` 每次取几百个再 `SREM`、`HDEL`）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DEL：同步释放，主线程被占住</text>
<text x="10" y="41" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">主线程</text>
<rect x="60" y="24" width="270" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="195" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">释放 500 万成员（约 260MB）</text>
<text x="60" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">这百毫秒量级的时间里，其他请求全部排队</text>
<text x="10" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNLINK：先摘下，后台慢慢释放</text>
<text x="10" y="127" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">主线程</text>
<rect x="60" y="110" width="12" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="127" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">摘下，不到 1 毫秒</text>
<text x="10" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">后台</text>
<rect x="66" y="143" width="264" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="198" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后台线程释放内存，不挡请求</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">拆分：hash(field) % N，拆成 N 个小 Hash</text>
<text x="10" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分批：SSCAN/HSCAN，每批几百个 SREM/HDEL</text>
</svg>
第一条时间线里 `DEL` 把主线程占满，其他请求排队；第二条里 `UNLINK` 只在主线程上摘下 key，真正释放内存交给后台线程。
**容易错。**
- **在线上直接 DEL 大 key：** 它同步释放内存，会阻塞整个 Redis；要用 `UNLINK`。
- **在主库上跑 --bigkeys：** 虽然是 SCAN 采样，但要在从库上跑，避免影响主库；单个 key 用 `MEMORY USAGE`，也可离线分析 RDB（rdb-tools），不影响线上。
- **只管删不管写入：** 写入时不限制元素数，过一阵子又会长成大 key，要有 `LTRIM`、容量告警。
- **把所有评论、粉丝塞进一个 key：** 要分页或分段，只缓存最新一两页。
**举个例子。** 优惠券把所有领取用户存进一个 Set，一年后 500 万成员。从库上 `--bigkeys` 找到 `coupon:1001:users`，`MEMORY USAGE` 约 260MB。直接 `DEL` 主线程被占百毫秒量级，期间读写排队、监控出现延迟尖刺；`UNLINK` 不到 1 毫秒，后台线程慢慢释放。根治：按 `hash(userId) % 100` 拆成 100 个小 Set，每个约 5 万成员，写入前检查元素数，超限告警。
