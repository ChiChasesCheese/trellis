---
nodes:
- practice.sizing-tuning
title: 生产环境部署前的准备：GC选择与数据中心布局
corpus: kafka-2e
section: 026-2-7
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 生产环境部署前的准备：GC选择与数据中心布局

本节讲解将Kafka部署到生产环境前的收尾工作，重点是Java垃圾回收器的选择（如G1GC）对延迟稳定性的影响，以及数据中心内broker和ZooKeeper节点的物理布局策略。是“硬件选型”之外，运维Kafka集群走向生产就绪必须补齐的软件层面调优知识。
