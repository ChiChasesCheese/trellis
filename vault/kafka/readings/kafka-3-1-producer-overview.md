---
nodes:
- producer.client-basics
title: 生产者概览：一条消息的发送流程
corpus: kafka-2e
section: 029-3-1
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 生产者概览：一条消息的发送流程

本节以图示方式讲解一条消息从ProducerRecord创建、序列化、经过分区器选择分区、被放入批次，到最终发送给broker并收到RecordMetadata响应或错误的完整流程。在深入学习各项生产者配置之前，先建立这张全局流程图，能帮助理解后续每个配置参数具体作用在流程的哪个环节上。
