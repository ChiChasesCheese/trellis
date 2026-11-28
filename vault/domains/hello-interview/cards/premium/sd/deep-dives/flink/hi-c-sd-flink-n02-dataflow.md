---
id: hi-c-sd-flink-n02-dataflow
node: sd.deep-dives.flink.notes
type: qa
step: 2
---
## Q
**Flink · Flink 的核心抽象：数据流图**｜摘要 · 必会

Flink 把一个计算描述成什么？开发者负责什么，框架负责什么？

## A
- **数据流引擎（dataflow engine）：** 计算被描述成一张有向图：节点是对数据的操作，叫算子（operator）；边是在算子之间流动的数据，叫流（stream）。
- **起点和终点：** 图的起点叫源（source），终点叫汇（sink）。
- **分工：** 开发者定义这张图，Flink 负责安排资源去执行，包括拆分任务、调度、容错。

```mermaid
flowchart LR
    S["源 source"] -->|"流"| O1["算子 operator"]
    O1 -->|"流"| O2["算子 operator"]
    O2 -->|"流"| K["汇 sink"]
```

- **记忆方式：** 源 → 若干算子 → 汇，边是流。
