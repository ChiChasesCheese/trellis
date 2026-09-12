---
nodes:
- consumer.poll-config
title: 配置消费者：拉取参数与存活检测
corpus: kafka-2e
section: 044-4-5
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 配置消费者：拉取参数与存活检测

本节详解消费者的一大批配置参数：fetch.min.bytes、fetch.max.wait.ms、max.poll.records等拉取相关参数如何影响吞吐；session.timeout.ms、heartbeat.interval.ms、max.poll.interval.ms等存活检测参数如何影响故障发现速度；以及auto.offset.reset等其他重要选项。是消费者调优必读的一章。
