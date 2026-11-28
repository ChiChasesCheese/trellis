---
id: bagu-no-duplicate-1-idempotent-consumer
node: b.mq.no-duplicate
type: qa
step: 1
---
## Q
**重复消费 · 怎么处理、Kafka 恰好一次的边界**｜必会

面试官：「积分服务收到两条一模一样的『支付成功』消息，业务不允许加两次分，怎么设计？Kafka 不是有恰好一次吗？」

## A
**基本回答。** MQ 默认至少一次，重复无法避免，所以消费端要幂等：消息带全局唯一 ID，在同一个本地事务里写去重表（唯一键 messageId）和业务数据，重复消息撞唯一键直接忽略；或用状态机条件更新 `UPDATE ... WHERE status = 'PENDING'`。
去重行和业务表要在同一个数据库的同一个本地事务里：先 INSERT 去重行，主键冲突就回滚并返回成功，成功再 UPDATE 业务表，最后 COMMIT。Kafka EOS = 幂等生产者（producer ID + 序列号，3.0 起 `enable.idempotence` 默认开）+ 事务（`transactional.id`，原子写多个分区并提交消费 offset），下游设 `isolation.level=read_committed`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 1 次：同一个本地事务</text>
<text x="180" y="14" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 2 次：重复消息</text>
<rect x="10" y="24" width="150" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INSERT 去重行 m1</text>
<text x="85" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成功</text>
<rect x="10" y="74" width="150" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UPDATE 积分 +10</text>
<rect x="10" y="124" width="150" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">COMMIT</text>
<line x1="85" y1="56" x2="85" y2="74" stroke="currentColor" stroke-width="1.2"/>
<polygon points="85,74 82.0,67.7 88.0,67.7" fill="currentColor"/>
<line x1="85" y1="106" x2="85" y2="124" stroke="currentColor" stroke-width="1.2"/>
<polygon points="85,124 82.0,117.7 88.0,117.7" fill="currentColor"/>
<rect x="180" y="24" width="150" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INSERT 去重行 m1</text>
<text x="255" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">唯一键冲突</text>
<rect x="180" y="74" width="150" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回滚，直接确认</text>
<line x1="255" y1="56" x2="255" y2="74" stroke="currentColor" stroke-width="1.2"/>
<polygon points="255,74 252.0,67.7 258.0,67.7" fill="currentColor"/>
<text x="10" y="184" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重复的来源：处理完但没提交 offset 就崩溃</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Kafka EOS 只覆盖 读 Kafka→写 Kafka</text>
<text x="10" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写数据库、调 HTTP 仍要自己幂等</text>
</svg>
左列是第一次到达：去重行和业务写入在同一个事务里一起提交；右列是同一条消息又来一次：插入去重行时撞上唯一键，回滚后直接确认，不再加分。
**举个例子。** 积分服务收到支付成功消息 m1（订单 O1，加 10 分）：
1. **第一次到达：** 开事务，`INSERT dedup(msg_id='m1')` 成功，`UPDATE points SET balance = balance + 10`，COMMIT。积分加了 10。
2. **重复到达：** 同一条 m1 再来，开事务，`INSERT dedup(msg_id='m1')` 撞唯一键失败，回滚，返回成功给 MQ。
3. **结果：** 积分仍然只加了一次 10，MQ 也不再重发。
4. **状态机版本：** 订单表状态 `PENDING`，`UPDATE orders SET status='PAID' WHERE id=O1 AND status='PENDING'`；第一次影响 1 行，重复来时影响 0 行，不再加分。
5. **崩溃场景：** 如果在 COMMIT 前崩溃，去重行和积分都回滚，重发时从头处理，不会出现「记了去重却没加分」。
**容易错。**
- **以为 Kafka 开了 EOS 就不用幂等：** 它只管 Kafka 内部的链路，写数据库、调 HTTP 仍要幂等。
- **去重行和业务写入分两个事务：** 中间崩溃就会「记了去重没加分」或「加了分没记去重」。
- **用内存集合去重：** 重启就丢，多实例之间也不共享，要落库。
- **去重表与业务表不同库：** 做不到同一个本地事务，只能靠业务唯一键。
