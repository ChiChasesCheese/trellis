---
id: bagu-rag-pipeline-4-rerank
node: a.agent.rag-pipeline
type: qa
step: 4
---
## Q
**Rerank · 重排解决什么问题，放在链路哪里**｜必会

面试官：「已经有向量召回了，为什么还要 Rerank？它放在哪一步？」

## A
**基本回答。** 向量召回衡量「表达像不像」，快但粗；Rerank（重排）用交叉编码器（Cross-Encoder）把问题和候选拼在一起编码，两者的词能互相看到，据此打分，判断「这段能不能回答这个问题」，把答案真正所在的片段排到最前。链路是：元数据过滤 → Hybrid 粗召回 30 到 100 条 → 去重合并 → Rerank 取 5 到 10 条 → 压缩后写入提示词。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="10" y="8" width="320" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">粗召回 30 到 100 条（向量加 BM25）</text>
<line x1="170" y1="38" x2="170.0" y2="47.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,54 166.8,47.0 173.2,47.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="50" y="54" width="240" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="73.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">去重合并</text>
<line x1="170" y1="84" x2="170.0" y2="93.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,100 166.8,93.0 173.2,93.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="70" y="100" width="200" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Rerank 取 5 到 10 条</text>
<line x1="170" y1="130" x2="170.0" y2="139.0" stroke="currentColor" stroke-width="1.2"/>
<polygon points="170,146 166.8,139.0 173.2,139.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="146" width="140" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="165.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">压缩后进提示词</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">向量排序：概述、入口……到账条款（第 5）</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重排之后：到账条款（第 1）</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只重排少量候选，因为交叉编码器每对都要现算</text>
</svg>
像漏斗一样逐级收窄：先便宜地多捞，再昂贵地精挑，最后压缩着放进提示词。
**容易错。**
- **以为 Rerank 能找回漏掉的文档：** 它只重排候选池里已有的，池里没有就无能为力。
- **以为 Rerank 可以替代向量召回：** 交叉编码器每一对都要现算，只能处理少量候选，海量文档仍要靠向量检索先取候选。
- **用 LLM 打分当通用方案：**又慢又贵，适合离线评估或低流量；通用链路用专用 Reranker 模型，时间、权限、版本这类确定条件用规则重排即可。
- **以为 Rerank 后就不用管 Top-N：** `rerank_top_n` 过小，或 Rerank 输入被截断，照样会丢掉答案。

**业务场景。** 用户问「退款多久到账」，向量召回前几名是「退款政策概述」和「退款入口」，真正写着到账时间的条款排第五；重排后排第一。
