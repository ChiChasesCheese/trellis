---
id: bagu-no-loss-5-rabbit
node: a.mq.no-loss
type: qa
step: 5
---
## Q
**消息不丢 · RabbitMQ 的对应做法**｜追问

面试官：「如果用 RabbitMQ，三端分别对应什么机制？」

## A
**基本回答。** 生产端用发布确认（publisher confirms）；队列声明持久化（durable），消息 `delivery_mode=2`；消费端手动 ack（`autoAck=false`）。高可用用仲裁队列（quorum queue，基于 Raft），不用旧的镜像队列。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Kafka</text>
<text x="190" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RabbitMQ</text>
<rect x="8" y="24" width="140" height="48" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="78.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产端</text>
<text x="78.0" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">acks=all</text>
<line x1="148" y1="48" x2="190" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,48.0 183.0,51.2 183.0,44.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="190" y="24" width="142" height="48" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="261.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发布确认</text>
<text x="261.0" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">publisher confirms</text>
<rect x="8" y="84" width="140" height="48" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="78.0" y="104.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker</text>
<text x="78.0" y="119.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本 + ISR</text>
<line x1="148" y1="108" x2="190" y2="108" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,108.0 183.0,111.2 183.0,104.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="190" y="84" width="142" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="104.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列、消息都持久化</text>
<text x="261.0" y="119.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仲裁队列（Raft）</text>
<rect x="8" y="144" width="140" height="48" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="78.0" y="164.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费端</text>
<text x="78.0" y="179.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理完再提交 offset</text>
<line x1="148" y1="168" x2="190" y2="168" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,168.0 183.0,171.2 183.0,164.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="190" y="144" width="142" height="48" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="261.0" y="164.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">手动 ack</text>
<text x="261.0" y="179.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">autoAck=false</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">队列和消息两处都要持久化，否则重启丢</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">镜像队列已弃用，新系统用仲裁队列</text>
</svg>
左边是 Kafka 的三端机制，右边是 RabbitMQ 里对应的做法，一一对应。
**举个例子。** Webhook 投递队列放在 RabbitMQ。
1. **没设持久化：**消息放进队列，RabbitMQ 重启，`delivery_mode` 不是 2 的消息消失。
2. **改成持久化：**队列 durable，消息 `delivery_mode=2`，重启后消息还在。
3. **加仲裁队列：**一个节点坏了，其他节点上有多数派的副本，消息不丢。
4. **生产端：**发布确认到了才算发送成功，没确认就重发。
5. **消费端：**手动 ack，处理完才 ack；处理到一半崩溃，消息回到队列，另一个消费者重新收到。
**容易错。**
- **只设队列持久化或只设消息持久化：** 两处都要，否则重启丢。
- **用自动 ack：** 消息一到就算处理完，处理中崩溃就丢。
- **新系统还用镜像队列：** 已弃用，用仲裁队列。
- **把 confirm 和 ack 混为一谈：** confirm 管生产者到 Broker，ack 管 Broker 到消费者。
