---
id: bagu-payment-idempotency-3-diff-body
node: a.idem.payment-idempotency
type: qa
step: 4
---
## Q
**支付幂等 · 相同幂等键但请求变了**｜追问

面试官：「同一个幂等键，第二次请求的金额变了，怎么办？」

## A
**基本回答。** 在保存幂等键的同时，保存首次请求的 `request_hash`（把关键参数算出来的哈希，相当于请求的指纹）。之后同一个键再来，算出新请求的指纹对比：一致就是同一个操作的重试，回放首次响应；不一致就返回 422，不执行也不回放，防止滥用。指纹取金额、币种、支付方式、订单号这类决定业务含义的参数。同键同内容回放首次响应，包括失败响应，想重新尝试必须换新键。
**2026 亮点。** 回放失败响应的副作用：首次若是 500，同键重试在保留期内一直拿到旧 500，换新键又失去去重；新做法是记录处理进度，同键重试时成功的步骤跳过、失败的接着做完，保留期可长到 30 天，代价是每一步都必须可续做。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="12" width="324" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">首次请求时存下 key=K1</text>
<text x="170.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">和 request_hash = 哈希(金额、币种、订单号…)</text>
<line x1="170" y1="54" x2="170" y2="68" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,68.0 166.8,61.0 173.2,61.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="68" width="140" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第二次来了 K1</text>
<line x1="170" y1="94" x2="56" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="56.0,116.0 62.3,111.5 63.5,117.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="94" x2="170" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,116.0 166.8,109.0 173.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="94" x2="284" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="284.0,116.0 276.5,117.8 277.7,111.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="118" width="104" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内容相同</text>
<text x="60.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回放首次响应</text>
<text x="60.0" y="169.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">含失败响应</text>
<rect x="118" y="118" width="104" height="64" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内容不同</text>
<text x="170.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">422</text>
<text x="170.0" y="169.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不执行不回放</text>
<rect x="228" y="118" width="104" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="139.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">首次还在处理</text>
<text x="280.0" y="154.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">409</text>
<text x="280.0" y="169.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">稍后再查</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">想重试一笔失败的扣款，要换新 key</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">key 保留期要比客户端最长重试时间长</text>
</svg>
同一个 key 再来时按三种情形分流：内容相同回放，内容不同 422（图中高亮），首次还没处理完是 409。
**容易错。**
- **同键不同内容直接按新内容执行：** 那等于让一个键对应两个不同的扣款，幂等就失效了。
- **把 409 和 422 混用：** 409 是还在处理中，422 是内容不同，客户端要根据状态码决定是等待还是修 bug。
- **指纹里放时间戳：** 重试时时间变了，哈希就不同，正常重试会被误判成内容不同。
- **保留期比重试窗口短：** 要比客户端最长重试时间长，常见 24 小时到 7 天；太短晚到的重试被当成新请求可能重复扣款，太长占存储。

**业务场景。** 客户端缓存了旧订单的幂等键，用户改了金额后重新提交；服务端发现 request_hash 不一致，返回 422，而不是按新金额扣款。
