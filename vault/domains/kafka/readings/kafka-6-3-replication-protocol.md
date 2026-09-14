---
nodes:
- core.replication-isr
- internals.replication-protocol
title: 复制协议：首领、跟随者与ISR
corpus: kafka-2e
section: 065-6-3
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 复制协议：首领、跟随者与ISR

本节讲解首领副本与跟随者副本的分工、跟随者如何通过发送Fetch请求追赶首领、broker如何根据replica.lag.time.max.ms判定副本是否失去同步资格并移出ISR，以及首选首领的概念。是理解Kafka可靠性与容错能力的核心机制。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
