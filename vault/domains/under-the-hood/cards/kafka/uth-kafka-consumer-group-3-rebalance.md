---
id: uth-kafka-consumer-group-3-rebalance
node: kafka.consumer-group
type: qa
step: 4
---
## Q
**再平衡：整组暂停还是只搬该搬的**｜Kafka · 4.0

消费者组里加入一个新成员，所有人都要停下来重新领分区吗？4.0 的新协议改了什么？

## A
**背景。** 再平衡期间，被收回的分区没人读，消息只能堆着。停得越久、搬得越多，延迟越大。

**结构。** 经典协议里，协调者收齐成员后，由其中一个消费者在客户端算出分配方案，再下发给大家。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">急切 (eager)</text>
<text x="8" y="31" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C0</text>
<rect x="34" y="22" width="96" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="22" width="74" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="204" y="22" width="124" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="8" y="47" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C1</text>
<rect x="34" y="38" width="96" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="38" width="74" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="204" y="38" width="124" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="8" y="63" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C2</text>
<rect x="34" y="54" width="96" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="54" width="74" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<rect x="204" y="54" width="124" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="167" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">整组暂停</text>
<text x="8" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">合作 (cooperative)</text>
<text x="8" y="123" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C0</text>
<rect x="34" y="114" width="294" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="8" y="139" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C1</text>
<rect x="34" y="130" width="120" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="154" y="130" width="30" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="184" y="130" width="144" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="8" y="155" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">C2</text>
<rect x="34" y="146" width="120" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="154" y="146" width="30" height="11" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="184" y="146" width="144" height="11" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="169" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只停搬走的分区</text>
</svg>
```

**细节。**

- 急切（eager）协议：每个成员先交回全部分区，等新方案，再重新领取，整组暂停。
- 合作（cooperative）协议：只收回要搬走的分区，其余继续消费。
- 新协议（KIP-848，`group.protocol=consumer`）4.0 起正式可用：分配改在 broker 端算，成员靠心跳（定时报一声“我还活着”）增量更新；4.0 客户端默认仍是 classic。

**为什么。** 把分配搬到协调者、去掉“全组等齐”的同步屏障，大组再平衡才不会整体抖动。

**对应 LeetCode：** 无直接对应的题
