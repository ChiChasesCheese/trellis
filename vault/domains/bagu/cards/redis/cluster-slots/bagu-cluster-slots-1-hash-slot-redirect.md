---
id: bagu-cluster-slots-1-hash-slot-redirect
node: b.redis.cluster-slots
type: qa
step: 1
---
## Q
**Redis Cluster · 哈希槽与重定向**｜追问

面试官：「排行榜只有一个 key，Cluster 怎么分？客户端打错节点会怎样，批量 MGET 为什么报错？」

## A
**基本回答。** 16384 个槽，`CRC16(key) mod 16384` 得槽号，每个主节点管一段连续的槽；扩缩容是整槽搬走，key 到槽的映射不变（不像「哈希除以节点数」加减节点几乎全部 key 换位置）。智能客户端本地缓存槽表直连目标节点。打错节点：MOVED（槽已永久迁走，更新槽表）；ASK（槽正在迁移，只这一次去目标节点，先发 `ASKING`，不更新槽表）。多 key 命令要求同槽，否则服务端不替你拆，报 `CROSSSLOT`；hash tag（只有 `{}` 里的部分参与哈希，如 `{u}:a`、`{u}:b`）可让相关 key 同槽，代价是挤在一个节点可能成热点。一个 key 永远只在一个槽，排行榜只有一个 key 时 Cluster 不会替你拆。16384 的由来：心跳包要带槽位图，16384 位只有 2KB，槽再多心跳更大，而集群建议不超过约 1000 个节点已够均匀。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<rect x="8" y="6" width="324" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CRC16(foo) mod 16384 = 12182</text>
<line x1="170" y1="30" x2="282" y2="54" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="282,54 274.5,55.7 275.8,49.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="6" y="56" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 A</text>
<text x="58" y="87.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0–5460</text>
<rect x="118" y="56" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 B</text>
<text x="170" y="87.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5461–10922</text>
<rect x="230" y="56" width="104" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="72.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 C</text>
<text x="282" y="87.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10923–16383</text>
<text x="8" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 客户端把 GET foo 发给节点 A（打错了）</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② A 回 MOVED 12182 → 节点 C</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 客户端更新槽表，之后直接发给 C</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">MGET a b c 槽不同 → CROSSSLOT 报错</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">{u}:a 和 {u}:b 槽相同 → 可以一起执行</text>
</svg>
`foo` 算出槽 12182 归节点 C；客户端误发给 A，A 不代办，回 MOVED 指向 C，客户端更新槽表后直连。
**业务场景。** 打赏榜按主播分 key 后批量 MGET 跨槽报 CROSSSLOT，把 key 改成 `{主播ID}:gift` 同槽后恢复，但大主播的所有 key 都压在一个节点上。
**容易错。**
- **以为 Cluster 会自动拆大 key。**
- **把 MOVED 和 ASK 当一回事。**
- **以为 hash tag 没代价。**
