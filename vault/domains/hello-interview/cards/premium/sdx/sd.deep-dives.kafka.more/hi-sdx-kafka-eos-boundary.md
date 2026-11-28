---
id: hi-sdx-kafka-eos-boundary
node: sd.deep-dives.kafka.more
type: qa
step: 2
---
## Q
**事务边界：Kafka 事务还是发件箱**｜补充 · Kafka · 追问

面试官：「要做到恰好一次，什么时候用 Kafka 事务，什么时候用事务发件箱？还有哪个地方，大家常误以为 Kafka 的保证能延伸过去？」

## A
**结论。** 原子边界只能落在同一个系统里。读—转换—写都在 Kafka 内（连消费位移也是写 Kafka）就用 Kafka 事务；要改数据库并发事件，就让数据库事务把状态和事件行一起提交（发件箱），之后再发 Kafka。常被误解的是跨集群：复制会重新生产记录，事务和位点都不跟着过去。

**要点。**
- **系统记录在 broker：** 输入位移和输出记录在 Kafka 内同一个事务里提交，下游用 `read_committed` 读取。
- **系统记录在数据库：** Kafka 无法加入数据库的提交，这一半 Kafka 事务帮不上忙，原子单元只能是数据库事务。
- **跨集群：** MirrorMaker 2 基于 Connect 的源连接器，默认至少一次，目标集群的位点和源集群不同；消费组位点靠检查点翻译，只是近似，切换后会有重复。
- **链上每多一个系统：** 另一种 broker、数据库、外部接口，都是新的边界，各自要去重或幂等。
- **2026 亮点：** Kafka 4.0 加固了事务协议（KIP-890）：（新版客户端）每次提交或中止都提升 producer epoch，晚到的旧消息会被拒绝，不再制造悬挂事务卡住 read_committed 消费者；应用遇到 TimeoutException 和 TransactionAbortableException 都应中止事务。但这仍只保证 Kafka 内部的恰好一次，数据库和支付渠道的副作用靠幂等键和发件箱。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 系统记录在 Kafka：读—转换—写</text>
<rect x="8" y="24" width="324" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">输入位移 + 输出记录 = 一个 Kafka 事务</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 系统记录在数据库：状态和事件同事务</text>
<rect x="8" y="92" width="132" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="74.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库事务</text>
<text x="74.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">改状态 + 写事件行</text>
<polyline points="140,114 153.0,114.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="160,114 153.0,117.2 153.0,110.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="160" y="92" width="70" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="195.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中继</text>
<polyline points="230,114 243.0,114.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,114 243.0,117.2 243.0,110.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="250" y="92" width="82" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="291.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 跨集群：事务和位点都不跟过去</text>
<rect x="8" y="172" width="92" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54.0" y="195.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群 A</text>
<polyline points="100,191 113.0,191.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120,191 113.0,194.2 113.0,187.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="120" y="172" width="100" height="38" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="170.0" y="195.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MM2 复制</text>
<polyline points="220,191 233.0,191.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240,191 233.0,194.2 233.0,187.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="240" y="172" width="92" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286.0" y="195.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">集群 B</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">复制会重新生产记录，默认至少一次；</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每多一个系统边界，就多一层去重。</text>
</svg>

**面试里这样说。** 「我先问原子边界在哪。管道全在 Kafka 里就用事务；一边是数据库我就用发件箱；跨集群的消费者我按至少一次设计，切换后仍然幂等。」

**易错。**
- **在数据库写之后再开 Kafka 事务：** 两个系统仍然没有共同的提交，崩在中间照样丢或重。
- **以为异地复制保留事务语义：** 目标集群是新的记录和新的偏移量，需要自己去重。
