---
id: bagu-rag-pipeline-6-graphrag
node: a.agent.rag-pipeline
type: qa
step: 6
---
## Q
**GraphRAG · 什么时候需要，什么时候别上**｜追问

面试官：「普通向量 RAG 不够用时，你会考虑 GraphRAG 吗？什么场景值得上？」

## A
**基本回答。** 向量 RAG 擅长答案集中在少数片段里的问题。GraphRAG 先从文档抽取实体和关系建成图，再沿关系检索，适合两类问题：需要多跳关系的（「A 系统的负责人参与过哪些支付链路的故障复盘」），以及要对整批文档做主题归纳的全局问题（对图里的社区做摘要来回答）。数据量小、问法简单、文档质量差、实时性要求高时，先把向量加 Hybrid 加 Rerank 做稳。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 258">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">向量 RAG：Top-K 是互不相连的碎片</text>
<rect x="8" y="26" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="58.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 介绍</text>
<rect x="120" y="26" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存使用规范</text>
<rect x="232" y="26" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="282.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">某次故障复盘</text>
<text x="8" y="80" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">连不起「Redis 异常影响哪些接口」</text>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GraphRAG：实体是点，关系是边</text>
<text x="104" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被依赖</text>
<text x="222" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被依赖</text>
<rect x="8" y="162" width="92" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54.0" y="183.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 集群</text>
<line x1="100" y1="179" x2="119.0" y2="179.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="126,179 119.0,182.2 119.0,175.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="162" width="92" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="172.0" y="183.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">商品缓存服务</text>
<line x1="218" y1="179" x2="237.0" y2="179.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="244,179 237.0,182.2 237.0,175.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="244" y="162" width="88" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="288.0" y="183.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付下单接口</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">沿关系走两跳，找出受影响的接口</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全局问题则靠社区摘要来回答</text>
</svg>
上半是向量 RAG 取回的互不相连的片段；下半是 GraphRAG 把实体连成图，沿「被依赖」关系走两跳找到受影响的接口。
**容易错。**
- **以为 GraphRAG 一定比向量 RAG 好：** 答案集中在少数片段的问题，向量 RAG 就够，GraphRAG 只会多花成本。
- **召回不好就直接上 GraphRAG：** 先看相关文本有没有进候选；没进候选，是 Chunk、Hybrid、Rerank 的问题，建图也救不了。
- **以为图建好就一劳永逸：** 文档更新时图和社区摘要都要同步更新。
- **不核对实体和关系抽取：** 实体抽错抽重、关系方向错，都会让答案系统性偏；依赖方向写反，走出来就是「Redis 依赖支付接口」。落地先做轻量图谱，只覆盖关系型失败样本多的部分。
**业务场景。** 「Redis 集群异常会影响哪些核心支付接口」：向量 RAG 只召回介绍 Redis 的文档，没有一篇把 Redis 和接口连起来；图里从 Redis 集群反向找依赖它的商品缓存服务（第 1 跳），再找依赖该服务的支付下单接口（第 2 跳）。
