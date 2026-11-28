---
id: bagu-selection-1-kafka-rabbit-rocket
node: b.mq.selection
type: qa
step: 1
---
## Q
**消息队列选型 · Kafka、RabbitMQ、RocketMQ**｜追问

面试官：「Kafka、RabbitMQ、RocketMQ 你怎么选？RocketMQ 的架构和事务消息是什么？」

## A
**基本回答。** 先看吞吐和是否要重放历史（选 Kafka）；再看有没有复杂路由、延迟、事务消息的刚需（RabbitMQ / RocketMQ）；最后看团队运维能力。
Kafka：分区日志、拉取、可重放，集群可到百万条/s；路由弱（topic + key），顺序只在分区内，事务只限 Kafka 内部，无原生延迟；适合日志、埋点、流处理；带 compaction 的 topic 可做变更日志源，但查询弱，不作主存储。RabbitMQ：交换机加队列、服务端推送、消费即删，万到十万条/s；路由强，无事务消息，延迟靠插件或 TTL 加死信交换机；适合业务异步、复杂路由。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="68" y="8" width="90" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="113" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<rect x="158" y="8" width="90" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="203" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RabbitMQ</text>
<rect x="248" y="8" width="92" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="294" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">RocketMQ</text>
<text x="10" y="64" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">模型</text>
<rect x="68" y="40" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区日志</text>
<text x="113" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拉取·可重放</text>
<rect x="158" y="40" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">交换机+队列</text>
<text x="203" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">推送·消费即删</text>
<rect x="248" y="40" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">类 Kafka</text>
<text x="294" y="69.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加 tag 过滤</text>
<text x="10" y="104" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">吞吐</text>
<rect x="68" y="80" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">百万条/s</text>
<text x="113" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群</text>
<rect x="158" y="80" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">万到十万</text>
<text x="203" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">条/s</text>
<rect x="248" y="80" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">十万级</text>
<text x="10" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">路由</text>
<rect x="68" y="120" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">弱</text>
<text x="113" y="149.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">topic+key</text>
<rect x="158" y="120" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">强</text>
<text x="203" y="149.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">四类交换机</text>
<rect x="248" y="120" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有 tag</text>
<text x="294" y="149.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过滤</text>
<text x="10" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">特性</text>
<rect x="68" y="160" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务限 Kafka</text>
<text x="113" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无原生延迟</text>
<rect x="158" y="160" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无事务消息</text>
<text x="203" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">延迟靠插件</text>
<rect x="248" y="160" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">半消息+回查</text>
<text x="294" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">原生延迟</text>
<text x="10" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">适合</text>
<rect x="68" y="200" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113" y="214.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志·埋点</text>
<text x="113" y="229.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流处理</text>
<rect x="158" y="200" width="90" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203" y="214.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务异步</text>
<text x="203" y="229.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">复杂路由</text>
<rect x="248" y="200" width="92" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="294" y="214.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">电商交易</text>
<text x="294" y="229.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">金融可靠</text>
<text x="10" y="252" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先看吞吐与重放，再看路由、延迟、事务</text>
</svg>
一张表看清三者：先横着看模型和吞吐，再看路由和特性，最后一行是各自适合的场景。
**举个例子。** 三个业务各选一个：
1. **埋点日志：** 每秒几十万条点击事件，要重放、要接流计算，选 Kafka。
2. **订单与支付状态流转：** 扣库存和下单要么都成功要么都不成，要事务消息和定时取消，选 RocketMQ。
3. **通知渠道路由：** 短信、邮件、推送按渠道和类型分发，延迟发送，选 RabbitMQ 的交换机。
4. **订单事务消息的过程：** 发半消息 → 执行本地事务（扣库存）→ 确认提交；如果确认没发出去，Broker 回查本地事务结果，再决定投递还是丢弃。
5. **最后看运维：** 如果团队只熟悉其中一种，而它又满足刚需，就先用它，不要为了「更合适」多养一套集群。
**容易错。**
- **只看吞吐就选 Kafka：** 它路由弱、无原生延迟、事务只限内部，业务场景可能不适合。
- **以为 RabbitMQ 吞吐不如 Kafka 就不能用：** 万到十万条/s 够大多数业务异步，路由强是优势。
- **把 Kafka 当主存储：** 它查询弱，不作主存储。
- **异步刷盘还想不丢消息：** 异步刷盘先回确认，宕机可能丢，要不丢选同步刷盘。
