---
id: bagu-rag-vector-index-1-hnsw-ivf-scale
node: b.agent.rag-vector-index
type: qa
step: 1
---
## Q
**向量索引 · HNSW、IVF 与千亿向量**｜追问

面试官：「HNSW 和 IVF 有什么区别？向量从 100 万涨到 1 亿，甚至 Milvus 里有一千亿个，索引怎么设计？向量库怎么选？」

## A
**基本回答。** 向量检索是近似最近邻（ANN，Approximate Nearest Neighbor），用一点召回损失换速度。HNSW 是多层图：上层大步跳，底层精细找，查询快、召回高而稳，缺点是内存大、构建慢。IVF 先用 K-Means 聚类分桶，查询只搜最近的几个桶，内存省、构建快，同召回下速度不如 HNSW。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 314">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">HNSW 多层图</text>
<text x="184" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">IVF 分桶</text>
<text x="8" y="48" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 2 层</text>
<line x1="60" y1="44" x2="150" y2="44" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 1 层</text>
<line x1="60" y1="94" x2="105" y2="94" stroke-width="1.2" stroke="currentColor"/>
<line x1="105" y1="94" x2="150" y2="94" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 层</text>
<line x1="60" y1="144" x2="82" y2="144" stroke-width="1.2" stroke="currentColor"/>
<line x1="82" y1="144" x2="105" y2="144" stroke-width="1.2" stroke="currentColor"/>
<line x1="105" y1="144" x2="128" y2="144" stroke-width="1.2" stroke="currentColor"/>
<line x1="128" y1="144" x2="150" y2="144" stroke-width="1.2" stroke="currentColor"/>
<line x1="60" y1="44" x2="60" y2="94" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="150" y1="44" x2="150" y2="94" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="94" x2="60" y2="144" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="105" y1="94" x2="105" y2="144" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="150" y1="94" x2="150" y2="144" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="60" y1="44" x2="150" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="150" y1="44" x2="150" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="105" y1="94" x2="150" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="105" y1="94" x2="105" y2="144" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="105" y1="144" x2="128" y2="144" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="60" cy="44" r="5.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="150" cy="44" r="5.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="60" cy="94" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="105" cy="94" r="5.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="150" cy="94" r="5.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="60" cy="144" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="82" cy="144" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="105" cy="144" r="5.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="128" cy="144" r="5.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="150" cy="144" r="5.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上层大步跳，下层精细找</text>
<circle cx="214" cy="56" r="30" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="214" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶 1</text>
<circle cx="292" cy="56" r="30" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶 2</text>
<circle cx="214" cy="128" r="30" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="214" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶 3</text>
<circle cx="292" cy="128" r="30" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="292" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶 4</text>
<circle cx="253" cy="56" r="3.5" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查询</text>
<text x="184" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只搜最近的 nprobe 个桶</text>
<text x="184" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">图中 nprobe = 2</text>
<line x1="8" y1="208" x2="332" y2="208" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">假设 768 维 float32，每条 3072 字节</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿条约 307GB，单机内存放不下</text>
<text x="8" y="264" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">千亿条约 307TB</text>
<text x="8" y="282" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">IVF-PQ 压到 64 字节一条：千亿约 6.4TB</text>
<text x="8" y="300" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">HNSW 全放内存，千亿不现实：磁盘索引（DiskANN）</text>
</svg>
左边高亮的是 HNSW 一次查询走过的路：从最上层开始大步跳，往下逐层变精；右边是 IVF：查询点只去最近的两个桶里找；底部是向量规模带来的内存账。
**容易错。**
- **以为 HNSW 在任何规模都更好：** 它内存大、构建慢，千亿级放不下；IVF-PQ 或磁盘索引才可行。
- **nprobe 越大越好：** 调大延迟和 CPU 都涨，调到等于桶数就是暴力全扫；在评测集上按召回目标找拐点。
- **按条数选向量库：** 条数不能单独决定选型，还看维度、过滤比例、QPS 和硬件；已有 PostgreSQL 且量不大用 pgvector，已有 Elasticsearch 就复用并叠加 BM25，要分布式扩展选 Milvus、Qdrant。
- **查询运算符和索引不匹配：** 运算符要与索引的 operator class 一致，否则不走索引。
- **压缩后不重排：** 量化会让召回略降，要用重排补回。
**举个例子。** 站内视频语义搜索，向量从 100 万涨到 1 亿：
1. 100 万条单机 HNSW 够用。768 维 float32 每条 3072 字节，1 亿条约 307GB（再加图的边），千亿约 307TB，单机放不下；按分区水平分片，各片查 Top K 再合并。
2. 改 IVF-PQ（乘积量化，向量切段用小码本近似），每条压到 64 字节：1 亿约 6.4GB，千亿约 6.4TB；HNSW 要把向量和图指针全放内存，千亿不现实，可考虑磁盘索引（如 DiskANN）。召回略降，用重排补回。
