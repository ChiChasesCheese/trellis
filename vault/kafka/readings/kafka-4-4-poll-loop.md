---
nodes:
- consumer.client-basics
title: 轮询循环与线程安全
corpus: kafka-2e
section: 043-4-4
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 轮询循环与线程安全

本节讲解消费者API的核心——poll()轮询循环的写法，以及为什么一个消费者实例不能被多个线程同时使用(线程安全约束)。理解轮询循环的运作方式，是编写任何消费者应用程序的基础。
