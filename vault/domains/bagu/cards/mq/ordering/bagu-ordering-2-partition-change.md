---
id: bagu-ordering-2-partition-change
node: a.mq.ordering
type: qa
step: 4
---
## Q
**消息顺序 · 分区数变化破坏顺序**｜追问

面试官：「同一个 key 到同一分区之后，如果把分区数从 4 扩到 6，顺序会怎样？」

## A
**基本回答。** 会乱。增加分区会改变 `hash(key) % 分区数` 的映射，同一个 key 的新旧消息落到不同分区，破坏顺序；分区只能增不能减。
**一句话记住。** 分区数像餐厅的窗口数：按「身份证号除以窗口数的余数」分配窗口。窗口从 4 个加到 6 个，同一个客户的余数变了，他的新业务去了新窗口，而旧窗口还排着他的旧业务，新旧两边谁先办完就不一定了。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个订单，hash(key) = 10</text>
<rect x="8" y="26" width="324" height="44" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 个分区：10 % 4 = 2</text>
<text x="170.0" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ P2（旧「创建」还在排队）</text>
<line x1="170" y1="70" x2="170" y2="96" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,96.0 166.8,89.0 173.2,89.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="182" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扩到 6 个分区</text>
<rect x="8" y="96" width="324" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6 个分区：10 % 6 = 4</text>
<text x="170.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ P4（新「支付」）</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两个分区的消费进度不同</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新「支付」可能先于旧「创建」被处理</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">做法：先排空再切换，或新建 topic 迁移</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区只能增不能减，第一次就留余量</text>
</svg>
同一个 key（哈希值 10），分区数 4 时落在 P2，分区数 6 时落在 P4。P2 里的旧消息还没消费完，新消息已经去了 P4。
**讲明白。**
- **为什么映射会变：** 消息去哪个分区由 `hash(key) % 分区数` 决定。分母从 4 变成 6，同一个 key 的余数一般会变。
- **为什么会乱序：** 旧分区里可能还有该 key 的未消费消息，新消息却去了新分区，两个分区由不同消费者读，消费进度不同，新消息可能先被处理。
- **分区只能增不能减：** Kafka 的分区只能增不能减。想减少只能新建 topic 并迁移数据。
- **所以第一次就要留余量：** 创建时按预期吞吐多留一些，避免后面扩分区。
- **必须扩时怎么做：** 选低峰，变分区前先让该 topic 的消息排空再切换；或新建分区更多的 topic，双写迁移。
- **兜底：** 对强顺序业务，消费端也可以带版本号，拒绝旧版本覆盖。
**举个例子。** 订单 7 的 key 哈希值是 10，topic 从 4 个分区扩到 6 个。
1. **扩容前：**10 % 4 = 2，订单 7 的「创建」消息进了 P2，还没被消费，排在队列里。
2. **扩容：**分区变成 6 个。
3. **扩容后：**10 % 6 = 4，订单 7 的「支付」消息进了 P4。
4. **消费：**P4 没有积压，消费者马上处理了「支付」；P2 的消费者还在处理积压，「创建」还没轮到。
5. **结果：**先处理支付、后处理创建，状态错乱。
**容易错。**
- **以为扩分区只影响新数据：** 它改变了映射，新旧消息对同一个 key 会落到不同分区。
- **以为分区可以缩回去：** 只能增不能减。
- **在高峰期扩容：** 积压多时更容易乱，要选低峰并先排空。
- **只依赖分区保序：** 强顺序业务还要在消费端加版本号兜底。
**业务场景。** 订单 topic 在大促前从 4 扩到 6 分区，同一订单的「支付」被另一分区的消费者先处理，出现先发货后支付的状态。
**系统设计。** 「[[links.messenger-chat-system|聊天/即时通讯系统（WhatsApp / Messenger）]]」扩容会话分区时，问「分区数变了，会话内顺序怎么保」，答先排空或新 topic，并让消费端带版本号拒绝旧消息。
**可能问法。**
- 分区数变了顺序怎么办？ → 增加分区会改变 hash(key) % 分区数 的映射，同一个 key 的新旧消息落到不同分区，两个分区消费进度不同，顺序就乱。变分区前先让该 topic 的消息排空再切换，或新建分区更多的 topic 迁移。
- 分区能减少吗？ → 不能，Kafka 的分区只能增不能减。想减少只能新建 topic 并迁移数据。所以第一次创建时就要按预期吞吐留出余量。
- 怎么避免扩容破坏顺序？ → 创建时预留余量，避免后面扩分区；必须扩时选低峰，先让旧消息消费完再让新消息进入新映射；或新建 topic、双写迁移。对强顺序业务，消费端也可以带版本号，拒绝旧版本覆盖。
