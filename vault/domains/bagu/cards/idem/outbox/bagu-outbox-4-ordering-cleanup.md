---
id: bagu-outbox-4-ordering-cleanup
node: a.idem.outbox
type: qa
step: 4
---
## Q
**本地消息表（Outbox）· 怎么避免乱序，表怎么清理**｜追问

面试官：「同一个订单先后产生『已支付』『已退款』两条事件，下游必须按顺序处理。outbox 怎么避免乱序？还有，这张表越写越大怎么办？」

## A
**基本回答。** 同一业务实体的消息按 outbox 自增 id 顺序发送，并用实体 ID（订单号）做 MQ 的分区键（partition key），同一订单落在同一分区，分区内有序。已发送的行定期归档或删除，防止表膨胀。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用订单号当分区键：同一订单落在同一分区</text>
<rect x="8" y="24" width="324" height="56" rx="4" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="14" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分区 1（订单 A）</text>
<rect x="18" y="46" width="90" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 已支付</text>
<line x1="108" y1="60" x2="143" y2="60" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="150.0,60.0 143.0,63.2 143.0,56.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="150" y="46" width="90" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="195" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 已退款</text>
<text x="250" y="64" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按序消费</text>
<rect x="8" y="88" width="324" height="56" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="14" y="102" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区 2（订单 B）</text>
<rect x="18" y="110" width="90" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 已支付</text>
<text x="120" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与 A 互不影响</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">outbox 里按自增 id 发；同一订单的更新会互斥，</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">所以同一订单内，id 顺序 = 提交顺序</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">清理：已发送行保留几天 → 分批 DELETE ... LIMIT 1000</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">或按日期分区，整块丢弃</text>
</svg>
订单 A 的「已支付」「已退款」永远进同一个分区，分区内顺序就是发送顺序；订单 B 在另一个分区，与 A 互不影响。下面两行是表的清理办法。
**容易错。**
- **追求全局有序：** 吞吐被拖垮，业务也不需要。
- **以为自增 id 全局等于提交顺序：** 不同订单之间不保证；只有同一订单内成立（因为互斥）。
- **同一分区放多个并发中继：** 批次完成时间不定，新消息可能先到；同一分区只让一个中继发，或按 biz_key 哈希把行固定分给某个中继。
- **一次删几百万行：** 大事务拖慢主库、造成主从延迟；已发送的行留几天便于排查，再分批 `DELETE ... LIMIT 1000` 或按日期分区整个丢弃；未发送的积压要监控告警。
- **消费端默认不会乱序：** 万一乱序，消息带版本号，收到比当前状态旧的版本直接丢弃，退款（版本 2）先到、支付（版本 1）迟到也不会覆盖回去。
**业务场景。** 订单刚付完款就退款，两条事件若落在不同分区，退款事件先到发货服务，就会出现先退款、后发货；用订单号做分区键后，同单消息按序到达。
