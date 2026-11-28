---
id: bagu-no-loss-2-producer
node: a.mq.no-loss
type: qa
step: 2
---
## Q
**消息不丢 · 生产端配置**｜必会

面试官：「生产端 acks、重试、幂等生产者怎么配？发送失败本地怎么办？」

## A
**基本回答。** `acks=all`；`retries` 足够大；`enable.idempotence=true`；使用带回调的发送并处理失败。
`acks=all` 等当前 ISR 内的副本都写入才返回，并配 `min.insync.replicas=2`。Kafka 3.0 起默认已是 `acks=all`、`retries=Integer.MAX_VALUE`（总时长受 `delivery.timeout.ms` 默认 120 秒限制），旧版本要显式配置。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<rect x="8" y="6" width="200" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务事务：写库 + 写 outbox</text>
<line x1="108" y1="36" x2="108" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,56.0 104.8,49.0 111.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="56" width="200" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">异步发送：带回调的 send</text>
<line x1="208" y1="71" x2="232" y2="71" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,71.0 225.0,74.2 225.0,67.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="56" width="100" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="75.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Kafka</text>
<line x1="60" y1="86" x2="60" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,112.0 56.8,105.0 63.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="156" y1="86" x2="156" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="156.0,112.0 152.8,105.0 159.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="112" width="104" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="60.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回调成功</text>
<rect x="120" y="112" width="124" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="182.0" y="131.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">失败：留在 outbox</text>
<text x="8" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重发任务定时补发，不静默丢</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">幂等生产者：producer ID + 序列号，重试不重复</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3.0 起默认 acks=all，retries 为 Integer.MAX_VALUE</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">总时长受 delivery.timeout.ms（120 秒）限制</text>
</svg>
业务写库的同时把待发事件写进 outbox 表；异步发送带回调，成功就标记已发，失败就留在 outbox 里等重发任务补发。
**举个例子。** 钱包充值成功后要发一条事件。
1. **业务事务：**更新余额，同时往 outbox 表插入「充值成功」事件，一起提交。
2. **异步发送：**发送任务带回调调用 send。
3. **Broker 短暂不可用：**回调收到失败，事件仍留在 outbox，没有标记已发。
4. **重发任务：**定时扫描 outbox，把没发出去的事件补发。
5. **发送成功：**回调收到成功，才标记已发。没有静默丢失。
**容易错。**
- **只看 send 有没有抛异常：** 异步发送的失败在回调里，不看回调等于不知道失败。
- **在业务事务里同步等发送结果再决定回滚：** 把消息队列的可用性绑进了业务事务，不要这样做；用 outbox。
- **以为开了重试就不会丢：** 重试次数和总时长有上限（`delivery.timeout.ms`），超了会失败，要有 outbox 兜底。
- **以为旧版本默认 acks=all：** 3.0 之前要显式配置。
