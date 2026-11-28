---
id: hi-c-sd-flink-n05-operators
node: sd.deep-dives.flink.notes
type: qa
step: 5
---
## Q
**Flink · 算子：map、filter、窗口、连接**｜摘要 · 必会

Flink 有哪些常见算子？一段"按广告统计 5 分钟点击"的代码做了什么？

## A
- **常见算子：** Map（逐个转换）、Filter（过滤）、FlatMap（一对零或多）、Reduce（按键合并）、Window（按时间或数量分组）、Join（合并两个流）、Aggregate（在窗口或键上聚合）。
- **和 MapReduce 的区别：** 算子兼具 mapper 与 reducer 的作用，但 Flink 是逐条流式处理，不是成批处理。
- **例子的三步：** `keyBy(广告ID)` 把流按键分区成键控流（KeyedStream）；`window(滚动 5 分钟)` 把同一键、同一 5 分钟时段的元素分到一组；`reduce` 把组内点击数相加。
- **结果：** 每个广告每 5 分钟输出一条聚合后的点击数。

```mermaid
flowchart LR
    E["点击流"] --> K["keyBy(广告ID)<br/>键控流"]
    K --> W["window(滚动 5 分钟)"]
    W --> R["reduce：点击数相加"]
    R --> O["每个广告每 5 分钟一条"]
```

- **重点：** `keyBy` 决定同一个键的数据去同一个并行实例，所以每个键的状态在本地、互不干扰。
