---
id: bagu-rag-pipeline-2-chunk
node: a.agent.rag-pipeline
type: qa
step: 2
---
## Q
**Chunk · 切分策略怎么选，为什么不能只按固定长度**｜必会

面试官：「文档怎么切块？为什么不能一律按 512 个 Token 切？」

## A
**基本回答。** 切块（Chunk）是把长文档切成一小段一小段再建索引。先用固定长度（如 512 Token，重叠 50 到 100）跑出基线，再按文档特点升级：
- 递归字符切分：先按段落、再按句子，尽量保完整，通用文档的常用起点（400 到 800 Token，重叠 10% 到 15%）。
- 按结构切：Markdown 按标题，代码按函数，合同按条款。
- 父子分块：小块（约 200 到 400 Token）建索引提高匹配精度，命中后取所属大块（约 1000 到 1500 Token）给模型。
- 每块前加标题路径（文档名 > 章节 > 小节），避免指代丢失。
**2026 亮点。** 上下文检索（Contextual Retrieval）：索引前让 LLM 给每块补一两句来自全文的说明，再建向量和 BM25 索引；厂商基准里与重排合用，检索失败率从 5.7% 降到约 1.9%。代价是索引时多一次 LLM 调用、文档更新要重生成；知识库很小（约 20 万 token 内）直接全塞上下文更简单。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">固定 512 Token 一刀切</text>
<rect x="8" y="26" width="150" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块 A</text>
<text x="83.0" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">……除以下情况外：</text>
<rect x="182" y="26" width="150" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">块 B</text>
<text x="257.0" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">定制、虚拟商品……</text>
<line x1="170" y1="20" x2="170" y2="86" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">例外名单被切到了下一块</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">问「虚拟商品能退吗」→ 只召回块 A → 答「可以」</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">按条款切，并给每块加标题路径</text>
<rect x="8" y="174" width="324" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="196.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">退款规则 &gt; 七天无理由退货</text>
<text x="170.0" y="211.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">除定制商品、虚拟商品外可退</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">规则和例外在同一块，召回时一起带上</text>
</svg>
上半是固定长度切断例外名单，召回的块没有例外；下半按条款结构切，规则和例外同在一块。
**容易错。**
- **以为 512 Token 是标准答案：** 它只是跑基线的起点，最终要在自己的评测集上比较。
- **以为重叠越大越稳：** 重叠太大，Top-K 里全是重复内容，浪费上下文窗口；一般取块大小的 10% 到 15%。
- **以为所有内容都适合固定切：** 文本切块必须保住语义；表格拉平成纯文本会丢行列关系。
- **以为语义切分一定更好：** 它要对每句算 Embedding，离线成本高，还要限定最小和最大块长。
- **没有万能参数：** 用自己的评测集比较，看 Hit Rate（正确证据有没有被召回）和回答质量，选效果最好的。
**业务场景。** 退款规则写着「七天无理由退货，除以下情况外：定制商品、虚拟商品……」，例外列表被切到下一块；用户问虚拟商品能否退，召回的那块没有例外，模型答「可以」。按条款结构切并带上标题路径后解决。
