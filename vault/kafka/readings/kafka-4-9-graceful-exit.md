---
nodes:
- consumer.client-basics
title: 如何优雅退出轮询循环
corpus: kafka-2e
section: 048-4-9
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 如何优雅退出轮询循环

本节讲解如何通过consumer.wakeup()从另一个线程安全地中断正在阻塞的poll()调用，并捕获WakeupException完成优雅退出，避免消费者在关闭时丢失未提交的偏移量或产生资源泄漏。
