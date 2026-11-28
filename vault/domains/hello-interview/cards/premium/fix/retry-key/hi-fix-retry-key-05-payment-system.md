---
id: hi-fix-retry-key-05-payment-system
node: fix.retry-key
type: qa
step: 6
---
## Q
**支付系统 · 重试键**｜补强

面试官：「商户调你的 `POST /payment-intents` 超时了，它的重试逻辑会再发一次；你向卡组织发起扣款时也可能超时。键放哪里、长什么样、谁来生成？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **键在请求头里：** 「`Idempotency-Key: K`，写操作必须带，没带返回 400。商户在自己的订单行上先存好 K，再调我们；它自己崩溃重启后重发，用的还是订单行里的同一个 K。」
- **服务端怎么存：** 「`payments` 表 `UNIQUE (merchant_id, idempotency_key)`，同时存请求哈希、状态和返回给商户的结果。按商户隔离，因为两个商户可能随手选了同一个字符串。」
- **同键再来四种情况：** 「同键同内容已完成：原样返回，拒绝也原样返回。同键同内容还在处理：409，稍后重试。同键不同内容：422，不扣款。没带键：400。」
- **拒绝也要存：** 「余额不足被拒绝也是一个结果。之后同一个 K 再来时，用户刚好充了值，如果重新判断就会成功，同一个键两次得到不同结果。想重试要换新键。」
- **第二道边界：** 「我们向卡组织发起扣款，有自己的 `network_attempts` 表，每次尝试一个 `attempt_id`。超时重发用同一个 `attempt_id`；确认失败之后才开新的 attempt。」
- **超时怎么记：** 「超时的 attempt 标记为 pending_verification，不当成失败。后台任务用记录下的引用号去查卡组织，查清之前不换通道、不开新的 attempt。」
- **保留多久：** 「键至少保留到商户最长的重试窗口之后，比如几天，不能比商户的重试更短。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="8" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="28" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">商户服务器</text>
<text x="18" y="43" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先把键 K 存进自己的订单行</text>
<text x="18" y="58" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再调我们；重发永远是同一个 K</text>
<rect x="8" y="118" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="138" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">支付 API</text>
<text x="18" y="153" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UNIQUE (merchant_id, idempotency_key)</text>
<text x="18" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存请求哈希 + 状态 + 返回的结果</text>
<rect x="8" y="228" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="248" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">调卡组织：network_attempts 表</text>
<text x="18" y="263" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">attempt_id（超时重发用同一个）</text>
<text x="18" y="278" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">确认失败后才开新的 attempt</text>
<polyline points="170,70 170,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,118 166.8,111.0 173.2,111.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Idempotency-Key: K</text>
<polyline points="170,180 170,228" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,228 166.8,221.0 173.2,221.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">attempt_id</text>
</svg>
白板上：商户和我们之间一个键，我们和卡组织之间另一个键，每道边界一个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个键再来，按这四行处理</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同键 · 同内容 · 已完成</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原样返回，拒绝也原样返回</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同键 · 同内容 · 还在处理</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">409，稍后重试，不开第二个</text>
<rect x="8" y="130" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同键 · 内容不同</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">422，不扣款：客户端 bug</text>
<rect x="8" y="182" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="200.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">没带键的写请求</text>
<text x="18" y="215.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">400：写操作必须带键</text>
</svg>
白板上：同一个键再来的四种情况。

**为什么这样说。** 面试官要看的是：键是谁生成的、存在哪里、同键不同内容怎么办、每道外部边界是不是都有自己的键。弱的回答只说「用幂等键」，不说商户在哪里保存它；强的回答把键落到商户的订单行，把我们到卡组织那一层也单独设计一个键。
**面试官可能接着问。**
- 同键来了不同的请求体怎么发现？ → 存请求体的哈希（规范化后的金额、币种、商户引用），不一致返回 422。
- 第一个请求还在处理，第二个请求同时到了呢？ → INSERT 冲突后读到状态 PROCESSING，返回 409 让商户稍后重试，不开第二个。
- 键该由商户怎么选？ → 绑定业务对象：「订单 id + 第几次付款尝试」，或在订单行里存一个随机 UUID；不要用时间戳。
- 键过期之后同一个键又来了怎么办？ → 当成新请求会重复扣款，所以保留期要覆盖商户的最长重试窗口，更长的重试由商户的对账来补。
**常见失分。**
- **只做商户到我们这一层：** 我们到卡组织的重发没有稳定键，我们自己的重试会重复冻结。
- **拒绝不保存：** 同一个键两次得到不同结果。
- **超时当成失败：** 对方可能已经扣款，换新键重发就会重复扣。
- **键全局唯一不分商户：** 一个商户选的字符串能读到另一个商户的结果。
