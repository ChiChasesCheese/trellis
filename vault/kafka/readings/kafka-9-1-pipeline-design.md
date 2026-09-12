---
nodes:
- connect.pipeline-design
title: 构建数据管道时需要考虑的问题
corpus: kafka-2e
section: 083-9-1
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 构建数据管道时需要考虑的问题

本节梳理设计数据管道时的八个关键考量：及时性、可靠性、吞吐量(含峰值处理能力)、数据格式、转换逻辑该放在哪个环节、安全性、故障处理，以及系统间的耦合性与灵活性。是评估任何数据集成方案(不局限于Kafka Connect)的通用框架。
