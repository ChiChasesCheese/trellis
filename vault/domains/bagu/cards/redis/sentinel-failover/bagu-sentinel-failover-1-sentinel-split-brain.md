---
id: bagu-sentinel-failover-1-sentinel-split-brain
node: b.redis.sentinel-failover
type: qa
step: 1
---
## Q
**哨兵 · 选主、故障转移与脑裂**｜追问

面试官：「哨兵怎么判断主库挂了、怎么选新主？机房网络分区时旧主还在接收写入，会怎样？」

## A
**基本回答。** 哨兵每秒 PING，超过 `down-after-milliseconds`（默认 30 秒）没有有效回复，该哨兵先标记主观下线（SDOWN）；达到 `quorum` 个哨兵同意，升为客观下线（ODOWN），多哨兵投票是为了避免单个哨兵网络问题造成误判。再选出一个哨兵 leader（要哨兵总数过半数授权）执行转移，挑新主：先排除掉线过久的从库，再比 `replica-priority` 小者优先、复制偏移量大者优先、`runid` 字典序小者优先；选定者执行 `REPLICAOF NO ONE`，其余从库改复制它。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<rect x="10" y="8" width="320" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单个哨兵：超过 30 秒无回复 → 主观下线</text>
<line x1="170" y1="32" x2="170" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,44 166.8,37 173.2,37" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="44" width="320" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">达到 quorum 个哨兵同意 → 客观下线</text>
<line x1="170" y1="68" x2="170" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,80 166.8,73 173.2,73" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="80" width="320" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过半数哨兵投票，选出 leader 执行转移</text>
<line x1="170" y1="104" x2="170" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,116 166.8,109 173.2,109" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="116" width="320" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选新主：priority 小 → 偏移量大 → runid 小</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">网络分区时的脑裂</text>
<rect x="8" y="178" width="140" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧主：被隔离</text>
<text x="78" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仍接收写入</text>
<line x1="170" y1="174" x2="170" y2="224" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="170" y="240" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区</text>
<rect x="192" y="178" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="194.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">哨兵 + 从库</text>
<text x="262" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">升出新主</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">恢复后旧主降为从库，隔离期间的写被丢弃</text>
<text x="8" y="280" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">缓解：min-replicas-to-write 1，只缩小窗口</text>
</svg>
上半部分是哨兵从发现主库没回话到选出新主的四步，高亮的是「多个哨兵都同意」这一步；下半部分是网络分区时的脑裂：旧主被隔离但还在接收写入，另一边已经升出了新主。
**业务场景。** 机房网络分区，旧主 M 被隔离但还活着，继续收了几秒写入；哨兵那边 3 个里 2 个同意（`quorum` 为 2），选 leader 拿到 2 票，从库 R1 偏移量更大被升主。网络恢复后 M 降为 R1 的从库，这几秒的写入被丢弃。配 `min-replicas-to-write 1` 加 `min-replicas-max-lag 10`（旧名 `min-slaves-*`），M 联系不上从库超过 10 秒就拒写，丢失窗口最多 10 秒。
**容易错。**
- **以为 quorum 就是选 leader 的票数：** `quorum` 只管判客观下线，选 leader 要过半数。
- **以为配了 min-replicas 就消除了脑裂：** 只缩小窗口，复制仍是异步，窗口内的写入仍可能丢。
- **以为切换后数据一定完整：** 新主可能还没收到旧主最后几条写入；基于 Redis 的锁在切换时可能丢，要靠 fencing token（单调递增令牌）兜底。
