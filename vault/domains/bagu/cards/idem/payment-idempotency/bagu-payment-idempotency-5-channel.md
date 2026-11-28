---
id: bagu-payment-idempotency-5-channel
node: a.idem.payment-idempotency
type: qa
step: 5
---
## Q
**支付幂等 · 对外部渠道调用的幂等**｜追问

面试官：「你调用外部支付渠道，怎么保证渠道侧也不重复扣？」

## A
**基本回答。** 调用外部支付渠道时，带上一个由我们自己生成、和订单一一对应的商户请求号，渠道按它去重；渠道返回超时的话，不要盲目重发，而是用同一个请求号去查询结果。
**一句话记住。** 商户请求号是我们和渠道之间的「同一张收据号」：不确定钱扣没扣，就拿这张收据号去问；问得到就是扣了，问不到才可以用同一个号再来一遍。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<rect x="15" y="6" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我们</text>
<rect x="235" y="6" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道</text>
<line x1="60" y1="32" x2="60" y2="220" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="280" y1="32" x2="280" y2="220" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="170" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣款 req_no=R1</text>
<line x1="62" y1="62" x2="278" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,62.0 271.0,65.2 271.0,58.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超时，结果未知</text>
<line x1="278" y1="96" x2="62" y2="96" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="62.0,96.0 69.0,92.8 69.0,99.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查询 req_no=R1</text>
<line x1="62" y1="134" x2="278" y2="134" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="278.0,134.0 271.0,137.2 271.0,130.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有记录：成功 → 入账</text>
<line x1="278" y1="172" x2="62" y2="172" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,172.0 69.0,168.8 69.0,175.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="14" y="193" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">或</text>
<text x="170" y="206" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查不到 → 同一个 R1 重发</text>
<line x1="62" y1="214" x2="278" y2="214" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,214.0 271.0,217.2 271.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">R1 贯穿去重、查询和对账文件</text>
</svg>
第一次扣款超时、结果未知；先用同一个请求号 R1 查询：渠道有记录就直接入账，查不到才用同一个 R1 重发。
**讲明白。**
- **为什么是商户请求号：** 我们的幂等键只管我们自己的服务；渠道是外部系统，它看不到我们的库，只认我们发给它的请求号。请求号稳定，重试和查询才有锚点。
- **请求号怎么生成：** 由我们在发起前生成并先落库，与订单一一对应，重试始终用同一个，不能每次重新生成。可以用订单号加业务类型，或雪花 ID（分布式下生成唯一编号的算法）。
- **超时意味着什么：** 超时只说明我们没收到响应，渠道那边可能已经扣了，也可能没扣；结果未知，所以不能直接当失败。
- **先查再决定：** 用同一个请求号查询：查到成功就入账；查不到，才可以用同一个请求号重发。
- **重发前要确认旧尝试终结：** 旧的那次请求可能还在渠道的处理队列里，要确认它已经终结（成功或失败），才能重发，否则可能重复扣款。
- **对渠道的要求：** 渠道要支持三件事：按请求号去重、按请求号查询、对账文件里包含请求号。
- **请求号保留多久：** 保留期要比最长重试窗口长。
- **渠道不支持去重怎么办：** 渠道不能按请求号去重或查询时，自动重发就有重复扣款的风险。做法：超时后不自动重发，先走对账文件或人工确认是否扣款；降低自动化程度，必要时换支持幂等的渠道。
**举个例子。**
1. **先生成并落库：**订单 O1 生成商户请求号 `R1`（比如订单号加业务类型 `pay`），先存库，再调渠道扣款 100 元。
2. 渠道很慢，我们的调用超时，订单卡在「处理中」。
3. 用 `R1` 查询：渠道返回「已扣款成功」，我们入账，订单置 `PAID`。
4. 另一种情形：用 `R1` 查询，渠道说「没有这个请求号」。确认旧尝试已经终结后，用同一个 `R1` 重发；即使旧请求这时才到，渠道也会按 `R1` 去重，只扣一次。
5. 反例：超时后换了新的请求号 `R2` 重发，渠道看不出是同一笔，扣两次。
**容易错。**
- **超时当失败：** 超时是结果未知，渠道可能已扣款，直接重发容易重复扣款。
- **每次重发换新请求号：** 渠道无法去重；请求号要稳定，重试始终用同一个。
- **请求号没落库：** 进程崩溃后，不知道之前用的是哪个号，没法查询。
- **以为所有渠道都支持去重：** 不支持时自动重发有风险，要走对账或人工。
**业务场景。** 渠道扣款超时，订单卡在处理中；用商户请求号查询，查到成功就入账，没记录就用同一请求号重发。
**系统设计。** [[links.tt-payment-reconciliation|支付对账系统（内部账本、PSP 结算文件、银行流水三方对账）]]：面试官问「内外两边怎么对上同一笔」，答商户请求号一一对应，对账文件里带着它。
**相关题。** 练习题 idempotent-transfer
**可能问法。**
- 对外调用怎么幂等？ → 调用渠道时带一个由我们生成、与订单一一对应的商户请求号，渠道按它去重；超时就用同一个请求号查询结果，查到成功就入账，查不到才用同一请求号重发。
- 请求号怎么生成？ → 由我们在发起前生成并先落库，与订单一一对应，重试始终用同一个，不能每次重新生成。可以用订单号加业务类型，或雪花 ID。保留期要比最长重试窗口长，对账文件里也要带它。
- 渠道不支持去重怎么办？ → 渠道不能按请求号去重或查询时，自动重发就有重复扣款风险。做法：超时后不自动重发，先走对账文件或人工确认是否扣款；降低自动化程度，必要时换支持幂等的渠道。
