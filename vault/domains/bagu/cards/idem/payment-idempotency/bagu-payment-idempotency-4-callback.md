---
id: bagu-payment-idempotency-4-callback
node: a.idem.payment-idempotency
type: qa
step: 3
---
## Q
**支付幂等 · 支付回调重复到达**｜必会

面试官：「渠道把同一笔订单的支付成功回调了三次，怎么保证只入账一次？」

## A
**基本回答。** 渠道的回调（callback，支付成功后渠道主动调我们的接口通知结果）会带第三方交易流水号 `transaction_id`。回调记录表对它建唯一索引；订单状态只允许 `UNPAID → PAID` 这一次流转（`UPDATE ... SET status='PAID' WHERE status='UNPAID'`，早到的退款回调、晚到的成功回调不会把状态改乱，状态敏感时回调后主动查渠道取权威状态）；更新订单、写资金流水、写回调记录放在同一个事务里；重复的回调直接返回成功。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">渠道把同一笔订单的成功回调发了三次</text>
<rect x="8" y="30" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回调 1</text>
<line x1="82" y1="45" x2="118" y2="45" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,45.0 111.0,48.2 111.0,41.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="72" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回调 2</text>
<line x1="82" y1="87" x2="118" y2="87" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,87.0 111.0,90.2 111.0,83.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="114" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回调 3</text>
<line x1="82" y1="129" x2="118" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,129.0 111.0,132.2 111.0,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="26" width="108" height="124" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="172.0" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一索引</text>
<text x="172.0" y="84.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">transaction_id</text>
<text x="172.0" y="99.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">= T9</text>
<text x="172.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只放第一个过</text>
<line x1="226" y1="45" x2="252" y2="45" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="252.0,45.0 245.0,48.2 245.0,41.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="252" y="30" width="80" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292.0" y="49.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">入账一次</text>
<line x1="226" y1="100" x2="252" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252.0,100.0 245.0,103.2 245.0,96.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="252" y="76" width="80" height="60" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="292.0" y="95.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">撞索引</text>
<text x="292.0" y="110.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不入账</text>
<text x="292.0" y="125.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不报错</text>
<rect x="8" y="168" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="187.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">三次都回 success，渠道才会停止重试</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">入账事务：订单 UNPAID→PAID + 流水 + 回调记录</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先验签、核对金额，落库成功后再回应</text>
</svg>
同一笔订单回调了三次：第一次通过唯一索引入账一次；后两次被唯一索引拦住不入账，但三次都回复 success，渠道才会停止重试。
**容易错。**
- **重复回调返回失败：** 渠道会一直重试，最后越堵越多；重复回调要返回成功。
- **先应答后落库：** 如果先回了 success、再写库时失败，渠道不会再重发，这笔钱就丢了；要落库成功后再应答。
- **只靠唯一索引：** 唯一索引防重复入账，状态机条件更新防状态回退，两层各管一件事；返回失败只用于验签失败或金额与订单不一致。
- **不验签就处理：** 任何人都能伪造一个「支付成功」的回调。

