---
id: bagu-cap-base-5-consistency-levels
node: a.distributed.cap-base
type: qa
step: 5
---
## Q
**一致性级别 · 最终一致靠什么实现**｜追问

面试官：「一致性有哪几个级别？最终一致具体靠什么机制实现？」

## A
**基本回答。** 从强到弱：强一致（写入后任何读都能读到）、最终一致（无新写入后，一段时间内收敛）、弱一致（不保证何时能读到）。中间还有读己所写、单调读、因果一致等会话级保证。最终一致靠：异步复制，加消息队列至少一次投递，加消费端幂等，加重试与补偿，再加定时对账修复。多副本存储靠读修复（Read Repair）、反熵（Anti-Entropy，后台同步）、Quorum 加速收敛：写副本数 W 加读副本数 R 大于总数 N，读写必有交集，如 N=3、W=2、R=2，读任意 2 个副本至少 1 个带新值，比较版本挑最新。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="8" y="24" width="76" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="46" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单成功</text>
<line x1="84" y1="44" x2="93.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100,44 93.0,47.2 93.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="24" width="98" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="149" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息队列</text>
<text x="149" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">至少一次投递</text>
<line x1="198" y1="44" x2="207.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214,44 207.0,47.2 207.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="214" y="24" width="118" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库存服务</text>
<text x="273" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">幂等扣减</text>
<line x1="273" y1="64" x2="273.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="273,92 269.8,85.0 276.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="214" y="92" width="118" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">失败：重试、补偿</text>
<line x1="273" y1="128" x2="273.0" y2="149.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="273,156 269.8,149.0 276.2,149.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="214" y="156" width="118" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">定时对账兜底</text>
<text x="8" y="100" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">至少一次会重复</text>
<text x="8" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">→ 消费端必须幂等</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单次失败总会发生</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">→ 要重试与对账</text>
</svg>
从左到右是一条消息的路：至少一次投递会重复，所以库存服务要幂等；失败了重试和补偿；最后用定时对账兜底。
**容易错。**
- **以为最终一致等于不一致：** 它承诺收敛，只是收敛前一段时间读到的值可能不同。
- **只做重试、没有幂等：** 至少一次投递会重复，重试越多重复越多，没有幂等就会重复扣减。
- **没有对账兜底：** 重试和补偿本身也可能出 bug 或漏掉，对账是最后一道防线。
- **不给收敛时间设上界：** 业务不知道要等多久，客服也无法回答「钱什么时候到」。
- **把读己所写当成强一致：** 它只保证自己读到自己写的，别人仍可能读到旧值。
**举个例子。** 下单成功发「扣库存」消息：投递了两次，库存服务按订单号去重只扣一次；库存服务挂了就等恢复后重试，重试仍失败走补偿取消订单；夜里对账发现订单已创建而库存没扣，以订单为准修正。
