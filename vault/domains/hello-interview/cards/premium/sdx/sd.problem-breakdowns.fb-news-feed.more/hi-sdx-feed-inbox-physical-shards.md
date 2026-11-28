---
id: hi-sdx-feed-inbox-physical-shards
node: sd.problem-breakdowns.fb-news-feed.more
type: qa
step: 1
---
## Q
**收件箱缓存拆成多个独立集群**｜补充 · Facebook 信息流 · 追问

面试官：「动态流的收件箱缓存每人保留 800 条、每条约 20 字节。日活从 2 亿涨到 20 亿，你是往现有的 Redis 集群里继续加节点，还是换个办法？为什么？」

## A
**结论。** 换办法：按 user_id 拆成多个物理上独立的集群，各自扩容、升级、恢复。容量只是起因，真正的理由是故障半径：一个超大集群出事，影响所有人；独立集群只影响它名下的那部分用户。

**要点。**
- **容量算式：** 2 亿 × 800 × 20 字节 ≈ 3.2 TB，20 亿就是约 32 TB。
- **实际更大：** 20 字节是原始数据，Redis 有序集合每个成员还有索引开销，实际内存常是数倍，要用实测值折算。
- **故障半径：** 单集群的一次故障转移、重分片、版本升级都影响全体用户；拆开后只影响约 1/N。
- **独立运维：** 每个集群可以单独灰度升级、单独扩容、单独恢复，出问题只回滚一个。
- **路由很简单：** 收件箱只按单个用户访问，用路由表把 user_id 映射到集群，不会有跨集群操作。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="10" y="8" width="320" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">动态服务</text>
<text x="170.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按 user_id 查路由表，选集群</text>
<polyline points="58,48 58.0,75.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="58,82 54.8,75.0 61.2,75.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="82" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="99.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群 A</text>
<text x="58.0" y="114.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">独立故障域</text>
<text x="58.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 1/3 用户</text>
<polyline points="170,48 170.0,75.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,82 166.8,75.0 173.2,75.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="122" y="82" width="96" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="99.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群 B</text>
<text x="170.0" y="114.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">独立故障域</text>
<text x="170.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 1/3 用户</text>
<polyline points="282,48 282.0,75.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="282,82 278.8,75.0 285.2,75.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="234" y="82" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="99.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群 C</text>
<text x="282.0" y="114.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">独立故障域</text>
<text x="282.0" y="129.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 1/3 用户</text>
<text x="10" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">集群 B 故障：只有它的用户走降级（读时合并），</text>
<text x="10" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">其余用户不受影响。</text>
<text x="10" y="210" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个集群独立扩容、升级、灰度、恢复；</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">访问只按单个用户，不会跨集群。</text>
</svg>

**为什么。** 单个集群越大，节点间的协调、重分片的搬迁量和一次事故的影响面都越大，增长到一定程度，加节点比拆开更危险。

**面试里这样说。** 「20 亿日活时收件箱按原始数据约 32 TB，实际内存更大。我不继续堆一个大集群，而是按 user_id 路由到多个独立的 Redis 集群，一个集群故障只影响约 1/N 的用户，并且可以单独升级和扩容；收件箱只按用户访问，所以没有跨集群操作。」

**易错。**
- **只讲容量：** 单集群放不下不是主要理由，故障半径和运维才是。
- **用固定取模分集群：** 集群数改变时几乎所有用户都要搬，应使用路由表或一致性哈希。
- **拆了集群没有降级路径：** 某个集群故障时，它的用户应退回读时合并，而不是报错。
