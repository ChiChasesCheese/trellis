---
nodes:
- monitoring.client-metrics
title: 配额与节流：限制客户端对broker资源的占用
corpus: kafka-2e
section: 037-3-9
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 配额与节流：限制客户端对broker资源的占用

本节介绍Kafka的生产、消费、请求三种配额类型，说明如何限制客户端发送/接收数据的字节速率以及请求处理时间占比，防止个别客户端占满broker资源影响其他客户端。是理解客户端指标与多租户资源隔离机制的重要一环。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
