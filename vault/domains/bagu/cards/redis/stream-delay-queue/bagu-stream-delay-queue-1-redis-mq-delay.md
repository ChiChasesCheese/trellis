---
id: bagu-stream-delay-queue-1-redis-mq-delay
node: b.redis.stream-delay-queue
type: qa
step: 1
---
## Q
**Redis 做队列与延时任务 · List、Pub/Sub、Stream**｜追问

面试官：「订单 30 分钟未支付自动取消，能用 Redis 的过期事件监听吗？Redis 能当消息队列吗，Stream 解决了什么？」

## A
**基本回答。** List（`BLMOVE`，旧名 `BRPOPLPUSH`）简单但没有消费确认，取走后消费者崩了 Redis 不知道没处理完；Pub/Sub 不持久化，订阅者离线就丢；Stream（5.0+）有消费组，`XREADGROUP` 读到的消息进待确认列表（PEL），`XACK` 后才移除，消费者宕机可用 `XAUTOCLAIM`（6.2+）认领超时未确认的消息。延时任务用 ZSet（score 是到期时间戳，`ZRANGEBYSCORE` 取 score 不大于当前时间的）或 Redisson 延迟队列，不要靠过期事件监听：事件只在 key 真正被删时发布，而删除是惰性加定期的，时效无保证；它走 Pub/Sub，没人订阅就丢，多实例订阅会重复消费；`notify-keyspace-events` 默认为空。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ZSet：score = 到期时间戳，从小到大排</text>
<rect x="8" y="22" width="76" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 A</text>
<text x="46" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">score 1000</text>
<rect x="88" y="22" width="76" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 B</text>
<text x="126" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">score 1005</text>
<rect x="168" y="22" width="76" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="206" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 C</text>
<text x="206" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">score 1030</text>
<rect x="248" y="22" width="76" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单 D</text>
<text x="286" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">score 1100</text>
<line x1="166" y1="20" x2="166" y2="78" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="166" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">now = 1010</text>
<line x1="86" y1="60" x2="86" y2="108" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="86,108 82.8,101 89.2,101" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="108" width="172" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="94" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZRANGEBYSCORE 取到期的</text>
<line x1="180" y1="122" x2="196" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="196,122 189,125.2 189,118.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="196" y="108" width="136" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="264" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">阻塞队列，worker 取</text>
<text x="8" y="158" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取出并删除要用 Lua 保证原子，防止重复取</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">List BLMOVE：简单，但没有消费确认</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Pub/Sub：不持久化，订阅者离线就丢</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Stream：消费组 + XACK + PEL，可轻量做队列</text>
</svg>
四个订单按到期时间戳排好，现在是 1010，所以 A、B 已到期，被取出放进阻塞队列等 worker 处理；C、D 还要等。图的底部是三种做消息队列的方式各自的短板。
**业务场景。** 订单 30 分钟未支付自动取消：下单时 `ZADD`，score 是下单时间加 30 分钟；定时任务扫到期订单，用 Lua 原子地取出并删除（否则多个 worker 会取到同一个），放进阻塞队列；worker 检查是否已支付，没付才取消。用户 10 分钟时就付了，订单仍在 ZSet 里，到点 worker 发现已支付直接跳过，也可以支付时 `ZREM`。
**容易错。**
- **以为 Stream 等于 Kafka：** Stream 数据在内存、复制异步，规模和可靠性有上限；强可靠、高吞吐、多消费方、长期保留回放选 Kafka、RocketMQ 的延迟消息。
