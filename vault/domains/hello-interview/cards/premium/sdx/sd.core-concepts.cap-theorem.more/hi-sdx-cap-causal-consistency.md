---
id: hi-sdx-cap-causal-consistency
node: sd.core-concepts.cap-theorem.more
type: qa
step: 2
---
## Q
**因果一致：保证什么、不保证什么**｜补充 · CAP 定理 · 追问

面试官：「最终一致的论坛里，用户有时先看到回复「不是的」，再刷出它回答的问题「地球是平的吗」。用什么一致性保证能防止这种事？它故意不保证什么？」

## A
**结论。** 因果一致（causal consistency）：如果写 B 是看过写 A 之后才做的，所有节点必须先应用并展示 A 再展示 B。彼此没有因果路径的并发写则不排序。

**要点。**
- **因果的成因：** 同一会话里的先后操作、先读后写（读到 A 再写 B）、回复针对某条已存在的问题。
- **实现方式：** 每条写带上它依赖的版本（版本向量或依赖列表）；副本在依赖没到齐前先缓存这条写，不展示。
- **故意不排序并发写：** 没有因果关系的两条写，不同节点可以看到不同顺序。省下的就是这部分协调成本。
- **为什么比线性一致便宜：** 不需要为每次读写跨节点等待；分区时两侧各自继续服务，依赖没到齐的写等分区恢复再放行。它是分区时仍能保持可用的模型里最强的一档。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 248">
<rect x="10" y="8" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写 Q：「地球是平的吗」</text>
<text x="85.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">节点 1 先收到</text>
<rect x="180" y="8" width="150" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="255.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写 R：「不是的」</text>
<text x="255.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">依赖 Q（看过 Q 才写）</text>
<text x="8" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">节点 3 的到达顺序：先 R，后 Q</text>
<rect x="10" y="84" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">R 先到：依赖 Q 未到</text>
<text x="85.0" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先缓存，不展示</text>
<polyline points="85,128 85.0,143.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="85,150 81.8,143.0 88.2,143.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="150" width="150" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Q 到达</text>
<text x="85.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">依赖满足，放行</text>
<polyline points="160,172 189.0,172.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196,172 189.0,175.2 189.0,168.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="196" y="150" width="134" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="263.0" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先展示 Q</text>
<text x="263.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再展示 R</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">没有因果关系的并发写不排序，</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不同节点可以看到不同顺序。</text>
</svg>

**面试里这样说。** 「回复带着它依赖的问题的版本，副本没收到问题就先缓存回复。这样不需要全局排序，分区时也能继续服务；两条互不相关的帖子顺序不同，我接受。」

**易错。**
- **用时间戳当因果：** 各机器时钟有偏差，回复的时间戳可能比问题还早，仍会「答在问前」。要靠依赖信息或逻辑时钟。
- **以为最终一致自带因果：** 最终一致只承诺最后收敛，中间顺序可以乱。
- **说成全局顺序：** 因果一致只排有依赖的操作，不是所有节点看到同一串顺序。
