---
nodes:
- core.topics-partitions
title: broker与主题的默认配置：从num.partitions说起
corpus: kafka-2e
section: 022-2-3-broker
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# broker与主题的默认配置：从num.partitions说起

本节讲解broker常规配置参数(broker.id、listeners、log.dirs等)，重点是主题默认配置中的num.partitions——如何根据生产者/消费者的目标吞吐量反推分区数量，以及replication.factor的选择建议(RF++)。这是把“主题划分为分区以获得并行度”这一核心概念落到实际配置决策的第一课。
