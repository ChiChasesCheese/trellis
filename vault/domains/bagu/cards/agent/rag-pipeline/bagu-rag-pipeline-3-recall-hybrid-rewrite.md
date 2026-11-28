---
id: bagu-rag-pipeline-3-recall-hybrid-rewrite
node: a.agent.rag-pipeline
type: qa
step: 3
---
## Q
**召回 · 召回率低怎么排查，Hybrid Search 和 Query Rewrite 解决什么**｜必会

面试官：「RAG 召回率低，你怎么排查？Hybrid Search 和 Query Rewrite 各解决什么问题？」

## A
**基本回答。** 召回（Recall）是从知识库里把可能含答案的片段先捞出来。先看正确证据有没有进粗召回候选池（如 Top-50）。没有就依次查：文档是否入库且解析正确（PDF 解析成乱码就永远召不回）、Chunk 是否切断了关键事实、元数据过滤（租户、时间、版本）是否过严。再用两个手段补：
- Hybrid Search（混合检索）：向量召回补语义相近，BM25 关键词召回补错误码、型号这类精确词，两路用 RRF 按名次融合（名次换成 1/(k+名次) 再相加，因为两种分数尺度不同）。
- Query Rewrite（问题改写）：把「钱能退吗」补成「退款政策、退款条件」，常见有多查询、拆分子问题、HyDE（先生成假设答案再检索）；原始 Query 也保留参与召回。
**2026 亮点。** Chunk 脱离原文会丢主语（「该公司营收增长 3%」）而召不回：索引前让 LLM 给每块补全文上下文，再同时建向量和 BM25 索引、RRF 合并、重排；代价是索引时多一次 LLM 调用，知识库很小时直接塞进上下文更简单。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 318">
<rect x="60" y="8" width="220" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户问：钱能退吗？</text>
<line x1="170" y1="36" x2="170.0" y2="45.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,52 166.8,45.0 173.2,45.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="52" width="280" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="68.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Query Rewrite 补全问题</text>
<text x="170.0" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">退款政策、退款条件（原句也留着）</text>
<line x1="100" y1="92" x2="87.0" y2="110.3" stroke="currentColor" stroke-width="1.2"/>
<polygon points="83,116 84.4,108.4 89.7,112.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="92" x2="253.0" y2="110.3" stroke="currentColor" stroke-width="1.2"/>
<polygon points="257,116 250.3,112.1 255.6,108.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="116" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">向量召回</text>
<text x="83.0" y="149.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找意思相近的</text>
<rect x="182" y="116" width="150" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BM25 关键词召回</text>
<text x="257.0" y="149.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找 E1027 这类词</text>
<line x1="83" y1="160" x2="123.8" y2="180.8" stroke="currentColor" stroke-width="1.2"/>
<polygon points="130,184 122.3,183.7 125.2,178.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="257" y1="160" x2="216.2" y2="180.8" stroke="currentColor" stroke-width="1.2"/>
<polygon points="210,184 214.8,178.0 217.7,183.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="184" width="280" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RRF 按名次融合</text>
<text x="170.0" y="217.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">各路 1/(k+名次) 相加</text>
<line x1="170" y1="228" x2="170.0" y2="239.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,246 166.8,239.0 173.2,239.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="50" y="246" width="240" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="264.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">粗召回候选池（如 Top-50）</text>
<text x="8" y="300" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">正确答案不在池里，后面再怎么重排都没用</text>
</svg>
问题先被改写，再分两路并行召回，用 RRF 按名次合成一个候选池；答案不在池里，后面就无从补救。
**容易错。**
- **召回低就先调 Rerank：** 答案根本不在候选池里，重排无从补救；先查入库、解析、Chunk、过滤。
- **把 BM25 分和余弦分加起来：** 两者尺度不同，要用 RRF。
- **改写后丢掉原句：** 改写可能偏题，原始 Query 要一起参与召回。
- **Top-K 越大越好：** 扩大 Top-K 会拉高 Rerank 的输入量、提示词 Token 和噪声，三档上限要分开设：粗召回 30 到 100，重排后 5 到 10，进上下文 3 到 6。

**业务场景。** 运营问「渠道错误码 E1027 怎么处理」，纯向量召回的是泛泛的「支付失败排查」；加上 BM25 后，写有 E1027 的那条处理说明排进候选。
