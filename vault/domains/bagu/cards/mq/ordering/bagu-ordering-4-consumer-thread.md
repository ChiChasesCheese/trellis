---
id: bagu-ordering-4-consumer-thread
node: a.mq.ordering
type: qa
step: 3
---
## Q
**消息顺序 · 消费端多线程**｜必会

面试官：「分区里的消息有序了，但我在消费者里把消息丢进线程池并行处理，顺序还在吗？」

## A
**基本回答。** 不在。丢进线程池并行处理，同 key 的消息会被不同线程并发执行，顺序就乱了。要按 key 路由到固定的内部线程队列：同 key 串行，不同 key 并行。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 246">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分区里的消息（key 为 A 或 B）</text>
<rect x="8" y="24" width="44" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="30.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A1</text>
<rect x="60" y="24" width="44" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B1</text>
<rect x="112" y="24" width="44" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="134.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A2</text>
<rect x="164" y="24" width="44" height="26" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="186.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B2</text>
<line x1="30" y1="50" x2="30" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="30.0,78.0 26.8,71.0 33.2,71.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="222" y1="50" x2="254" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,78.0 246.6,75.8 250.8,71.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="74" y="68" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash(key) % 2</text>
<rect x="8" y="78" width="156" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 0：A1，A2</text>
<rect x="176" y="78" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 1：B1，B2</text>
<line x1="86" y1="108" x2="86" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,128.0 82.8,121.0 89.2,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="254" y1="108" x2="254" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="254.0,128.0 250.8,121.0 257.2,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="128" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="86.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 0 串行处理</text>
<rect x="176" y="128" width="156" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="254.0" y="147.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1 串行处理</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同 key 串行，不同 key 并行</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列有界：满了暂停拉取（反压）</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">offset 只能提交到连续已完成的最小位置</text>
</svg>
分区里的消息按 key 哈希到两个内部队列，每个队列只有一个线程消费：A 的消息永远在队列 0 里按顺序处理，B 的在队列 1。
**举个例子。** 分区里依次来了 4 条：A1、B1、A2、B2（A、B 是两个用户 ID），N=2。
1. **哈希：**hash(A) % 2 = 0，hash(B) % 2 = 1（假设）。
2. **分发：**A1、A2 进队列 0，B1、B2 进队列 1。
3. **处理：**线程 0 先做 A1 再做 A2；线程 1 先做 B1 再做 B2；两个线程同时进行。
4. **如果用普通线程池：**A1 和 A2 可能分给两个线程，A2 先做完，A 的先后就乱了。
5. **提交 offset：**A1、B1 做完、A2 还没完时，只能提交到 A2 之前。
**容易错。**
- **以为分区内有序，消费端随便并发：** 线程池会打乱同 key 的先后。
- **退回单线程保序：** 吞吐只有几十条每秒，不能这样。
- **队列无界：** 慢了就撑爆内存，要有界并反压。
- **提交了还没做完的 offset：** 崩溃就丢消息，只能提交连续已完成的位置。
- **再平衡时直接交出分区：** 新旧消费者可能并发处理同一个 key。
