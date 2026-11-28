---
id: bagu-flash-sale-5-timeout-protect
node: a.scenario.flash-sale
type: qa
step: 5
---
## Q
**超时回补与限流削峰 · 保护链路**｜必会

面试官：「用户抢到后一直不付款，库存怎么回补？整条链路又怎么限流削峰保护？」

## A
**基本回答。** 抢到的人可能不付款，预扣的库存被一直占着，所以订单设支付时限（如 15 分钟），超时就关单并回补 Redis 和数据库库存，由延迟消息、Redis 有序集合（分数是到期时间）或定时扫描触发。回补必须幂等，否则消息重复投递会让库存凭空变多、超卖：用条件更新的影响行数当门锁，`UPDATE orders SET status = 'CLOSED' WHERE id = ? AND status = 'UNPAID'`，为 1 才回补，为 0 说明已关过。保护上，网关按用户、IP 限流，总放行量按库存放大有限倍数（库存 1000 放行约 1 万；比库存多是因为总有人不付款，也不能无限多，因为多数请求注定失败，越早拒绝越省资源）；写订单走消息队列削峰；过载时降级返回「排队中」或静态结果页，而不是让请求超时引发重试加剧过载。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="8" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">抢到</text>
<text x="56" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库存 -1</text>
<line x1="104" y1="44" x2="111.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118,44 111.0,47.2 111.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15 分钟未付</text>
<text x="166" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">延迟队列触发</text>
<line x1="214" y1="44" x2="221.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="228,44 221.0,47.2 221.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="228" y="24" width="104" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">条件更新</text>
<text x="280" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改为 CLOSED</text>
<line x1="270" y1="64" x2="237.4" y2="91.5" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232,96 235.3,89.0 239.4,93.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="294" y1="64" x2="298.7" y2="89.1" stroke-width="1.2" stroke="currentColor"/>
<polygon points="300,96 295.6,89.7 301.9,88.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="96" width="90" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="195" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">影响 1 行</text>
<text x="195" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回补库存 +1</text>
<rect x="250" y="96" width="82" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="291" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">影响 0 行</text>
<text x="291" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不回补</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重复投递的关单</text>
<text x="8" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">消息走右边</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回补不幂等 → 库存凭空变多</text>
</svg>
关单用条件更新当门锁：只有真的把「待支付」改成「已关闭」的那一次才回补库存，重复的消息改不动，也就不回补。
**举个例子。** 座位 S1 的订单 O1 抢到时 UNPAID、库存预扣 1。15 分钟没付，延迟队列发「关闭 O1」：第一次 UPDATE 影响 1 行，库存回补 1；同一消息重复投递，UPDATE 影响 0 行，不回补。没有 `status='UNPAID'` 这个条件，重复两次就回补两次，多卖出一个座位。
**容易错。**
- **回补前不看订单状态：** 见上，重复消息造成超卖。
- **放行量等于库存：** 有人不付款，库存可能卖不完。
