---
id: hi-sdx-ch-rebalance-strategies
node: sd.core-concepts.consistent-hashing.more
type: qa
step: 1
---
## Q
**三种再平衡策略怎么选**｜补充 · 一致性哈希 · 追问

面试官：「分区再平衡常见三种做法：总分区数固定、动态分裂与合并、每个节点的分区数固定。它们各自让什么保持不变？你怎么选？」

## A
**结论。** 看哪个量被钉死。总数固定钉住分区个数，分区大小随数据变大；动态钉住分区大小，个数随数据增长；每节点固定钉住每个节点的分区数，新节点从别人手里切走区间。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">三种策略各钉死一个量</text>
<rect x="10" y="26" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">总数固定</text>
<rect x="114" y="26" width="216" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="222.0" y="50.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区个数不变</text>
<text x="222.0" y="65.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区大小随数据变大</text>
<rect x="10" y="90" width="96" height="56" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="122.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">动态分裂/合并</text>
<rect x="114" y="90" width="216" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="222.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区大小在上下界内</text>
<text x="222.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区个数随数据增长</text>
<rect x="10" y="154" width="96" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="186.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每节点固定</text>
<rect x="114" y="154" width="216" height="56" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="222.0" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每节点分区数不变</text>
<text x="222.0" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新节点随机切走别人的区间</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">定小了的固定总数，是后两种存在的原因。</text>
</svg>

**要点。**
- **总数固定：** Kafka 主题、Elasticsearch 索引的分片数。搬迁最简单，整分区换节点，键到分区的函数永不变；适合规模可预测的场景。
- **动态分裂合并：** HBase、CockroachDB。数据从 1 GB 到 100 TB 都不用重新规划，也是范围分区唯一能贴合键实际分布的办法。
- **每节点固定：** Cassandra 的虚拟节点。新节点随机切走其他节点的一段区间，分区大小跟每节点数据量成比例；随机切点只有对哈希后的键才公平，所以要哈希分区。
- **选择：** 规模可预测又求简单，选总数固定；规模难估或用范围分区，选动态；同质机器、逐步加机器的哈希集群，选每节点固定。

**面试里这样说。** 「如果能预估规模，我预先切好足够多的固定分区，搬迁只是改分区到节点的映射；范围分区或规模说不准，我用 HBase 那种动态分裂，让分区大小保持在界内。」

**易错。**
- **固定总数定得太小：** 数据超预期后它就是节点数的硬上限，这正是另外两种策略存在的原因。
- **把 Kafka 加分区当成无代价扩容：** 加分区会改变键到分区的映射，同一个键的顺序被打乱。
- **范围分区配每节点固定：** 随机切点在范围键上会切得极不均匀。
