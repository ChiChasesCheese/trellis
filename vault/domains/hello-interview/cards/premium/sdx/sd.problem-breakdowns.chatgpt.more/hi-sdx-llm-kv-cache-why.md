---
id: hi-sdx-llm-kv-cache-why
node: sd.problem-breakdowns.chatgpt.more
type: qa
step: 1
---
## Q
**大模型怎么生成：预填充、解码与 KV 缓存**｜补充 · ChatGPT · 必会

ChatGPT 这类对话模型生成一段回答时，GPU 里实际在做什么？为什么说它「一个 token 一个 token 地生成」，而且要把前面每个 token 的中间结果一直留在显存里（KV 缓存）？预填充和解码分别指什么？

## A
**结论。** 模型每一步只产出一个新 token，而且必须看过前面所有 token。前面 token 的中间向量 K（键）和 V（值）不会随后面的内容改变，所以算一次存起来，这就是 KV 缓存；不存，每一步都要把整段前文重算一遍。处理提示叫预填充，之后逐个 token 生成叫解码。

**要点。**
- **逐个生成：** 下一个 token 要用上一个 token 作为输入，所以解码没法并行，只能一步一步来；这也是回答能边生成边流式输出的原因。
- **注意力要看全部历史：** 每一层里，新 token 拿自己的查询向量（Q）和前面每个 token 的 K 比对，再按比对结果加权取它们的 V。K、V 只取决于各自的 token，所以可以缓存。每层有多个注意力头，每个头各存一份 K、V；分组查询注意力让几个头共用一份，缓存就小几倍。
- **预填充：** 整段提示一次并行算完，把每个 token、每一层的 K 和 V 写进缓存，同时得出第一个输出 token。计算量大，受算力限制，决定首 token 延迟。
- **解码：** 每步只算 1 个新 token，计算量很小，但要把全部权重和整个缓存从显存读一遍，所以受显存带宽限制。
- **缓存的代价：** 大小随 token 数线性增长，会话存活期间一直占着显存。同时能服务多少会话，先被显存卡住，而不是算力。
- **2026 亮点：** 估并发先算 KV 缓存：大小正比于层数、KV 头数、head 维度、序列长度和并发数，所以选模型时要问 KV 头数。结构上 GQA 减少 KV 头数，更激进的 MLA 把 KV 压成低维 latent，同样显存能放更多并发。这是模型训练时就定下的结构，推理引擎补不回来。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="27" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">预填充</text>
<rect x="62" y="14" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="78" y="14" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="94" y="14" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="110" y="14" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="126" y="14" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="198" y="27" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提示一次并行算完</text>
<text x="8" y="67" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">解码 1</text>
<rect x="62" y="54" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="78" y="54" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="94" y="54" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="110" y="54" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="126" y="54" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="142" y="54" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="198" y="67" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读缓存，只算 1 个新的</text>
<text x="8" y="107" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">解码 2</text>
<rect x="62" y="94" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="78" y="94" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="94" y="94" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="110" y="94" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="126" y="94" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="142" y="94" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="158" y="94" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="198" y="107" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓存多一格，再读一遍</text>
<text x="8" y="147" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">解码 3</text>
<rect x="62" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="78" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="94" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="110" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="126" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="142" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="158" y="134" width="14" height="18" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<rect x="174" y="134" width="14" height="18" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="198" y="147" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每一步都读整个缓存</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每一格是一个 token 的 K 和 V（每层各一份）</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">亮格：这一步新写入的</text>
</svg>

**面试里这样说。** 「大模型一个 token 一个 token 地生成。提示先做预填充：并行算完整段，把每个 token 的 K 和 V 存进 KV 缓存；之后每步解码只算新 token，读缓存做注意力。缓存随长度线性增长，所以并发会话数先受显存限制。」

**易错。**
- **把 KV 缓存当成回答文本的缓存：** 它存的是每层每个 token 的中间向量，不是文字，也不能在不同模型之间复用。
- **以为解码和预填充一样受算力限制：** 解码每步计算量很小，慢在读显存。
