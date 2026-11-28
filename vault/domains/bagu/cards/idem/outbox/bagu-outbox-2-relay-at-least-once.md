---
id: bagu-outbox-2-relay-at-least-once
node: a.idem.outbox
type: qa
step: 2
---
## Q
**本地消息表（Outbox）· 中继怎么发，为什么只能至少一次**｜必会

面试官：「outbox 表写好了，谁来把它发出去？定时轮询和订阅 binlog 各怎么做？如果消息发成功了，但标记『已发送』时进程挂了，会怎样？」

## A
**基本回答。** 中继（relay）进程负责把 outbox 里的消息发出去。轮询：定时查 `status=0` 的行，按 id 升序发，成功后标记已发送。CDC（变更数据捕获，Change Data Capture）：订阅 binlog（MySQL 的变更日志）里 outbox 表的插入（如 Debezium），延迟更低、不增加业务库查询压力，但多一套组件要运维；量小先轮询，延迟敏感或量大用 CDC。发成功但标记失败，重启后会重发，所以是至少一次（at-least-once）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 226">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先发后标记：失败 = 重复，但不丢（选这个）</text>
<rect x="8" y="24" width="150" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发到 MQ</text>
<text x="83" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成功</text>
<line x1="158" y1="41" x2="175" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="182.0,41.0 175.0,44.2 175.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="182" y="24" width="150" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">标记已发送</text>
<text x="257" y="52.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">进程挂了</text>
<text x="8" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重启后 status 还是 0 → 再发一次 → 至少一次</text>
<text x="8" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先标记后发：失败 = 丢消息（不要这样）</text>
<rect x="8" y="124" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">标记已发送</text>
<text x="83" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">成功</text>
<line x1="158" y1="141" x2="175" y2="141" stroke-width="1.2" stroke="currentColor"/>
<polygon points="182.0,141.0 175.0,144.2 175.0,137.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="182" y="124" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257" y="137.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发到 MQ</text>
<text x="257" y="152.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">进程挂了</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">标记已是 1，没人再发 → 消息永远丢了</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两个动作不可能原子，只能选往哪边失败</text>
</svg>
第一行是选的方向：先发后标记，崩了只会重复。第二行是不能选的：先标记后发，崩了消息就永远丢了。
**代码。** 中继一轮：
```sql
-- 中继每轮：锁住一批待发行，其他实例会跳过它们（MySQL 8.0.1+）
START TRANSACTION;
SELECT id, payload FROM outbox WHERE status = 0
ORDER BY id LIMIT 100 FOR UPDATE SKIP LOCKED;
-- 发送到 MQ 成功后：UPDATE outbox SET status = 1 WHERE id IN (...);
COMMIT;
```
**容易错。**
- **以为可以先标记后发更安全：** 它在崩溃时丢消息，这是更糟的方向。
- **以为 outbox 恰好一次：** 发送和标记不可能原子，端到端只能至少一次。
- **批开得太大：** 发送期间事务一直占着这些行的锁，其他实例和业务更新都会被拖慢。
- **轮询不建联合索引：** 已发送的行积累后，`status=0` 的查询会越来越慢。

**业务场景。** 中继把「支付成功」发到 Kafka 之后、标记已发送之前被重启，同一事件重发了一次，发货服务收到两条相同的消息；消息带着 msg_id，下游据此去重，没有重复发货。
