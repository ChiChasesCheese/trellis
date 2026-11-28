---
id: hi-c-sd-flink-n09-job
node: sd.deep-dives.flink.notes
type: qa
step: 9
---
## Q
**Flink · 定义一个作业**｜摘要 · 必会

一个 Flink 作业的代码骨架是什么？

## A
- **入口：** 先拿到流执行环境（`StreamExecutionEnvironment`）。
- **四段：** ① 定义源（如读 Kafka 的 `clicks` 主题）；② 定义转换（`keyBy` 用户、5 分钟事件时间滚动窗口、聚合）；③ 定义汇（如写 Elasticsearch）；④ 调用 `execute` 提交作业。
- **读法：** 掌握上述概念后，代码就是在描述一张数据流图：源、一串算子、汇。
- **面试提示：** 不需要背 API，但要能讲清源是什么、键是什么、窗口是什么、汇是什么。
