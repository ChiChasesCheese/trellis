---
nodes: [problems.geo.ride-hailing]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber
tags: [no-archive]
---
# Uber

值得读：Hello Interview 对这道题的深入拆解，给出了撮合并发正确性（用短 TTL 分布式锁
防止同一司机被重复绑定，锁失败直接跳到下一候选人）、Kafka 排队削峰、以及用
Temporal/Step Functions 这类持久化执行框架处理超时重试的思路。本题解在锁机制的核心
判断上与它一致；与本题解不同的地方在于：本题解用 Uber 真实披露的 2025 年第四季度
经营数据（日行程数、月活司机数）重新推导了摄入 QPS 和撮合 QPS 的具体数字，而不是
采用一个未说明来源的"同一位置 10 万并发请求"规模假设。
