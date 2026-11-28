---
id: bagu-partition-count-1-how-many
node: b.mq.partition-count
type: qa
step: 1
---
## Q
**Kafka 分区数 · 怎么定、为什么只增不减**｜追问

面试官：「评论 topic 要上线，分区数你打算设多少？流量涨了以后还能再改吗？」

## A
**基本回答。** 按压测结果估：分区数 ≥ max(目标吞吐 ÷ 单分区生产吞吐, 目标吞吐 ÷ 单分区消费吞吐)，再留余量。分区只能增不能减，所以第一次就要留足。
算例（假设压测数字）：目标 300MB/s，单分区生产 30MB/s、消费 15MB/s，分别要 10 个和 20 个，取 20，再留 50% 余量约 30 个。分区不是越多越好：每个分区是目录和文件句柄，leader 选举和重平衡变慢，复制更多分区使端到端延迟上升，单 broker 建议控制在几千以内，客户端按分区缓冲内存变大。Pulsar 5.0 的 Scalable Topics 由 broker 按负载拆合键范围并保持按键有序，没有固定分区数的问题，但刚成为 LTS，只有 Java v5 客户端、暂不支持跨地域复制。
**2026 亮点。** Pulsar 5.0 的 Scalable Topics 由 broker 按负载拆合键范围的段并保持按键有序，没有固定分区数问题；Kafka 仍是分区只增不减。但它刚成为 LTS，只有 Java v5 客户端、暂不支持跨地域复制。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3 个分区：7 % 3 = 1</text>
<rect x="10" y="26" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="62" y="26" width="46" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="114" y="26" width="46" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="137" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<text x="180" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">4 个分区：7 % 4 = 3</text>
<rect x="180" y="26" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="197" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p0</text>
<rect x="218" y="26" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p1</text>
<rect x="256" y="26" width="34" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p2</text>
<rect x="294" y="26" width="34" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="311" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p3</text>
<text x="10" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">旧消息在 p1</text>
<text x="180" y="78" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新消息去了 p3</text>
<text x="10" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一 key 的新旧消息分在两处，顺序乱了</text>
<text x="10" y="126" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">分区数 ≥ 下面两个数里较大的：</text>
<text x="22" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">目标吞吐 ÷ 单分区生产吞吐</text>
<text x="22" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">目标吞吐 ÷ 单分区消费吞吐</text>
<text x="10" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">例：300÷30=10，300÷15=20，取 20，</text>
<text x="10" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">再留 50% 余量，约 30 个</text>
<text x="10" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区只增不减，第一次就留足</text>
</svg>
上方对比 3 个分区和 4 个分区时同一个哈希值 7 落到的位置：从 p1 变成了 p3；下方是分区数的估算公式和算例。
**举个例子。** 评论 topic，起初 3 个分区，按用户 ID 做 key：
1. **起初：** 用户 U 的哈希值是 7，7 % 3 = 1，U 的评论都进 p1，在 p1 内严格有序。
2. **流量翻倍：** 临时把分区扩到 4 个。
3. **映射变了：** 7 % 4 = 3，U 的新评论进了 p3，旧评论还在 p1。
4. **顺序被打乱：** 消费者读 p1 和 p3 的速度不同，U 的两条评论可能先看到新的、后看到旧的。
5. **事前怎么办：** 设计时就按峰值预估，留足余量；真的要扩，新建分区更多的 topic，等旧 topic 消费完再切换，同一 key 的顺序就不会乱。
**容易错。**
- **以为分区越多越好：** 分区多了选举、重平衡、复制和内存开销都上升。
- **以为扩分区没有代价：** 它会改变 key 到分区的映射，同 key 的顺序被打乱。
- **以为消费者越多越快：** 消费者数超过分区数，多出来的空闲。
- **以为可以随时减分区：** Kafka 不支持，只能迁到新 topic。
