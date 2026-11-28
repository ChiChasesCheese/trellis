---
id: bagu-kafka-architecture-2-replica
node: a.mq.kafka-architecture
type: qa
step: 2
---
## Q
**Kafka 结构 · 副本与 Leader、Follower**｜必会

面试官：「分区的数据只在一台 Broker 上会丢，Kafka 的副本机制怎么做？Follower 怎么同步？」

## A
**基本回答。** 每个分区有多个副本（replica），其中一个是 leader，负责读写，其余是 follower，主动从 leader 拉数据。leader 挂了，从 ISR 里选新 leader。
复制是 follower 主动 fetch，不是 leader 推；跟上的副本组成 ISR。2.4 起配置 `replica.selector.class` 可让同机架 follower 服务读，省跨机架流量，代价是读到稍旧的数据。选主由 controller 从 ISR 里选，`unclean.leader.election.enable` 要设 false，避免落后副本当选而丢数据。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="8" y="4" width="90" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="53.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者</text>
<line x1="53" y1="30" x2="53" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="53.0,46.0 49.8,39.0 56.2,39.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="62" y="41" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只读 leader</text>
<rect x="8" y="46" width="90" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="53.0" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker 1</text>
<text x="53.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0 leader</text>
<rect x="125" y="46" width="90" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker 2</text>
<text x="170.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0 follower</text>
<rect x="242" y="46" width="90" height="42" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="287.0" y="63.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker 3</text>
<text x="287.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0 follower</text>
<line x1="125" y1="67" x2="98" y2="67" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="98.0,67.0 105.0,63.8 105.0,70.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="287" y1="88" x2="287" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="287" y1="106" x2="40" y2="106" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="40" y1="106" x2="40" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="40.0,88.0 43.2,95.0 36.8,95.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">follower 主动拉取（fetch），不是推送</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Broker 2 同时是 P1 的 leader：读写负载分散</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">leader 挂了 → 从 ISR 里选新 leader</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">replication.factor 默认 1，生产要配 3</text>
</svg>
Broker 1 上是 P0 的 leader，Broker 2、3 上是 follower，它们向 leader 拉数据（高亮箭头）；消费者默认只读 leader。
**举个例子。** 审核事件所在分区 P0，三个副本，replication.factor=3。
1. **正常：**Broker 1 是 P0 的 leader，Broker 2、3 的副本隔一会儿就来拉；生产者的写入和消费者的读取都找 Broker 1。
2. **Broker 1 宕机：**控制器从 ISR（Broker 2、3）里选一个，比如 Broker 2，成为新 leader。
3. **客户端：**元数据更新后改为连 Broker 2，审核服务只经历一次重连，不丢消息。
4. **如果副本数是 1：**宕机就是丢数据加中断，所以默认的 1 在生产上不能用。
**容易错。**
- **以为 leader 推数据给 follower：** 是 follower 主动拉。
- **以为 follower 能随便读：** 默认只读 leader，读 follower 要显式配置，且可能读到稍旧的数据。
- **以为副本数默认是 3：** 默认只有 1，要自己配。
- **以为一台 Broker 只放 leader：** 一台 Broker 上既有 leader 也有 follower，负载才分散。
