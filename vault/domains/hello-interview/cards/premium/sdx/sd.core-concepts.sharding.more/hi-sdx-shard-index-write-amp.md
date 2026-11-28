---
id: hi-sdx-shard-index-write-amp
node: sd.core-concepts.sharding.more
type: qa
step: 1
---
## Q
**全局二级索引的写放大**｜补充 · 分片（Sharding） · 追问

面试官：「分片的表上给 3 个属性建了全局二级索引（global secondary index）。插入一行、更新一行分别要多少次写？这会怎样影响你建索引的原则？」

## A
**结论。** 插入一行是 1 + k 次写（k 为索引数），每次索引写都落在与基础行不同的分片上。更新比插入更糟：每个被改动的被索引列，要在旧值下删一项、新值下加一项，也就是 2 次索引写。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">把邮箱从 a@x 改成 b@x（邮箱有全局索引）</text>
<rect x="10" y="60" width="112" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="66.0" y="81.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">基础行</text>
<text x="66.0" y="96.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据分片 P2</text>
<rect x="190" y="30" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="260.0" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">索引分片 Q5</text>
<text x="260.0" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">删旧项 邮箱=a@x</text>
<rect x="190" y="96" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="260.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">索引分片 Q9</text>
<text x="260.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加新项 邮箱=b@x</text>
<polyline points="122,78 183.3,58.2" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,56 184.3,61.2 182.4,55.1" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="122,94 183.4,115.7" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,118 182.3,118.7 184.5,112.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 次基础写 + 2 次索引写，落在 3 个分片；</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新增一行带 k 个索引：1 + k 次写。</text>
</svg>

**要点。**
- **插入：** 3 个全局索引就是 1 + 3 = 4 次写，分布在最多 4 个分片，通常是不同节点。
- **更新：** 改 1 个被索引列是 1 + 2 = 3 次写；同时改 c 个被索引列是 1 + 2c 次。
- **建索引的原则：** 只给真正会查的属性建索引。
- **投影的原则：** 只投影查询需要的属性。DynamoDB 的 KEYS_ONLY 和 INCLUDE 优于 ALL，因为被投影的每个属性在每次写入时都要再复制一份。
- **为什么是最终一致：** 要让索引写与基础行原子，每次写都要跨分片做分布式事务，规模上去后代价过高，所以系统让索引异步更新。

**面试里这样说。** 「全局索引不是免费的：每个索引让每次写多一次跨分片的写，改被索引列还要先删后加。所以我只给高频查询的属性建索引，投影只带需要的列，并接受索引是最终一致的。」

**易错。**
- **按读来想不按写来想：** 加了索引读变快了，但写吞吐按 1 + k 摊薄，写热的表更要克制。
- **把更新当成一次索引写：** 忽略旧项也要删除，改被索引列的成本翻倍。
- **投影选 ALL 图省事：** 存储和写入成本都随之上升。
