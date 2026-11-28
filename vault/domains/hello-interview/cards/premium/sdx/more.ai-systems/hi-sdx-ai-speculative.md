---
id: hi-sdx-ai-speculative
node: more.ai-systems
type: qa
step: 5
---
## Q
**推测解码：多跑一个模型反而更快**｜补充 · AI 系统 · 加分

面试官：「推测解码每个请求多跑了一个模型，为什么反而更快？为什么输出质量不变？什么时候就没用了？」

## A
**结论。** 小的草稿模型先自回归提出 k 个 token，大模型用一次前向并行校验这 k 个，接受与自身分布一致的最长前缀，被拒位置由大模型重新采样。解码受带宽限制，校验 k 个和生成 1 个读权重的代价差不多，所以接受的 token 几乎免费；输出分布与只用大模型完全一致。

**要点。**
- **草稿模型：** 便宜，连续猜 k 个 token。
- **一次校验：** 大模型像预填充那样并行给这 k 个位置打分，只读一遍权重。
- **接受规则：** 精确的拒绝采样，接受一致的最长前缀，被拒位置从大模型分布重采样。
- **质量不变：** 输出分布严格等于大模型的分布，速度才是唯一变量。
- **什么时候失效：** 接受率低（草稿模仿不像，随机文本）；批量很大时 GPU 已经算力饱和，没有空闲算力去校验。
- **2026 亮点：** 主流引擎（如 vLLM）已支持草稿模型、n-gram、EAGLE、MTP 等多种方式，其中 EAGLE、MTP 这类模型方法延迟收益最好，标准拒绝采样在理论上无损。收益主要在低到中等 QPS 的延迟敏感场景，并发高时 batch 已吃满算力，收益会变小，要实测；论文里的 6.5 倍是最佳条件下的数字（SGLang 里 batch 64 时吞吐只提升约 1.38 倍），不要当生产预期。

**为什么。** 解码慢是因为每个 token 都要读一遍权重。一次读权重换回多个 token，就是在用空闲的算力换掉带宽等待。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="8" y="8" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">草稿模型</text>
<text x="83" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">便宜，连猜 4 个</text>
<rect x="182" y="8" width="150" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大模型</text>
<text x="257" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一次前向并行校验</text>
<polyline points="158,28 182,28" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="182,28 175.7,31.0 175.7,25.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">草稿提出的 4 个 token</text>
<rect x="8" y="88" width="72" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="44" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接受</text>
<rect x="88" y="88" width="72" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="124" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接受</text>
<rect x="168" y="88" width="72" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="204" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">接受</text>
<rect x="248" y="88" width="72" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拒绝</text>
<polyline points="284,122 284,150" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="284,150 281.0,143.7 287.0,143.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="150" width="152" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="256" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大模型重采样</text>
<text x="256" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 4 个位置</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一步读权重得到 4 个 token</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">输出分布与只用大模型完全一致</text>
</svg>

**面试里这样说。** 「草稿模型猜 k 个 token，大模型一次前向并行校验，接受一致的前缀。因为解码受带宽限制，校验 k 个和生成 1 个几乎一样快，而拒绝采样保证输出分布不变。批量大到算力饱和就没有收益。」

**易错。**
- **以为会降低质量：** 精确拒绝采样不改变输出分布。
- **草稿模型太大：** 草稿本身的开销吃掉收益。
- **高并发下仍开启：** 算力饱和时反而变慢。
