---
nodes:
- connect.connect-basics
title: 何时使用Connect API或客户端API
corpus: kafka-2e
section: 084-9-2-connect-api-api
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 何时使用Connect API或客户端API

本节回答一个实际问题：向Kafka读写数据时，什么时候该用原生的生产者/消费者客户端，什么时候该用Connect API和现成的连接器。理解这个边界，能避免重复造轮子，也能避免滥用Connect处理本该用客户端API实现的定制逻辑。
