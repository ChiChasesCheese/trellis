---
id: bagu-distributed-kv-1-shard-replica-loss
node: b.scenario.distributed-kv
type: qa
step: 1
---
## Q
**分布式 KV 设计 · 分片、副本与故障切换的丢数据边界**｜追问

面试官：「用 10 台机器设计一个分布式 KV，key 是用户 UID，value 是一个二进制文件，要高可用、低延迟。主从异步复制，主节点挂了会丢什么？文件存储怎么保证不丢？」

## A
**基本回答。** 分片：一致性哈希或哈希槽把 UID 分到各机器，扩容只迁一小部分。副本：每片一主两从，读可走从库；心跳发现主挂了，把从库提升为主。丢数据的边界：异步复制下，主已确认给客户端、但还没传到从库的写，切换后会丢，这是低延迟的代价；要不丢就至少一个副本确认后再返回（半同步或多数派写），代价是延迟变高。脑裂：旧主被隔离后仍接受写，恢复后覆盖数据；用多数派选主、旧主降级，必要时带 fencing token。哈希分片只能点查，范围查询要用范围分片，代价是新数据集中在最后一片形成写热点。value 是大文件时，KV 只存元数据和位置，文件放文件存储：多副本（常见 3 份）、校验和发现静默损坏、后台巡检补副本，冷数据用纠删码（erasure coding）省空间。热点 key 用本地缓存或多副本分担读。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 288">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UID 经一致性哈希 / 哈希槽 → 分片</text>
<rect x="6" y="22" width="96" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54.0" y="36.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 1</text>
<text x="54.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一主两从</text>
<rect x="122" y="22" width="96" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="36.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 2</text>
<text x="170.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一主两从</text>
<rect x="238" y="22" width="96" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286.0" y="36.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 3</text>
<text x="286.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一主两从</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">异步复制：主已确认 w5，还没传到从库</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">主</text>
<rect x="44" y="92" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w1</text>
<rect x="74" y="92" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w2</text>
<rect x="104" y="92" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="117.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w3</text>
<rect x="134" y="92" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="147.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w4</text>
<rect x="164" y="92" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="177.0" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w5</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">从</text>
<rect x="44" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w1</text>
<rect x="74" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w2</text>
<rect x="104" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="117.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w3</text>
<rect x="134" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="147.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w4</text>
<rect x="164" y="122" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="177.0" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w5</text>
<text x="200" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还在路上</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">主宕机 → 从升主</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新主</text>
<rect x="44" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="57.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w1</text>
<rect x="74" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w2</text>
<rect x="104" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="117.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w3</text>
<rect x="134" y="178" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="147.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">w4</text>
<text x="172" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">w5 丢了 ✗</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">不丢已确认的写：至少一个副本确认再返回</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（半同步 / 多数派写），代价是延迟变高</text>
<text x="8" y="266" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">脑裂：多数派选主，旧主降级</text>
<text x="8" y="284" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">必要时带 fencing token</text>
</svg>
上半部分是 10 台机器上按 UID 分出的分片，每片一主两从。下面放大一片：主写了 w1 到 w5 并已确认，从库只收到 w1 到 w4；主宕机从库升主，w5 丢了。
**举个例子。** 用户上传头像：UID 哈希落分片 2，主库写元数据（文件位置）并确认，此刻是 w5；w1 到 w4 已传到从库，w5 还在途中，主宕机、从库升主，用户刚上传的头像映射没了。重要写入要求至少一个从库确认再返回，则升主的从库一定带有 w5。
**容易错。**
- **以为有从库就不丢数据：** 已确认但未复制的写会丢。
- **大文件直接存进 KV：** KV 只存元数据，文件放文件存储并多副本。
