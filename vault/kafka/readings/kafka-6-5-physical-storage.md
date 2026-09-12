---
nodes:
- internals.tiered-storage
- internals.storage-segments
- internals.indexes
- internals.compaction
title: 物理存储：分层存储、分区分配、索引与压实
corpus: kafka-2e
section: 067-6-5
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 物理存储：分层存储、分区分配、索引与压实

本节系统讲解Kafka的存储层：分层存储如何把冷数据下沉到远程对象存储从而把保留期与本地磁盘容量解耦；分区与副本在broker间及磁盘目录间的分配策略；日志如何被切分为片段文件及其文件格式；偏移量索引和时间索引如何加速消息定位；日志压实如何为每个键保留最新值及其工作原理与配置。内容较长，是理解Kafka存储内部机制最完整的一节。
