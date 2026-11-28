---
id: hi-sdx-dcache-shard-router
node: sd.problem-breakdowns.distributed-cache.more
type: qa
step: 2
---
## Q
**分片映射放在哪一层：客户端、代理还是协议**｜补充 · 分布式缓存（Redis） · 追问

面试官：「缓存集群的分片映射可以放在客户端库里、放在代理层（mcrouter 这类），或者像 Redis Cluster 那样写进协议。节点增减时，三种方式各让谁付代价？」

## A
**结论。** 客户端库省一跳，但每个进程都要及时更新拓扑；代理把映射集中到无状态代理层，应用最简单，但每个请求多一跳；Redis Cluster 把分片写进协议，客户端被重定向纠正，不需要代理，代价是迁移期多一次往返。

**要点。**
- **客户端库：** 映射内嵌在每个应用进程，延迟最低。拓扑变化要推送到所有进程，更新慢的进程会把请求发错节点，不同进程对同一个键的落点还可能不一致。
- **代理层：** 映射集中在无状态、可水平扩展的代理里，应用与语言无关，拓扑变化对应用透明，代理还能做连接池、复制和故障摘除。代价是多一次网络往返。
- **协议内：** 键哈希到 16384 个槽之一，客户端缓存槽表；发错节点会收到 -MOVED 告诉它正确节点，迁移中的槽用 -ASK。不需要代理，也不需要客户端预先知道全部拓扑。
- **怎么选：** 语言统一、拓扑稳定选客户端库；多语言、想集中控制选代理；直接用 Redis 就用 Cluster 协议。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 客户端库</text>
<rect x="10" y="22" width="140" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用 + 分片表</text>
<rect x="200" y="22" width="130" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="265.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存节点</text>
<polyline points="150,39 200,39" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="200.0,39.0 193.0,35.8 193.0,42.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="10" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 代理层</text>
<rect x="10" y="90" width="70" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="45.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用</text>
<rect x="108" y="90" width="100" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="158.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无状态代理</text>
<rect x="236" y="90" width="94" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="283.0" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存节点</text>
<polyline points="80,107 108,107" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="108.0,107.0 101.0,103.8 101.0,110.2" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="208,107 236,107" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="236.0,107.0 229.0,103.8 229.0,110.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="10" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ Redis Cluster 槽协议</text>
<rect x="10" y="158" width="60" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="40.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用</text>
<rect x="110" y="158" width="76" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="148.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 A</text>
<rect x="254" y="158" width="76" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292.0" y="179.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 B</text>
<polyline points="70,175 110,175" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="110.0,175.0 103.0,171.8 103.0,178.2" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="186,175 254,175" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="254.0,175.0 247.0,171.8 247.0,178.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="220" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">MOVED</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">映射放在谁手里，拓扑变化时谁来付代价</text>
</svg>

**面试里这样说。** 「我先问是不是多语言。多语言或想集中治理就放代理，多一跳换简单；用 Redis Cluster 就靠槽协议和 MOVED 重定向，不用代理；纯客户端分片延迟最低，但要保证所有进程的拓扑同步。」

**易错。**
- **说代理没有额外延迟：** 每个请求都多一次往返。
- **忽略客户端版本不一致：** 不同进程映射不同，命中率下降，还可能读到旧数据。
