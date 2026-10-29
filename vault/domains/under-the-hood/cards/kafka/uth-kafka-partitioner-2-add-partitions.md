---
id: uth-kafka-partitioner-2-add-partitions
node: kafka.partitioner
type: qa
step: 2
---
## Q
**加分区会打乱 key**｜Kafka · 4.0

一个主题从 6 个分区扩到 7 个，已有的 key 会怎样？

## A
**背景。** 分区号是 `hash % N`，N 是分区数。N 一变，同一个 hash 取余的结果通常也跟着变。

**结构。** 下图把 hash 从 0 排到 13，对比 `% 6` 和 `% 7`：只有 0 到 5 的结果相同，之后全不一样。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 136">
<text x="8" y="17" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash</text>
<text x="8" y="40" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">% 6</text>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">% 7</text>
<text x="62" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="52" y="24" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="62" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="52" y="56" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="62" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="82" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="72" y="24" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="82" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="72" y="56" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="82" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="102" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="92" y="24" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="102" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="92" y="56" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="102" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="122" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="112" y="24" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="112" y="56" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="122" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="142" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="132" y="24" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="142" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="132" y="56" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="142" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="162" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="152" y="24" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="162" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="152" y="56" width="20" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="162" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="182" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="172" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="182" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="172" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="182" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="202" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="192" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="202" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="192" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="202" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="222" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="212" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="212" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="242" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<rect x="232" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="242" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="232" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="242" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="262" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<rect x="252" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="252" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="282" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11</text>
<rect x="272" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="272" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="302" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<rect x="292" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="292" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="322" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">13</text>
<rect x="312" y="24" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="322" y="39.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="312" y="56" width="20" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="322" y="71.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="170" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hash 0-5 不变, 其余都换了分区</text>
<text x="170" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每 42 个 hash 只有 6 个不变</text>
</svg>
```

**细节。**

- `hash % 6` 与 `hash % 7` 只在 `hash` 对 42 取余落在 0–5 时相等，即约 1/7 的 key 不动，约 6/7 换了分区。
- 公式在 `BuiltInPartitioner.partitionForKey`，只看 key 字节和当前分区数，不记任何历史。

**坑。** 同一个 key 的新旧消息进了不同分区，“按 key 有序”的保证就断了；压实主题里同一个 key 还会在两个分区各留一份。

**为什么。** 取模不记状态，代价是扩容几乎全部重新分布；一致性哈希（把 key 和机器都放到一个环上，新增机器只接管相邻的一段）只需搬走约 1/N 的 key。

**对应 LeetCode：** 无直接对应的题
