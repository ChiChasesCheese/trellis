---
id: uth-gaps-heuristics-3-vllm-budget
node: gaps.heuristics
type: qa
step: 3
---
## Q
**一步推理里塞多少请求**｜vLLM · 0.32

GPU 每一步最多处理固定数量的 token。很多请求在排队：有的正在逐个生成，有的刚到、提示词很长。vLLM 每一步怎样挑？

## A
**背景。** 又是背包：每步有一个 token 预算，每个请求要若干 token，要尽量塞满，又不能让谁一直等。精确求解得知道未来来哪些请求，做不到。

**结构。** 每一步从 `token_budget`（默认等于 `max_num_batched_tokens`）往下扣：先给正在运行的请求各分一份（正在生成的通常只差 1 个 token），再按先来先到（默认 `fcfs`）从等待队列队首取请求，给它「需要的和剩余预算里较小的」个 token，预算用完就停。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="170" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">一步的 token 预算 (一步最多处理的 token 数)</text>
<rect x="20" y="30" width="300" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="30" width="26" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="33" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="46" y="30" width="26" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="59" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="72" y="30" width="26" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">1</text>
<rect x="98" y="30" width="222" height="32" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="209" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">队首请求的提示词 取一段</text>
<text x="20" y="84" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">先给正在生成的请求 通常各 1 个</text>
<text x="20" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">再按先来先到 给队首请求 min(需要, 剩余)</text>
<rect x="98" y="120" width="222" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="209" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">没做完的部分 下一步接着做</text>
<line x1="300" y1="64" x2="300" y2="112" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<path d="M300,118 L297,112 L303,112 Z" stroke="none" style="fill:var(--dim,#6b7280)"/>
</svg>
```

**细节。**

- 提示词太长，就只处理一段，剩下的下一步继续（分块预填充，chunked prefill）
- 关掉分块预填充时，队首放不下就直接停，不会跳过它去挑后面更小的

**为什么。** 先到先得、不跳队，简单也公平；代价是队首的大请求可能浪费预算，分块就是用来缓解它的。

**对应 LeetCode：** 无直接对应的题
