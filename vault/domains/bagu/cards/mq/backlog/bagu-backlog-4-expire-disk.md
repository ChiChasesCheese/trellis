---
id: bagu-backlog-4-expire-disk
node: a.mq.backlog
type: qa
step: 4
---
## Q
**消息积压 · 过期和磁盘写满**｜追问

面试官：「积压了几个小时，消息会过期吗？磁盘快写满了怎么办？」

## A
**基本回答。** 会。Kafka 超过保留时间（`retention.ms`）未消费的数据会被删除，积压时间超过保留期就丢；RabbitMQ 设了 TTL（消息存活时间）的消息过期也会被清理。要有 lag 告警，必要时临时延长保留时间。
**一句话记住。** 消息队列是一条只保留最近几天的监控录像：你回看得太慢，最早的那段会被新录像覆盖，想看也看不到了。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<rect x="8" y="22" width="92" height="50" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已消费</text>
<text x="54" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（可以删）</text>
<rect x="100" y="22" width="116" height="50" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="158" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">未消费，但已</text>
<text x="158" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">过期被删：丢</text>
<rect x="216" y="22" width="116" height="50" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="274" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">未消费，还在</text>
<text x="274" y="59" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">保留期内</text>
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个分区的日志，左旧右新</text>
<line x1="100" y1="102" x2="100" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100.0,74.0 103.2,81.0 96.8,81.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="100" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已提交位点</text>
<line x1="216" y1="102" x2="216" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="216.0,74.0 219.2,81.0 212.8,81.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保留期边界</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">积压时间 &gt; retention.ms，中间这段就丢</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">磁盘要写满 → 消费一个丢一个，晚上再补</text>
</svg>
一个分区的日志从左到右由旧到新。消费者的位点停在中间，右边的消息还在保留期内；位点左边已经过了保留期的部分被删掉了。位点和保留期边界之间的那一段，是没消费却已经被删的消息，就是丢的数据。
**讲明白。**
- **Kafka 按时间删数据：** `retention.ms` 是保留时间，超过这个时间的数据会被删除，不管有没有被消费。积压超过保留期，没消费的消息就永远丢了。
- **RabbitMQ 靠 TTL：** 给消息设了 TTL 的话，到期没被消费也会被清理。
- **先靠告警提前发现：** 要有 lag 告警，在积压快追上保留期之前就处理，而不是丢了才发现。
- **临时延长保留时间：** 可以临时把保留时间调大，为消费争取时间。调之前先看磁盘余量，因为保留时间越长，占的磁盘越多。
- **按大小限制：** `retention.bytes` 可以限制单个分区的大小，防止日志无限变大。
- **已经丢掉的怎么补：** 积压高峰过后，写一个临时程序，把丢失的数据从业务库或日志里按时间范围查出来，重新灌回 MQ（批量重导），再用对账确认没有缺口。
- **补发会造成重复：** 重新发回去的消息，有些可能已经被处理过，所以消费端要做幂等。
- **磁盘要写满了：** 对低价值消息消费一个丢一个，先快速消完、腾出磁盘，晚上再把这些数据补回来。
**举个例子。** 保留期 retention.ms 设成 6 小时，一批积分事件积压了 7 小时：
1. **到第 6 小时：** 最早写入的消息已经满 6 小时，开始被删除。
2. **到第 7 小时：** 最早那 1 小时的消息已经被删，消费者再读，位点之前的这一段没有了，积分少发。
3. **高峰过后：** 从订单库按时间范围查出那一小时的订单，重新发送给积分服务。
4. **补发之后：** 消费端用订单号做幂等，已经处理过的重复消息直接忽略，对账确认没有缺口。
**容易错。**
- **以为未消费的消息会一直留着：** Kafka 按保留时间删，不管有没有消费。
- **无脑延长保留：** 保留时间越长越占磁盘，磁盘写满会让整个 broker 出问题，要先看余量。
- **补数据忘了幂等：** 重导会带来重复消息，消费端不幂等就会重复处理。
**业务场景。** 积压超过保留期，一批积分事件被删除；高峰后从订单库按时间范围查出缺失订单，重新发送给积分服务。
**系统设计。** [[links.ad-click-aggregator|广告点击聚合]]：事件丢了就少算点击，面试官问「积压期间事件被删怎么补」，答从源库或日志重导，并用对账发现缺口。
**可能问法。**
- 积压超过保留期怎么办？ → Kafka 超过 `retention.ms` 未消费的数据会被删除，积压超过保留期就丢。要有 lag 告警，必要时临时延长保留时间（先看磁盘余量，`retention.bytes` 可限制单分区大小）；已经丢掉的，高峰后从业务库查出来批量重灌回 MQ。
- 消息过期丢了怎么补？ → 高峰过后写临时程序，从业务库或日志按时间范围查出缺失的数据，重新发回 MQ，并用对账确认没有缺口；补发会造成重复，所以消费端要幂等。
- 磁盘满了怎么办？ → 对低价值消息消费一个丢一个，先快速消完腾出磁盘，晚上再补数据；延长保留前先看磁盘余量，保留时间越长占的磁盘越多。
