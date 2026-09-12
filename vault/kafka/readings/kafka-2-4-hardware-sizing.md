---
nodes:
- practice.sizing-tuning
title: 为Kafka选择合适的硬件
corpus: kafka-2e
section: 023-2-4
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 为Kafka选择合适的硬件

本节逐项分析磁盘吞吐量、磁盘容量、内存、网络和CPU这五个维度如何影响Kafka broker的性能表现，并给出各维度的选型经验，比如磁盘吞吐优先于容量、内存主要服务于页面缓存而非JVM堆。是规划生产集群硬件配置前必须掌握的基础知识。
