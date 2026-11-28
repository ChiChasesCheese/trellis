---
id: bagu-ordering-1-same-key
node: a.mq.ordering
type: qa
step: 1
---
## Q
**消息顺序 · 同 key 同分区**｜必会

面试官：「同一个订单的创建、支付、发货消息必须按序处理。Kafka 怎么保证顺序？全局有序可行吗？」

## A
**基本回答。** Kafka 只保证分区内有序、分区间无序。同一订单号做 key，哈希到同一分区，就保证这个订单内有序。全局严格有序只能一个分区，吞吐降到单分区水平，通常不是好设计。
发送时指定 partition 则全发到该分区，指定 key 则对 key 取哈希再对分区数取余，推荐用 key。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<text x="160" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash(订单号) % 分区数</text>
<rect x="8" y="24" width="96" height="24" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="40.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单A 创建</text>
<line x1="104" y1="36" x2="214" y2="36" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214.0,36.0 207.0,39.2 207.0,32.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="54" width="96" height="24" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单A 支付</text>
<line x1="104" y1="66" x2="214" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214.0,66.0 207.0,69.2 207.0,62.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="84" width="96" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单A 发货</text>
<line x1="104" y1="96" x2="214" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214.0,96.0 207.0,99.2 207.0,92.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="114" width="96" height="24" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单B 创建</text>
<line x1="104" y1="126" x2="214" y2="126" stroke-width="1.2" stroke="currentColor"/>
<polygon points="214.0,126.0 207.0,129.2 207.0,122.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="214" y="24" width="118" height="80" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273.0" y="45.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P1</text>
<text x="273.0" y="60.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单A 创建</text>
<text x="273.0" y="75.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单A 支付</text>
<text x="273.0" y="90.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单A 发货</text>
<rect x="214" y="112" width="118" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="273.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0</text>
<text x="273.0" y="144.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单B 创建</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同 key → 同分区 → 分区内有序</text>
<text x="8" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区间没有顺序；全局有序只能 1 个分区</text>
<text x="8" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">key 选订单号或会话 ID，缩小有序范围</text>
</svg>
订单 A 的三条消息（创建、支付、发货）都被哈希到同一个分区 P1，在里面按到达顺序排好；订单 B 去了另一个分区，和 A 之间没有顺序。
**举个例子。** topic 有 3 个分区，订单 A 的 key 哈希后对 3 取余得到 1。
1. **订单 A 创建：**key=A，进 P1，offset 0。
2. **订单 A 支付：**key=A，进 P1，offset 1。
3. **订单 A 发货：**key=A，进 P1，offset 2。
4. **订单 B 创建：**key=B，哈希后取余得 0，进 P0，offset 0。
5. **消费者读 P1：**按 0、1、2 的顺序读，发货一定在支付之后。
6. **A 和 B 之间：**没有顺序保证，也不需要。
**容易错。**
- **以为 Kafka 整个 topic 有序：** 只有分区内有序。
- **为了全局有序只建一个分区：** 吞吐降到单机水平，不是好设计，应该缩小有序范围。
- **只做到同 key 同分区就以为万事大吉：** 还要防生产端重试乱序、消费端多线程乱序、分区数变化。
- **随便选 key：** key 要选需要有序的业务实体（订单号、会话 ID），选错了该有序的消息被拆到不同分区。
