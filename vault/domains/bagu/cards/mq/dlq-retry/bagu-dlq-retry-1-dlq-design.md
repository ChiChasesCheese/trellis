---
id: bagu-dlq-retry-1-dlq-design
node: b.mq.dlq-retry
type: qa
step: 1
---
## Q
**死信队列与重试 · 毒消息怎么处置**｜追问

面试官：「有一条消息消费一直失败，会卡住整个分区。重试和死信队列你怎么设计？」

## A
**基本回答。** 毒消息（poison message，格式错误或触发 bug）不能无限重试。做法：本地先快速重试 2–3 次；仍失败发到分级重试 topic（`retry-1m`、`retry-10m`、`retry-1h`），到点再消费；超过最大次数发到死信 topic，主流程继续消费后面的消息。
RabbitMQ 的死信交换机（DLX）：消息被拒绝且不重新入队、TTL 过期、队列溢出，或 quorum 队列超过 delivery-limit，自动路由到 DLX 对应的队列。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="10" y="10" width="70" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主 topic</text>
<rect x="110" y="10" width="70" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者</text>
<rect x="210" y="10" width="120" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地快速重试</text>
<text x="270" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 到 3 次</text>
<line x1="80" y1="28" x2="110" y2="28" stroke="currentColor" stroke-width="1.2"/>
<polygon points="110,28 103.7,31.0 103.7,25.0" fill="currentColor"/>
<line x1="180" y1="28" x2="210" y2="28" stroke="currentColor" stroke-width="1.2"/>
<polygon points="210,28 203.7,31.0 203.7,25.0" fill="currentColor"/>
<text x="292" y="66" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">仍失败</text>
<line x1="298" y1="46" x2="298" y2="82" stroke="currentColor" stroke-width="1.2"/>
<polygon points="298,82 295.0,75.7 301.0,75.7" fill="currentColor"/>
<rect x="266" y="82" width="64" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">retry-1m</text>
<rect x="170" y="82" width="70" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">retry-10m</text>
<rect x="74" y="82" width="64" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">retry-1h</text>
<line x1="266" y1="100" x2="240" y2="100" stroke="currentColor" stroke-width="1.2"/>
<polygon points="240,100 246.3,97.0 246.3,103.0" fill="currentColor"/>
<line x1="170" y1="100" x2="138" y2="100" stroke="currentColor" stroke-width="1.2"/>
<polygon points="138,100 144.3,97.0 144.3,103.0" fill="currentColor"/>
<text x="114" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过最大次数</text>
<line x1="106" y1="118" x2="106" y2="158" stroke="currentColor" stroke-width="1.2"/>
<polygon points="106,158 103.0,151.7 109.0,151.7" fill="currentColor"/>
<rect x="10" y="158" width="190" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="105" y="174.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">死信 topic</text>
<text x="105" y="189.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带原位置、异常栈、重试次数</text>
<text x="10" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主流程继续消费后面的消息</text>
<text x="10" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">死信要告警、能回放、有保留期</text>
</svg>
消息沿着箭头一级级降级：本地快速重试、三级重试 topic、最后进死信；每一级的目的都是不拖住主流程。
**举个例子。** 风控服务偶尔超时，订单事件 E1 处理失败：
1. **本地重试：** 在原地立刻重试 3 次，仍超时。
2. **进 retry-1m：** 发到 `retry-1m`，主 topic 继续处理 E2、E3……
3. **一分钟后：** 从 `retry-1m` 消费 E1，再试，还失败，发到 `retry-10m`。
4. **再失败：** 十分钟后试，仍失败，发到 `retry-1h`；一小时后第三次仍失败，超过最大次数。
5. **进死信：** E1 带着原 topic / 分区 / offset 和异常栈发到死信 topic，并触发告警。工程师修好 bug 后用回放工具把它送回原 topic。
**容易错。**
- **原地无限重试：** 毒消息会堵住整个分区。
- **死信里不带上下文：** 没有原 topic / 分区 / offset 和异常栈，排查和回放都做不了。
- **死信当垃圾桶：** 没有告警、没有回放、没有保留期，等于消息丢了。
- **以为 Kafka 自带 DLQ：** Kafka 没有原生死信，要应用自己实现；RabbitMQ 才有 DLX。
- **要保序却直接发重试 topic：** 同 key 的后续消息会先于失败的那条被处理，顺序乱了。
