---
id: tc-tradeoff-language
node: t06.trade-off-language
type: qa
step: 1
tags: [惯用说法]
---
## Q
**Trade-off language · 取舍的说法**｜惯用说法 · 必会

面试官问："Why a message queue instead of calling the service directly?" 你想说它的好处是解耦，代价是复杂度和最终一致。英文怎么把取舍说清楚？

## A
**可以这么说：**
- "The upside is that the services are decoupled. The cost is added complexity."
- "We trade strict consistency for availability."
- "The downside is latency, but in this case it's acceptable."
- "On one hand, X is simpler. On the other hand, Y scales better."
- "I'd pick A because we care more about throughput than ordering."

**别这么说：**
- "It's better." 没说在什么标准下更好。
- "No downsides." 面试官会认为你没想过。

**语气：** 先说好处，再说代价，最后**回到约束**说你的选择：因为我们更在意什么。每个方案至少说一个代价。

<details class="pt" markdown="1"><summary>出处</summary>

惯用说法，非引用

</details>
