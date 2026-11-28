---
id: hi-sdx-kafka-vs-pulsar
node: sd.deep-dives.kafka.more
type: qa
step: 6
---
## Q
**Kafka 与 Pulsar 的架构差异**｜补充 · Kafka · 加分

面试官：「为什么有团队选 Pulsar 而不是 Kafka？存算分离换来了什么，又付出了什么？」

## A
**结论。** Pulsar 把无状态的 broker 和存储层（BookKeeper 存储节点）分开，分区日志被切成段，分散存放在多个存储节点上。换来：扩容不用搬数据、冷热分层、同一集群既有日志语义又有共享订阅的队列语义，还有多租户和跨地域复制。代价是组件更多、运维更重、生态比 Kafka 小。

**要点。**
- **Kafka：** 分区数据在 leader broker 的本地盘，扩容要迁移分区；组内一个分区只被一个消费者读，并行度被分区数封顶。
- **Pulsar：** broker 无状态，加 broker 不搬数据；新的日志段写到新的存储节点上；订阅有独占、故障转移、共享、按键共享四种，共享订阅下消费者数不受分区数限制。
- **选择规则：** 分发任务选队列语义；其他系统要反复重读的事实选日志语义；要两种语义、多租户、跨地域都在一个集群，才考虑 Pulsar。
- **成本：** 要运维 broker、BookKeeper 和元数据存储三层，生态和人才都比 Kafka 少。
- **2026 亮点：** Pulsar 5.0 成为新的 LTS，带 Scalable Topics：按键范围分段，broker 按负载自动拆分和合并并保持按键有序，不再有固定分区数的难题；新集群推荐用 Oxia 做元数据存储。限制：目前只有 Java v5 客户端，Scalable Topics 暂不支持跨地域复制，选型要看这些。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Kafka：数据在 broker 本地盘</text>
<rect x="8" y="24" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">broker 1</text>
<text x="83.0" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区 0 的数据</text>
<rect x="8" y="72" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="83.0" y="88.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">broker 2</text>
<text x="83.0" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区 1 的数据</text>
<text x="8" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扩容要搬分区数据</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">并行度受分区数限制</text>
<text x="182" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Pulsar：存算分离</text>
<rect x="182" y="24" width="150" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无状态 broker</text>
<polyline points="257,58 257.0,69.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257,76 253.8,69.0 260.2,69.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="182" y="76" width="150" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">BookKeeper 存储节点</text>
<text x="182" y="138" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加 broker 不搬数据</text>
<text x="182" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">共享订阅不限分区数</text>
<line x1="8" y1="176" x2="332" y2="176" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">代价：组件更多（broker、BookKeeper、</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">元数据存储），运维更重，生态比 Kafka 小</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">日志段（ledger）分散在多个存储节点上</text>
</svg>

**面试里这样说。** 「大多数场景我选 Kafka，生态和人才都成熟。如果同一集群既要队列又要日志、还要多租户，才会考虑 Pulsar，因为它的存算分离让扩容不用搬数据，但运维多一层。」

**易错。**
- **把存算分离说成没有代价：** 多一层存储集群，延迟和运维都更复杂。
- **只说吞吐：** 选型的区别在语义和运维形态，不在谁的吞吐数字更高。
