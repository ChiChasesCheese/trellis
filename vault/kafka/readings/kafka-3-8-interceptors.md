---
nodes:
- producer.extensibility
title: 拦截器：无侵入地修改客户端行为
corpus: kafka-2e
section: 036-3-8
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 拦截器：无侵入地修改客户端行为

本节讲解ProducerInterceptor的onSend和onAcknowledgement两个关键方法，说明如何在不修改业务代码的前提下，给公司所有应用统一加上审计、监控等横切逻辑。是Kafka生产者扩展性机制的最后一块拼图。
