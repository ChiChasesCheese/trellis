---
nodes: [problems.foundations.message-queue]
url: https://www.confluent.io/blog/incremental-cooperative-rebalancing-in-kafka/
tags: []
---
# Incremental Cooperative Rebalancing in Apache Kafka: Why Stop the World When You Can Change It?

值得读：eager rebalance（stop-the-world）与增量协作式 rebalance（KIP-429）的实测
对比，给出具体数字——900 个任务/3 个 worker 场景下，稳定耗时从 12–14 分钟降到约
1 分钟，聚合吞吐从 252.68 MB/s 提升到 537.81 MB/s。本题解「深入探讨」第 4 节引用了
这组数字来说明消费者组协调协议的改进幅度；这篇文章测的是 Kafka Connect 任务分配
场景，本题解在引用时明确标注了这一点，没有把它直接当作纯消费者组场景的测量结果。
