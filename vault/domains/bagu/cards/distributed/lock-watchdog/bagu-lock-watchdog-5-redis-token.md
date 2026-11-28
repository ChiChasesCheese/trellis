---
id: bagu-lock-watchdog-5-redis-token
node: a.distributed.lock-watchdog
type: qa
step: 5
---
## Q
**Redis 能发严格单调的 token 吗 · 不引入 fencing 还有什么办法**｜追问

面试官：「Redis 能发出严格单调的 token 吗？如果不想引入 fencing，还有什么办法？」

## A
**基本回答。** Redis 做不到严格的 fencing。单实例 `INCR` 能递增，但主从是异步复制，主库宕机切换后，新主可能还没收到最近的计数，token 会回退。ZooKeeper 的事务号（zxid）、临时顺序节点序号，etcd 的 revision，由共识协议保证单调。不引入 fencing 时：让被保护的操作本身幂等，或用数据库乐观锁（`WHERE version = ?`）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 248">
<rect x="6" y="8" width="140" height="46" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="76" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧主库</text>
<text x="76" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数器 = 42</text>
<rect x="194" y="8" width="140" height="46" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="264" y="27.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库</text>
<text x="264" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数器 = 40</text>
<line x1="146" y1="31" x2="180" y2="31" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="180" y1="31" x2="187" y2="31" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="194,31 187,34.2 187,27.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="76" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">宕机</text>
<text x="170" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没赶上</text>
<line x1="264" y1="54" x2="264" y2="87" stroke-width="1.2" stroke="currentColor"/>
<polygon points="264,94 260.8,87 267.2,87" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="270" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升为新主</text>
<rect x="194" y="94" width="140" height="46" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="264" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新主库</text>
<text x="264" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INCR → 41</text>
<text x="8" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧持有者 A 用 42</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写过下游</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">下游见过最大 42：新持有者拿 41，</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合法的写被当成过期请求拒绝</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZooKeeper 的 zxid、etcd 的 revision</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">由共识协议保证单调，不会回退</text>
</svg>
旧主库已经发到 42，但异步复制还没把这个值送到从库（只有 40）。主库宕机、从库升为新主，再 `INCR` 就发出了 41，比下游见过的 42 还小，新持有者反而被拒绝。
**容易错。**
- **以为 `INCR` 返回递增就能当 fencing token：** 主从切换会丢最近的计数，值会回退。
- **以为 Redis 主从是强一致的：** 复制是异步的，确认写入不等于已到达从库。
- **不用 fencing 就什么都不做：** 至少要让操作幂等，或用乐观锁版本号兜底。
- **以为 ZooKeeper 和 Redis 一样：** ZooKeeper 的序号由共识协议保证，不会回退。

