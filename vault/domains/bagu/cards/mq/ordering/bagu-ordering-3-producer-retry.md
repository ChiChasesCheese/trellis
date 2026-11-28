---
id: bagu-ordering-3-producer-retry
node: a.mq.ordering
type: qa
step: 2
---
## Q
**消息顺序 · 生产端重试与幂等生产者**｜必会

面试官：「生产端发送失败重试，会不会让后发的消息先到？幂等生产者和 max.in.flight 对顺序有什么影响？」

## A
**基本回答。** 会。批次 1 失败重试，批次 2 已经成功，顺序就反了。开启幂等生产者 `enable.idempotence=true`（Kafka 3.0 起默认开）后，`max.in.flight.requests.per.connection ≤ 5` 也能保序。
Kafka 3.0 起 `enable.idempotence` 默认 true，`retries` 默认 `Integer.MAX_VALUE`，总时长受 `delivery.timeout.ms`（默认 120 秒）限制；3.0 之前要自己显式打开幂等。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不开幂等：批次 1 失败重试，批次 2 先成功</text>
<rect x="8" y="22" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批次 1 发送超时失败</text>
<rect x="176" y="22" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批次 2 成功写入</text>
<line x1="86" y1="52" x2="86" y2="68" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,68.0 82.8,61.0 89.2,61.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="68" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批次 1 重试写入</text>
<line x1="86" y1="98" x2="86" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,112.0 82.8,105.0 89.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="112" width="324" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分区日志：批次 2，批次 1 → 乱序</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">开幂等：每个批次带序列号</text>
<rect x="8" y="172" width="324" height="46" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批次 2（序号 1）先到，Broker 期望序号 0</text>
<text x="170.0" y="206.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 拒绝，按序重发：批次 1，批次 2</text>
<text x="8" y="240" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">max.in.flight ≤ 5 仍保序；不开幂等要设 1</text>
</svg>
上半部分是不开幂等：批次 1 重试晚于批次 2，日志里顺序反了；下半部分是开幂等：Broker 靠序号拒绝乱序批次。
**举个例子。** 同一个玩家的两条分数更新，批次 1 是 80 分、批次 2 是 95 分，同 key 同分区。
1. **不开幂等：**批次 1 超时失败，批次 2 成功写入，批次 1 重试后追加在后面。
2. **日志里顺序：**批次 2（95），批次 1（80）。后到的 80 覆盖了 95，分数倒退。
3. **开幂等：**批次 1 序号 0，批次 2 序号 1。批次 1 失败，批次 2 先到。
4. **Broker 判断：**期望序号 0，收到的是 1，拒绝批次 2。
5. **客户端重发：**按序重发批次 1，再发批次 2，日志是批次 1（80）、批次 2（95），顺序正确。
**容易错。**
- **以为同 key 同分区就没有乱序：** 生产端重试也会让它乱。
- **以为幂等只防重复：** 它也让重试按序，是保序的一部分。
- **开了幂等还把 max.in.flight 设很大：** 超过 5 保序不再有保证。
- **以为 3.0 前也默认开：** 3.0 之前要自己显式打开。
