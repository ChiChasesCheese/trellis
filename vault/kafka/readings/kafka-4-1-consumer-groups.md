---
nodes:
- consumer.groups-rebalance
title: 消费者与消费者群组
corpus: kafka-2e
section: 040-4-1-kafka
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 消费者与消费者群组

本节解释消费者群组如何让多个消费者共同分摊一个主题的分区，分区再均衡在群组成员变化时如何被触发，以及群组固定成员(static membership)如何通过保留身份减少不必要的再均衡。是理解Kafka横向扩展消费能力的核心机制。
