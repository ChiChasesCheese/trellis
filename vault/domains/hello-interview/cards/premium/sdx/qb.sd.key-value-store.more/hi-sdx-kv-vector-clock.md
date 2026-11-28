---
id: hi-sdx-kv-vector-clock
node: qb.sd.key-value-store.more
type: qa
step: 3
---
## Q
**向量时钟：怎么判先后、并发和截断**｜补充 · 分布式键值存储 · 追问

面试官：「Dynamo 式存储在网络分区时，两个客户端把同一个购物车键写到了不同的节点。用时间戳『最后写入胜出』有什么危险？向量时钟怎么判断先后与并发，代价是什么？」

## A
**结论。** 最后写入胜出依赖各机时钟，较晚的写可能带较小的时间戳而被悄悄丢掉。向量时钟给每个版本记一组 {节点: 计数}，能区分「后继」和「并发」，并发的版本都保留，交给应用合并；代价是元数据增长，需要截断。

**要点。**
- **规则：** 每次写由处理它的节点把自己的计数加一。版本 X 的每个分量都不小于 Y，且至少一个更大，则 X 取代 Y；否则两者并发。
- **例子：** 起点 {A:1}。一个客户端经节点 A 写成 {A:2}；另一个在分区另一侧经节点 B 写成 {A:1,B:1}。互不支配，所以并发，两个都保留。
- **读时返回全部 sibling：** 应用合并（购物车取并集，删除要用墓碑，否则删掉的商品会复活），再带着合并后的上下文写回，新版本支配两者。
- **截断：** 元数据随写入节点数增长。Dynamo 论文的做法是超过阈值（论文举例 10 对）就丢弃最旧的一对，偶尔会把真正的祖先当成并发，多出一个无害的 sibling。
- **对比：** LWW 简单，但静默丢写；Cassandra 用按列的 LWW 加时间戳。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<rect x="120" y="8" width="100" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{A:1}</text>
<rect x="20" y="86" width="100" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="70.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{A:2}</text>
<rect x="220" y="86" width="100" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="270.0" y="104.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{A:1,B:1}</text>
<polyline points="150,36 80,86" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80.0,86.0 87.6,84.5 83.8,79.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="68" y="66" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">经 A 写</text>
<polyline points="190,36 260,86" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260.0,86.0 256.2,79.3 252.4,84.5" style="fill:var(--accent,#3b6fd4)"/>
<text x="272" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">经 B 写</text>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">并发</text>
<rect x="70" y="160" width="200" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="178.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">{A:2,B:1,C:1}</text>
<polyline points="70,114 130,160" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,160.0 126.4,153.2 122.5,158.3" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="270,114 210,160" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210.0,160.0 217.5,158.3 213.6,153.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="330" y="146" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合并后写回</text>
<text x="10" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">互不支配 = 并发：两个都留，由应用合并</text>
</svg>

**面试里这样说。** 「购物车不能用最后写入胜出，时钟偏差会丢写。我用向量时钟：互相不支配就是并发，读时返回 sibling 由应用取并集合并；元数据靠阈值截断，代价是偶尔多一个 sibling。」

**易错。**
- **以为向量时钟能自动合并：** 它只检测并发，合并要靠应用。
- **用墙钟时间戳当版本：** 机器时钟不可靠。
