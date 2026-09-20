---
nodes: [problems.search.ad-click-aggregation]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator
tags: [no-archive]
---
# Ad Click Aggregator Problem Breakdown

值得读：完整走了一遍服务端重定向上报点击、按 ad id 分片摄入、Flink 窗口聚合、批流结合
校验的路线，容量估算和 API 设计示例齐全。本题在此基础上把"为什么去重不能用近似结构"单独
拿出来和 [[solution-top-k]] 对照论证，并把幂等 sink 的 upsert key 确定性要求和
Accumulating & Retracting 触发模式的机制讲得更细，这是它没有展开的部分。
