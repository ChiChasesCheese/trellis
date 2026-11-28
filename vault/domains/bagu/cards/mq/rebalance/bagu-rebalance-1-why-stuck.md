---
id: bagu-rebalance-1-why-stuck
node: b.mq.rebalance
type: qa
step: 1
---
## Q
**消费者组重平衡 · 为什么卡、怎么避免**｜追问

面试官：「判题消费者一发布重启，消费就停几十秒、积压陡增，日志里全是 rebalance。是怎么回事？怎么避免？」

## A
**基本回答。** 重平衡（rebalance）是消费者组重新分配分区。成员加入或离开、心跳超时、两次 `poll` 间隔超过 `max.poll.interval.ms`、分区数变化都会触发。经典的急切（eager）协议下，所有消费者先撤销全部分区，等组协调者重新分配后才恢复，整个组停摆。
默认值：`session.timeout.ms` 3.0 起 45 秒（之前 10 秒），`heartbeat.interval.ms` 3 秒，`max.poll.interval.ms` 5 分钟。Kafka 4.0 的新协议 KIP-848 由服务端增量分配，没有全组暂停，要显式设 `group.protocol=consumer`，默认仍是 classic。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="110" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C2 重启</text>
<line x1="110" y1="18" x2="110" y2="112" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="10" y="48" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">急切</text>
<rect x="56" y="28" width="54" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费</text>
<rect x="110" y="28" width="120" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="170" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全组停摆</text>
<rect x="230" y="28" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重新分配后消费</text>
<text x="10" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">协作式</text>
<rect x="56" y="78" width="274" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C1 不停，只迁移要动的分区</text>
<text x="10" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">触发：成员加入或离开、心跳超时、</text>
<text x="10" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两次 poll 超过 max.poll.interval.ms、</text>
<text x="10" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">订阅的分区数变化</text>
<text x="10" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">默认：session 45 秒，心跳 3 秒</text>
<text x="10" y="220" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">poll 间隔 5 分钟</text>
</svg>
第一条是急切协议：C2 重启的那一刻起，整组都停下撤销分区，等重新分配后才继续；第二条是协作式：C1 不停，只迁移要动的分区。
**举个例子。** 判题消费者 3 个实例，滚动发布：
1. **实例 1 重启：** 它离开消费组，触发一次重平衡；急切协议下，实例 2、3 也撤销全部分区，整组停摆。
2. **等重新分配：** 协调者重新分配后，大家恢复消费，这段时间积压陡增，日志里全是 rebalance。
3. **实例 1 回来：** 它重新加入，又触发一次重平衡，再停一次。
4. **处理慢的情况：** 一批判题任务要几十秒，超过 `max.poll.interval.ms`，实例被踢出组，分区被接走，它再提交 offset 失败，任务被重复判。
5. **改进：** 调大 `max.poll.interval.ms`、减小 `max.poll.records`；改成 `CooperativeStickyAssignor`；设 `group.instance.id`，让实例在 `session.timeout.ms` 内回来就保留原分区，滚动发布时不触发重平衡。
**容易错。**
- **以为配了协作式就一定生效：** 3.0 起默认策略列表里 Range 排在前面，要显式配置 `CooperativeStickyAssignor`。
- **以为 KIP-848 默认就是新协议：** 要显式设 `group.protocol=consumer`，默认仍是 classic。
- **只调大 session.timeout.ms：** 处理太慢引起的超时是 `max.poll.interval.ms`，要缩短每批耗时。
- **重平衡后不做幂等：** 已处理未提交的会被重读，消费端必须幂等。
