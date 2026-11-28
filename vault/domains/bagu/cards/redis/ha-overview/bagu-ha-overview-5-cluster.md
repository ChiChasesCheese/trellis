---
id: bagu-ha-overview-5-cluster
node: a.redis.ha-overview
type: qa
step: 5
---
## Q
**Cluster · 怎么分片，槽怎么迁移，客户端怎么找到数据**｜追问

面试官：「Cluster 的数据怎么分到各节点？为什么是 16384 个槽？扩容怎么迁移，客户端怎么找数据？」

## A
**基本回答。** 槽号 = `CRC16(key) mod 16384`，每个主节点管一段槽，迁移最小单位是槽、不是 key（逐 key 搬只是手段）。客户端缓存槽映射直发；映射过期时节点重定向：`MOVED`（槽已永久迁走，客户端更新映射）、`ASK`（槽迁移中，只此一次去目标节点，先发 `ASKING`，不更新映射）。16384 的由来：心跳包要带槽位图，16384 位正好 2KB，65536 个槽就 8KB，而集群建议不超过约 1000 个节点已够均匀。迁一个槽：源标 migrating、目标标 importing，`MIGRATE` 逐 key 搬，完成后更新归属并广播，`redis-cli --cluster reshard` 自动化。节点用 gossip（PING/PONG）走集群总线端口（服务端口加 10000）交换状态；主节点被多数主节点判不可达（`cluster-node-timeout` 默认 15 秒），其从节点发起选举，多数主节点投票后接管槽。`cluster-require-full-coverage yes`（默认）时有槽无主整个集群拒服务。多键命令要同槽，用哈希标签 `{user:1}:cart` 只对大括号内算槽；只支持 0 号库。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="8" y="8" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key</text>
<line x1="68" y1="23" x2="84" y2="23" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84,23 77.0,26.2 77.0,19.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="84" y="8" width="170" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CRC16(key) mod 16384</text>
<line x1="254" y1="23" x2="270" y2="23" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270,23 263.0,26.2 263.0,19.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="270" y="8" width="62" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="301" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽 N</text>
<text x="8" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16384 个槽，例：3 个主节点平分</text>
<rect x="8" y="74" width="108" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 A</text>
<text x="62" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0–5460</text>
<rect x="116" y="74" width="108" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 B</text>
<text x="170" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5461–10922</text>
<rect x="224" y="74" width="108" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 C</text>
<text x="278" y="107" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10923–16383</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">映射过期时，节点返回重定向：</text>
<rect x="8" y="152" width="158" height="76" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="87" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MOVED</text>
<text x="87" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽已永久迁走</text>
<text x="87" y="201" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端更新映射</text>
<text x="87" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">之后直接发新节点</text>
<rect x="174" y="152" width="158" height="76" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ASK</text>
<text x="253" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">槽正在迁移中</text>
<text x="253" y="201" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先发 ASKING 再重试</text>
<text x="253" y="216" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不更新映射，只此一次</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">{user:1}:cart 只对大括号内算槽，保证同槽</text>
</svg>
key 算出槽号，槽落在哪个节点的区间就归谁；发错节点收到 MOVED 或 ASK，作用不同。
**业务场景。** 同一场直播的礼物榜和观众榜要在一个 Lua 里原子更新，key 设成 `{room:123}:gift`、`{room:123}:fan` 落同一槽；但别让所有大房间共用同一标签，否则压力又集中到一个节点。
**容易错。**
- **把 MOVED 和 ASK 混为一谈。**
- **以为迁移单位是 key。**
- **所有大房间共用同一个哈希标签。**
