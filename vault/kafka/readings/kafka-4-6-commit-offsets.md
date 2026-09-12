---
nodes:
- consumer.offset-commit
title: 提交和偏移量
corpus: kafka-2e
section: 045-4-6
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 提交和偏移量

本节讲解消费者如何通过提交偏移量追踪消费进度，对比自动提交、手动同步提交、异步提交及同步异步组合提交的优劣，并演示如何提交特定偏移量而非默认的最新偏移量。理解偏移量提交的时机，直接决定应用是否会丢失消息或重复处理消息。
