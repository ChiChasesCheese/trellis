---
id: hi-fix-component-cost-10-wallet-kafka
node: fix.component-cost
type: qa
step: 10
---
## Q
**Airbnb Wallet · Kafka 加还是不加**｜补强

面试官：「支付平台的 webhook 进来之后，你打算直接写数据库，还是先放进 Kafka？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说不加的版本：** 「webhook 到服务，验签，一个事务改交易状态和钱包，直接写 Postgres。」
- **数字：** 「每笔转账一个 webhook，峰值 16.5 × 3 ≈ 50 笔/秒；单主库的简单写是每秒数千次（调优后约 2 万次），余量几十倍。」
- **Kafka 的三句：** 「作用是缓冲：平台的更新来得比数据库写入者能安全处理的快，或更新服务宕机时不丢。代价是延迟、重复投递和多一套要运维的系统。我在 webhook 持续超过写库余量，或更新服务宕机时必须不丢更新，或多个下游要订阅同一份状态变化时才加。」
- **代价逐项给处理办法：** 「延迟：多一段，积压时更长，监控消费滞后。重复：按平台的 event_id 去重，去重记录和状态更新同一个事务。乱序：按 transfer_id 分区，状态更新是 WHERE status = 'pending' 的条件更新。运维：broker 副本、告警。」
- **「宕机不丢」是第二个触发，但有条件：** 「更新服务宕机时不丢平台的更新，本身是该加的理由。这里平台会重发 webhook 一段时间，每日扫描又按 vendor id 补查，丢的是时间，不是数据；所以只有平台不重发，或产品要求几分钟内恢复，这条才成立，那时我加。」
- **留一句给扩展：** 「规模再大 100 倍，webhook 到 5,000 笔/秒，我会在 webhook 和 Postgres 之间加 Kafka。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">现在：webhook 直接写 Postgres</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付平台 webhook</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">峰值 50 笔/秒</text>
<polyline points="170,70 170,92" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,92 166.8,85 173.2,85" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="92" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">钱包服务</text>
<text x="170" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">验签，一个事务改状态和钱包</text>
<polyline points="170,136 170,158" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,158 166.8,151 173.2,151" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="158" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Postgres</text>
<text x="170" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">简单写数千次/秒，余量数十倍</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发之后：中间加 Kafka</text>
<rect x="8" y="26" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">webhook 接收：验签，写 Kafka，立刻 200</text>
<polyline points="170,55 170,85" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,85 166.8,78 173.2,78" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 transfer_id 分区</text>
<rect x="8" y="85" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<text x="170" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：延迟、重复、乱序、运维</text>
<polyline points="170,129 170,151" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,151 166.8,144 173.2,144" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="151" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">更新服务：按 event_id 去重</text>
<text x="170" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">条件更新，一个事务</text>
<polyline points="170,195 170,217" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,217 166.8,210 173.2,210" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="217" width="324" height="29" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="235.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Postgres</text>
</svg>
白板上：先画不带 Kafka 的三个框，Kafka 的版本画在旁边，标「触发后」。
**为什么这样说。** （约 1 分钟。）面试官要确认你不是在背「异步用消息队列」。强的回答给出不加的版本、数字和触发条件，并且把代价逐项配上办法；弱的回答是「用 Kafka 保证不丢、解耦」。
**面试官可能接着问。**
- 平台只重发 1 小时，扫描一天一次，中间不是有缺口吗？ → 缺口是 24 小时内恢复；如果要求更紧，先把每日扫描改成每小时，或把 webhook 先落进 Postgres 的收件箱表再处理，作用相同，少一个系统。
- 需要通知、风控也订阅状态变化呢？ → 这就是第二个触发：多个下游订阅同一份事件，才值得一个日志；也可以先用 outbox 加一个队列。
- 加了 Kafka 之后，钱包余额会不会错？ → 不会：重复被 event_id 挡住，乱序被条件更新挡住；但余额的更新会晚几秒，页面显示 last_checked_at。
**常见失分。**
- **「保证不丢」当理由：** 没说丢在哪，也没说平台重发和扫描已经覆盖了。
- **加了不处理重复：** 同一个 webhook 处理两次，余额改两次。
- **一上来就画：** 没有不加的版本，也没有数字。
