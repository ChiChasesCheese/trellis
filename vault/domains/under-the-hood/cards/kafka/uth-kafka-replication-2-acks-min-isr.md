---
id: uth-kafka-replication-2-acks-min-isr
node: kafka.replication
type: qa
step: 2
---
## Q
**acks=all 与 min.insync.replicas**｜Kafka · 4.0

副本因子 3、`acks=all`、`min.insync.replicas=2`：挂 1 台和挂 2 台 broker，写入分别会怎样？

## A
**背景。** 生产者要选“等多少份确认才算写成功”（`acks`）。等得越多越安全，也越容易因为副本不够而写不进去。

**结构。** `acks=all` 要求当前 ISR 里的副本全部确认；`min.insync.replicas` 规定 ISR 至少要有几个，不够就拒绝写入。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 158">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂 1 台</text>
<circle cx="30" cy="38" r="15" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="30" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">L</text>
<circle cx="74" cy="38" r="15" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">F</text>
<circle cx="118" cy="38" r="15" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="118" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂</text>
<text x="170" y="35" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ISR 剩 2 个: 够</text>
<text x="170" y="52" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">照常写入</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂 2 台</text>
<circle cx="30" cy="104" r="15" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="30" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">L</text>
<circle cx="74" cy="104" r="15" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="74" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂</text>
<circle cx="118" cy="104" r="15" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="118" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂</text>
<text x="170" y="101" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">ISR 剩 1 个: 不够</text>
<text x="170" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拒绝写入</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">min.insync.replicas = 2</text>
</svg>
```

**细节。**

- 挂 1 台：ISR 还剩 2 个，满足要求，照常写。
- 挂 2 台：ISR 只剩 1 个，leader 对 `acks=all` 的请求抛 `NotEnoughReplicasException`，高水位也不再前进。
- 生产者 `acks` 从 3.0 起默认 `all`（之前是 1）；`min.insync.replicas` 默认只有 1。

**坑。** “all”指当前 ISR 全体而非全部副本：ISR 缩到 1 个且 `min.insync.replicas=1` 时，`acks=all` 等于只写了 leader。

**对应 LeetCode：** 无直接对应的题
