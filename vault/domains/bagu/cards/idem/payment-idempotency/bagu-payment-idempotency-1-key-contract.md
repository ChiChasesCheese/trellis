---
id: bagu-payment-idempotency-1-key-contract
node: a.idem.payment-idempotency
type: qa
step: 1
---
## Q
**支付幂等 · 幂等键谁来生成、怎么传**｜必会

面试官：「设计一个扣款接口，重试不能重复扣。幂等键谁来生成？」

## A
**基本回答。** 幂等（idempotent）就是同一个操作做一次和做很多次，结果一样。扣款接口要做到这一点：由客户端为每一个逻辑上的一次扣款生成一个幂等键（放在请求头 `Idempotency-Key`，通常是 UUID），重试时必须带同一个键。服务端建一张表 `idempotency(key PRIMARY KEY, request_hash, status, response, created_at)`，把键设为主键，用来判断「这笔我见过没有」：`request_hash` 识别同一个键但内容变了（参数不同就报错），`response` 存第一次的响应供回放。没传键时可用订单号派生，并用部分唯一索引保证同一订单同一时刻最多一笔活跃支付。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<rect x="15" y="6" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端</text>
<rect x="235" y="6" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端</text>
<line x1="60" y1="32" x2="60" y2="176" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="280" y1="32" x2="280" y2="176" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="170" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣款 key=K1</text>
<line x1="62" y1="62" x2="278" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,62.0 271.0,65.2 271.0,58.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超时，响应没收到</text>
<line x1="278" y1="96" x2="62" y2="96" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="62.0,96.0 69.0,92.8 69.0,99.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重试：同一个 key=K1</text>
<line x1="62" y1="134" x2="278" y2="134" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="278.0,134.0 271.0,137.2 271.0,130.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回放第一次的结果</text>
<line x1="278" y1="172" x2="62" y2="172" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,172.0 69.0,168.8 69.0,175.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只扣了一次</text>
<text x="8" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">错：重试时换新 key → 被当成新请求，扣两次</text>
</svg>
第一次请求超时了，客户端不知道扣没扣；它用同一个 key 重试，服务端直接回放第一次的结果，只扣一次。
**容易错。**
- **键绑在每次请求上：** 键必须绑在逻辑操作上，一次扣款一个键；SDK 或网关重试时重新生成键，服务端就把重试当新请求，重复扣款。
- **让服务端生成键：** 服务端不知道哪次请求是重试，键必须由发起操作的客户端生成。
- **金额用 double：** 0.1 + 0.2 不等于 0.3，扣款金额要用整数分或 BigDecimal。
- **只靠客户端：** 客户端可能有 bug，服务端要再用订单号唯一约束做最后一道防线，保证同一订单不会重复支付。
**业务场景。** 用户点击支付，客户端生成 `K1` 存本地，`POST /pay` 带 `Idempotency-Key: K1`，100 元；服务端插入 `(K1, hash, PROCESSING)`，扣款成功置 `DONE` 并存响应，但响应丢了，客户端超时。重试仍带 `K1`，服务端直接回放，只扣一次；反例：SDK 重试时换成 `K2`，服务端当新请求，扣两次。
