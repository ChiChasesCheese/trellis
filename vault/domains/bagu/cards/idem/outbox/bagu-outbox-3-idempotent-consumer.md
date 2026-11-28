---
id: bagu-outbox-3-idempotent-consumer
node: a.idem.outbox
type: qa
step: 3
---
## Q
**本地消息表（Outbox）· 消费端为什么必须幂等，去重表怎么设计**｜必会

面试官：「中继是至少一次，同一条『入账』消息会到消费者两次。你的钱包服务怎么保证只加一次钱？去重表怎么设计？」

## A
**基本回答。** 消息带全局唯一的 msg_id；消费者用去重表（主键是 msg_id）和业务更新放进同一个本地事务：先插入去重行，主键冲突说明处理过，直接返回成功；插入成功才执行入账。两者同事务，所以不会出现「记了去重却没入账」。中继是至少一次，同一条消息一定会到两次以上。业务本身是状态机（`WHERE status='PENDING'` 条件更新）时天然幂等，可以不建去重表。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一条消息 M0001 到了两次</text>
<rect x="8" y="28" width="84" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 1 次</text>
<text x="50" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M0001</text>
<line x1="92" y1="46" x2="101" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,46.0 101.0,49.2 101.0,42.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="108" y="22" width="224" height="52" rx="4" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="114" y="28" width="100" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="164" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">插去重行</text>
<text x="164" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成功</text>
<line x1="214" y1="48" x2="217" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="224.0,48.0 217.0,51.2 217.0,44.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="224" y="28" width="102" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加钱 +100</text>
<text x="275" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交</text>
<text x="112" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两步在同一个本地事务里</text>
<rect x="8" y="116" width="84" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 2 次</text>
<text x="50" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M0001</text>
<line x1="92" y1="134" x2="101" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,134.0 101.0,137.2 101.0,130.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="108" y="112" width="106" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">插去重行</text>
<text x="161" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主键冲突</text>
<line x1="214" y1="134" x2="217" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="224.0,134.0 217.0,137.2 217.0,130.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="224" y="112" width="102" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不加钱</text>
<text x="275" y="145.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接返回成功</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">返回成功 = 让 MQ 确认，否则它会一直重投</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先记去重后入账：崩了 = 丢；先入账后记：崩了 = 重复</text>
</svg>
同一个 msg_id 第一次来，插去重行成功，和加钱在同一个事务里一起提交；第二次来，插入撞上主键，直接返回成功，钱不再动。
**代码。** 去重行和入账同事务：
```sql
START TRANSACTION;
INSERT IGNORE INTO consumed(msg_id) VALUES ('M0001');  -- 影响 0 行 = 重复，提交后直接返回
-- 影响 1 行才继续：
UPDATE wallet SET balance = balance + 100 WHERE uid = 7;
COMMIT;
```
**容易错。**
- **先记去重、后入账分两个事务：** 中间崩了，消息被当成已处理，钱永远没加。
- **去重放 Redis：** 和 MySQL 不是同一个事务，`SETNX` 成功后业务失败，消息被当成已处理而丢失；Redis 只能当前置快速过滤，最终幂等靠数据库主键。
- **重复消息抛异常：** broker 会认为没处理成功，无限重投；应当返回成功。
- **去重行保留太短：** 要比「最长重试时间 + 消息保留期」更久，否则重复消息又被当作新的。

**业务场景。** 打赏入账消息因中继重启发了两次，钱包服务按 msg_id 去重，主播只被加了一次币；没有去重时，每次重发都会多给主播一笔钱，直到对账才发现。
