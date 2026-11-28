---
id: bagu-llm-api-gateway-1-stream-limit-retry
node: b.agent.llm-api-gateway
type: qa
step: 1
---
## Q
**LLM 调用工程 · 流式、限流（RPM/TPM）、重试与模型网关**｜追问

面试官：「一次生产级 LLM 调用经过哪些环节？哪些错误能重试？限流为什么不能只按 QPS？模型供应商触发 TPM 限制怎么办？」

## A
**基本回答。** 请求先过网关：鉴权、预算与限流、选模型；再调供应商，用流式（SSE）把 Token 一段段推给前端；最后落库和计费。SSE 是 HTTP 上的单向事件流，复用现有网关、鉴权和代理，浏览器自带断线重连。重试只对瞬时错误（网络断、5xx、过载）做指数退避加抖动（`min(上限, base × 2^n) + 随机抖动`），429 先看 `Retry-After`，400、401、403 不重试。限流除了 RPM（每分钟请求数）还要 TPM（每分钟 Token 数），因为一次请求可大可小。
**2026 亮点。** 提示词缓存（Prompt Caching）是成本最大的一杠：不变的内容（工具定义、系统提示、知识文档）放前缀并打缓存断点，变化的输入放最后；命中读价约为基础输入价的 0.1 倍，写入有 1.25 到 2 倍溢价，前缀要字节级稳定（工具顺序固定、别放时间戳），TTL 内不命中就白付溢价；离线批处理再走 Batch API 省一半。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 304">
<rect x="8" y="14" width="70" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="116" y="14" width="112" height="64" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="172" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关</text>
<text x="172" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">鉴权、预算</text>
<text x="172" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限流、选模型</text>
<rect x="266" y="14" width="66" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="299" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">供应商</text>
<line x1="78" y1="34" x2="116" y2="34" stroke-width="1.2" stroke="currentColor"/>
<polygon points="116.0,34.0 109.0,37.2 109.0,30.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="228" y1="34" x2="266" y2="34" stroke-width="1.2" stroke="currentColor"/>
<polygon points="266.0,34.0 259.0,37.2 259.0,30.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="266" y1="60" x2="228" y2="60" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="228.0,60.0 235.0,56.8 235.0,63.2" style="fill:var(--accent,#3b6fd4)" stroke-width="0.5" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="116" y1="60" x2="78" y2="60" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="78.0,60.0 85.0,56.8 85.0,63.2" style="fill:var(--accent,#3b6fd4)" stroke-width="0.5" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SSE：Token 一段段推回</text>
<line x1="8" y1="112" x2="332" y2="112" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">限流为什么要看 Token</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求 A：约 500 Token</text>
<rect x="8" y="156" width="3" height="10" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求 B：约 8 万 Token</text>
<rect x="8" y="190" width="316" height="10" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">都只算 1 次请求，所以还要看 TPM</text>
<line x1="8" y1="234" x2="332" y2="234" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">哪些错误可以重试</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">可以：网络断、5xx、过载（退避加抖动）</text>
<text x="8" y="290" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">429：先看 Retry-After　不重试：400、401、403</text>
</svg>
上半部分是请求去、Token 流回的路径；中间两条横条的长度比约是 500 比 8 万，都算一次请求，所以只数请求数会严重失真；底部是重试的边界。
**容易错。**
- **只按 QPS 限流：** 一次请求可以是 500 Token，也可以是 8 万 Token，要同时看 RPM 和 TPM。
- **所有错误都重试：** 400、401、403 重试没用；429 要先看 `Retry-After`。
- **重试不设上限：** 最多 2 到 3 次，并设总截止时间。
- **重试不带幂等键：** 第一次可能已成功，会重复计费或写两条消息；用消息 ID 加尝试 ID，只让一次尝试成为最终结果。
- **相信「请返回 JSON」：** 要用 JSON Schema 或函数调用约束，仍要校验。
- **流式用 WebSocket：** 单向推 Token 用 SSE 就够了，更轻，也能复用现有网关。
**举个例子。** 大促客服对话量暴涨，供应商 TPM 触顶全是 429。一个带约 6000 Token 历史的请求，网关估算「输入 6000 加预留输出 1000」，从租户 TPM 预算扣 7000，扣不到就排队或降级到小模型。
- 429 按 `Retry-After` 等；5xx 退避 1 秒、2 秒加抖动；401 直接返回。
- 网关超时后重试，同一幂等键保证不重复计费。
