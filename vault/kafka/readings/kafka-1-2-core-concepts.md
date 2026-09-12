---
nodes:
- core.topics-partitions
- core.offsets
- core.cluster-roles
title: Kafka核心概念全景：消息、主题、偏移量、broker与集群
corpus: kafka-2e
section: 014-1-2-kafka
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# Kafka核心概念全景：消息、主题、偏移量、broker与集群

本节一次性引入Kafka最重要的一批术语：消息与批次、模式(schema)、主题如何切分为分区以获得并行与顺序、生产者与消费者的角色、偏移量如何标记消费进度，以及broker如何组成集群、为何需要多集群。是理解全书后续内容的词汇表和地图，建议逐字理解每个术语再往下读。
