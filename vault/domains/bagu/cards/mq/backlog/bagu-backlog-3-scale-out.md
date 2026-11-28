---
id: bagu-backlog-3-scale-out
node: a.mq.backlog
type: qa
step: 3
---
## Q
**消息积压 · 消费者已等于分区数怎么扩**｜必会

面试官：「消费者数已经等于分区数，还是处理不过来，怎么扩？」

## A
**基本回答。** 写一个临时消费者，快速把消息只转发（不处理）到分区数 10 倍的临时 topic，再起 10 倍的消费者去消费临时 topic；低价值消息直接丢弃或降级。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="8" y="8" width="170" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="93" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">原 topic（N 个分区）</text>
<rect x="8" y="62" width="170" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="93" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">转发消费者</text>
<rect x="8" y="116" width="170" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="93" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">临时 topic（10N 分区）</text>
<rect x="8" y="170" width="170" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="93" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10N 个业务消费者</text>
<line x1="93" y1="42" x2="93" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,62.0 89.8,55.0 96.2,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="93" y1="96" x2="93" y2="116" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,116.0 89.8,109.0 96.2,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="93" y1="150" x2="93" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,170.0 89.8,163.0 96.2,163.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="190" y="29" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加实例也没用</text>
<text x="190" y="83" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只搬运不处理，所以快</text>
<text x="190" y="137" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同 key 仍同分区</text>
<text x="190" y="191" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">追平后恢复原架构</text>
</svg>
左边四格是一条从上到下的流水线：原 topic 的消息先被转发消费者原样搬到十倍分区的临时 topic，再由十倍数量的业务消费者处理。关键在第二格：它只搬运、不做业务，所以单个实例就能搬得很快。
**举个例子。** 积压 6000 万条，消费 5000 条/秒，生产 3000 条/秒：
1. **原来能追平吗：** 净消化 5000 − 3000 = 2000 条/秒，6000 万 ÷ 2000 = 3 万秒，约 8.3 小时。
2. **扩到 2 万条/秒：** 净消化 2 万 − 3000 = 1.7 万条/秒，6000 万 ÷ 1.7 万 ≈ 3529 秒，约 59 分钟。
3. **怎么扩：** 原 topic 假设 8 个分区、8 个消费者已经满员；转发到 80 个分区的临时 topic，起 80 个业务消费者，单分区速度不变，理论上整体能力约放大到 10 倍（5 万条/秒），超过目标 2 万条/秒；实际取决于下游能否承受。
4. **收尾：** 积压追平后，生产流量切回原 topic 的原架构，撤掉临时部分。
**容易错。**
- **以为加消费者实例就行：** 超过分区数的实例拿不到分区，纯属浪费。
- **以为转发消费者也要处理业务：** 它只搬运，业务处理在临时 topic 的新消费者里，所以转发这一步很快。
- **算追平时间忘了减生产：** 用积压量直接除以消费速度会低估时间，生产速度也在往里加。
