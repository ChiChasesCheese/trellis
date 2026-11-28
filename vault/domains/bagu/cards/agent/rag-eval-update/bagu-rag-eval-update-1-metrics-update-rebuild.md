---
id: bagu-rag-eval-update-1-metrics-update-rebuild
node: b.agent.rag-eval-update
type: qa
step: 1
---
## Q
**RAG 评测与知识库更新 · 检索与生成分开评、增量与重建**｜追问

面试官：「RAG 评测要分哪两段，指标有哪些？知识库文档改版后，新旧版本同时被召回，怎么办？Embedding 模型升级为什么要重建索引？」

## A
**基本回答。** 评测分检索质量和生成质量，分开看才知道问题出在哪。检索指标：Hit@K（Top K 里有没有命中期望证据）、Evidence Recall@K（命中的证据数除以应有证据数）、MRR（Mean Reciprocal Rank，首个相关结果排名的倒数，再对多道题取平均）。生成看正确性、完整性、忠实度（回答有没有资料依据）和拒答。日常用增量更新：变更事件或 CDC 触发，加定时轮询对比 `content_hash` 兜底防漏检；只有换 Embedding 模型、改切分策略、改元数据结构、故障恢复才全量重建，用索引别名切换，新索引验证后切别名，旧索引留着回滚。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一题需要证据 A、B，检索取 Top 3</text>
<rect x="8" y="24" width="100" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 1 名</text>
<text x="58" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无关</text>
<rect x="118" y="24" width="100" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 2 名</text>
<text x="168" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">证据 A 命中</text>
<rect x="228" y="24" width="100" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 3 名</text>
<text x="278" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无关</text>
<text x="8" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">证据 B 没有出现在 Top 3 里</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Hit@3 = 1　Recall@3 = 1/2　RR = 1/2</text>
<line x1="8" y1="124" x2="332" y2="124" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">换模型重建索引，不停服切换</text>
<rect x="8" y="154" width="108" height="56" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="178.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">别名 docs</text>
<text x="62" y="193.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查询都走它</text>
<rect x="204" y="150" width="128" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">索引 v1（旧）</text>
<rect x="204" y="186" width="128" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="205" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">索引 v2（新）</text>
<line x1="116" y1="172" x2="204" y2="165" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204.0,165.0 197.3,168.7 196.8,162.4" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="116" y1="192" x2="204" y2="201" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<polygon points="204.0,201.0 196.7,203.5 197.4,197.1" style="fill:var(--dim,#6b7280)" stroke-width="0.5" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v2 在后台建好、通过评测集后，才把别名切过去</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">v1 保留一段时间，出问题立刻切回</text>
</svg>
上半部分用一道题算三个检索指标：命中一条不代表找全；下半部分是重建索引时靠别名切换，旧索引一直在服务。
**容易错。**
- **命中一条就当找全：** Hit@K 只看有没有命中，Recall 才看找全；要拿到两条证据，命中一条 Recall 只有 1/2。
- **把 MRR 和 Recall 当一回事：** MRR 看首个相关结果排多靠前，Recall 看证据找全没有。
- **只评最终答案：** 检索和生成要分开评，才知道问题出在哪。
- **库外问题也算 Recall：** 没有期望证据，Recall 不适用，要评拒答行为。
- **换模型只重算查询向量：** 不同模型的向量空间不通用，维度不同甚至插不进去，必须全量重建；元数据记录 embedding 模型、版本和维度，查询时校验。
- **更新只加新 chunk 不删旧的：** 旧版本继续被召回，答案前后矛盾；每个 chunk 带 `doc_id`、`version_id`、`content_hash`，更新时删旧版本，检索只取当前版本。

**业务场景。** 退款规则文档从 7 天改成 15 天，旧 chunk 没删，新旧同时被召回，Agent 回答前后矛盾；按 `doc_id` 加版本删除旧 chunk 即可。
