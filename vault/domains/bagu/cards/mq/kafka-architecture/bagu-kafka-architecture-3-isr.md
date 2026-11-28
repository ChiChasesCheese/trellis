---
id: bagu-kafka-architecture-3-isr
node: a.mq.kafka-architecture
type: qa
step: 3
---
## Q
**Kafka 结构 · ISR 与 acks=all 的真实含义**｜必会

面试官：「ISR 是什么？副本什么情况下被踢出？acks=all 是不是写了所有副本才返回？」

## A
**基本回答。** ISR（in-sync replicas，同步副本集合）是与 leader 保持同步的副本集合，包含 leader。follower 超过 `replica.lag.time.max.ms`（默认 30 秒）没追上就被踢出。`acks=all` 的真实含义是写入当前 ISR 的所有副本，不是全部副本。
`unclean.leader.election.enable=false`（默认）时只有 ISR 里的副本能当新 leader。Kafka 4.1 起新集群默认启用 ELR：ISR 低于 min.insync.replicas 时高水位不再推进，controller 记录不在 ISR 但仍安全的副本，选主按 ISR、ELR、最后已知 leader 的顺序，减少为恢复可用性而开 unclean 选举的需要（4.0 只是预览）。
**2026 亮点。** Kafka 4.1 起新集群默认启用 ELR：ISR 低于 min.insync.replicas 时高水位不再推进，controller 记录「不在 ISR 但仍安全」的副本，选主按 ISR、ELR、最后已知 leader 的顺序，减少为恢复可用性而开 unclean 选举的需要；4.0 里只是预览且默认关闭。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<rect x="8" y="4" width="324" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ISR = { leader, F1, F2 }</text>
<line x1="80" y1="34" x2="80" y2="54" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,54.0 76.8,47.0 83.2,47.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="92" y="49" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F2 超过 30 秒没追上，被踢出</text>
<rect x="8" y="54" width="324" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="73.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ISR = { leader, F1 }</text>
<line x1="80" y1="84" x2="80" y2="104" stroke-width="1.2" stroke="currentColor"/>
<polygon points="80.0,104.0 76.8,97.0 83.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="92" y="99" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">F1 也掉队（网络抖动、磁盘慢、GC）</text>
<rect x="8" y="104" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ISR = { leader }</text>
<line x1="86" y1="134" x2="86" y2="160" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,160.0 82.8,153.0 89.2,153.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="254" y1="134" x2="254" y2="160" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,160.0 250.8,153.0 257.2,153.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="160" width="156" height="40" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有 min.insync：</text>
<text x="86.0" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">acks=all 退化成 acks=1</text>
<rect x="176" y="160" width="156" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254.0" y="176.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">min.insync.replicas=2</text>
<text x="254.0" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入失败并报警</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">落后副本当 leader（unclean）会丢已确认的消息</text>
</svg>
从上往下是 ISR 逐步缩小的过程；缩到只剩 leader 时，有没有 min.insync.replicas 结果完全不同。
**举个例子。** 支付成功事件的 topic，replication.factor=3。
1. **起点：**ISR = {leader, F1, F2}，三份都在。
2. **F2 网络抖动：**超过 30 秒没追上，被踢出，ISR = {leader, F1}。此时 `acks=all` 要等 leader 和 F1 两个都写入。
3. **F1 也掉队：**ISR = {leader}。
4. **没配 min.insync：**`acks=all` 等于 `acks=1`，写入只存 leader 一份；这时 leader 一挂，消息就丢了。
5. **配了 min.insync.replicas=2：**ISR 只有 1 个，不满足，写入失败并报警，运维能及时发现。
**容易错。**
- **以为 acks=all 等于所有副本：** 是当前 ISR 的所有副本。
- **只配 acks=all 不配 min.insync：** ISR 缩到 1 个时形同 acks=1。
- **以为 ISR 是固定的：** 它是动态的，掉队就移出，追上就回来。
- **为了可用性打开 unclean 选举：** 会丢掉已确认的消息，默认关闭，不要轻易开。
