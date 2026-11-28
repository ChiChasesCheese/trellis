---
id: bagu-kafka-architecture-1-structure
node: a.mq.kafka-architecture
type: qa
step: 1
---
## Q
**Kafka 结构 · Topic、分区与消费者组**｜必会

面试官：「短视频发布后，事件要给转码、审核、推荐三个服务各消费一遍。用 Kafka，说一下它的整体结构。」

## A
**基本回答。** 主题（topic）切成多个分区（partition），每个分区是只追加的日志，消息有分区内递增的偏移量（offset）。消费者组内一个分区同一时刻只给一个消费者；不同组各自独立消费。
分区让读写分散到多台 Broker，吞吐才能横向扩展。超过 `retention.ms`（默认 7 天）或大小限制的整段删除；`cleanup.policy=compact` 只保留每个 key 的最新值。元数据由控制器管理，新版本用 KRaft 取代 ZooKeeper。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">转码组：组内一个分区只给一个消费者</text>
<rect x="8" y="26" width="130" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="73.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0：0 1 2 3 →</text>
<line x1="138" y1="41" x2="208" y2="41" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,41.0 201.0,44.2 201.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="208" y="26" width="124" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="270.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者 C1</text>
<rect x="8" y="70" width="130" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="73.0" y="89.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P1：0 1 2 3 →</text>
<line x1="138" y1="85" x2="208" y2="85" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,85.0 201.0,88.2 201.0,81.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="208" y="70" width="124" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="270.0" y="89.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者 C2</text>
<rect x="8" y="114" width="130" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="73.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P2：0 1 2 3 →</text>
<line x1="138" y1="129" x2="208" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,129.0 201.0,132.2 201.0,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="208" y="114" width="124" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="270.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者 C3</text>
<rect x="208" y="158" width="124" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="270.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">消费者 C4：空闲</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">消费者比分区多</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">多出来的空闲</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">审核组、推荐组：各读全部分区，各记各的 offset</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">顺序只在分区内，分区数 = 并行度上限</text>
</svg>
左边三个分区，右边是转码组的消费者：每个分区只连一个消费者，多出来的 C4 没活干。审核组、推荐组也各有一套同样的连线，各自独立。
**举个例子。** 短视频发布事件的 topic 有 3 个分区，三个服务各用一个消费者组。
1. **发布一条事件：**生产者按 key 把它放进某个分区，例如 P1，在 P1 里 offset 是 7。
2. **转码组：**有 3 个消费者，各分到一个分区，C2 读 P1，读到 offset 7 后记下「下次从 8 开始」。
3. **审核组：**独立的 offset，读 P1 时也会读到 offset 7，不受转码组进度影响。
4. **转码慢：**转码组的 offset 落后，审核组照样往前读，互不拖累。
5. **组里多一个人：**转码组加到 4 个消费者，第 4 个分不到分区，空闲；要提高并发就要增加分区数。
**容易错。**
- **以为消费者越多越快：** 超过分区数的消费者是空闲的。
- **以为 topic 内全局有序：** 只有分区内有序。
- **以为不同组会抢消息：** 不同组各自完整消费一遍，互不影响；同组内才是分摊。
- **以为过期是一条一条删：** 按整段（segment）删，不是逐条。
