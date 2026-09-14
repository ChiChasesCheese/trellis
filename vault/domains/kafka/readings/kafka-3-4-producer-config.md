---
nodes:
- producer.acks-durability
- producer.batching-throughput
- producer.timeouts-retries
- producer.idempotence-ordering
title: 生产者关键配置：acks、批处理与幂等性
corpus: kafka-2e
section: 032-3-4
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 生产者关键配置：acks、批处理与幂等性

本节系统讲解生产者最重要的一批配置参数：acks决定消息被判定为已确认前需要写入多少副本；linger.ms、batch.size、buffer.memory、compression.type共同决定吞吐与延迟的取舍；传递超时体系与max.in.flight.requests.per.connection影响重试与消息顺序；enable.idempotence则消除重试带来的重复写入。是生产者调优的核心一章。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
