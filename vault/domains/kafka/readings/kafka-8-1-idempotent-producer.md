---
nodes:
- eos.idempotent-producer
title: 幂等生产者
corpus: kafka-2e
section: 078-8-1
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 幂等生产者

本节讲解幂等生产者如何依靠生产者ID(PID)与每分区序列号来检测并丢弃重试产生的重复消息，说明它只在单个生产者会话内对单分区生效的局限性，以及如何通过enable.idempotence开启这一特性。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
