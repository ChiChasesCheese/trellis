---
id: bagu-delay-message-1-delay-impl
node: b.mq.delay-message
type: qa
step: 1
---
## Q
**延迟消息 · 各 MQ 怎么实现、订单超时取消用什么**｜追问

面试官：「订单 30 分钟未支付要自动取消，用消息队列怎么做？Kafka 没有延迟消息怎么办？」

## A
**基本回答。** Kafka 没有原生支持：按延迟档位建多个 topic（1s、10s、1min……），转发服务检查到期后写回目标 topic；或把任务存 Redis ZSet（score 是到期时间）/ 数据库，由调度器扫描。RabbitMQ 用 TTL + 死信交换机或延迟消息插件，RocketMQ 原生支持。
RocketMQ 4.x 是 18 个固定延迟级别（1s 5s 10s 30s 1m … 2h），5.x 支持任意时间的定时消息，用时间轮实现。时间轮：环形数组，每格一个时间刻度，指针每过一格执行该格任务，插入删除 O(1)，Kafka 内部的延迟操作（如 `acks` 超时）也用它。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">时间轮：8 格的环形数组</text>
<text x="78" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指针</text>
<line x1="78" y1="42" x2="78" y2="58" stroke="currentColor" stroke-width="1.2"/>
<polygon points="78,58 75.0,51.7 81.0,51.7" fill="currentColor"/>
<rect x="20" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="37" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="58" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="96" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="113" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="134" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="151" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="172" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="189" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="210" y="60" width="34" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="227" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="248" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="286" y="60" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="303" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="227" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 A 到期</text>
<line x1="303" y1="90" x2="303" y2="130" stroke="currentColor" stroke-width="1.2"/>
<line x1="37" y1="130" x2="303" y2="130" stroke="currentColor" stroke-width="1.2"/>
<line x1="37" y1="130" x2="37" y2="92" stroke="currentColor" stroke-width="1.2"/>
<polygon points="37,92 40.0,98.3 34.0,98.3" fill="currentColor"/>
<text x="170" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">指针转完一圈回到 0</text>
<text x="10" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Kafka：无原生，分档 topic 转发，或 Redis ZSet</text>
<text x="10" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RabbitMQ：TTL+死信交换机，或延迟插件</text>
<text x="10" y="200" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">RocketMQ：4.x 固定 18 档，5.x 任意时间</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">到期后要再查订单状态并做幂等</text>
</svg>
8 个格子的环形数组，指针每个刻度前进一格；订单 A 挂在高亮的第 5 格，指针转到那里就触发；转完一圈回到 0。
**举个例子。** 订单 30 分钟未支付要自动取消：
1. **下单：** 创建订单，同时登记一个「30 分钟后」的延迟任务（RocketMQ 5.x 延迟消息，或 Redis ZSet 里 `score = 当前时间 + 1800 秒`）。
2. **等待期间：** 用户 10 分钟时支付了，订单状态变成已支付；延迟任务不删除也没关系。
3. **到期触发：** 30 分钟到了，延迟消息被投递（或调度器扫描 ZSet 发现 score 已到）。
4. **再查状态：** 消费者先查订单：已支付就丢弃消息，未支付才取消订单并释放库存。
5. **重复触发：** 同一个到期消息被重复投递，取消逻辑做幂等（订单已取消就跳过）。
**容易错。**
- **以为 Kafka 有延迟消息：** 没有原生支持，要自己用分档 topic、ZSet 或数据库实现。
- **用一个 TTL 队列混放不同延迟：** 队头阻塞，TTL 长的挡住 TTL 短的。
- **到期后直接取消：** 用户可能已支付，必须先查状态并做幂等。
- **以为 RocketMQ 都能任意延迟：** 4.x 是 18 个固定级别，5.x 才支持任意时间。
