---
id: hft-measurement-coordinated-omission-fix
node: measurement.coordinated-omission
type: qa
step: 2
---
## Q
怎样修正 coordinated omission（协同遗漏）？“闭环（closed loop）”和“开环（open loop）”测试有什么区别？

## A
两种互补的办法：

1. **按计划发送时间计算延迟**：每个请求在**计划**的时刻就算作开始，延迟 = 实际完成时间 − 计划发送时间，而不是 − 实际发送时间。系统卡住时，被推迟发送的请求依然带着“它本该在那时候发”的账，延迟被如实计入。
2. **开环测试**：按固定速率发送，**不等**上一个响应，像真实市场那样不管你处理完没有数据都会来。闭环则是“发—等—发”，速率被系统速度拖慢。

HdrHistogram 提供 `recordValueWithExpectedInterval`：当你记录了一个远大于预期间隔的值，它自动补上“那段时间里本该观察到的”若干个合成样本。

例：预期间隔 1 ms，记录一个 1 秒的样本，会补上延迟约 999 ms、998 ms、…… 1 ms 的 999 个样本，分布就接近真实情况。

闭环适合测“一个请求最快多久”，开环才适合测“在持续负载下用户会感受到什么”。
