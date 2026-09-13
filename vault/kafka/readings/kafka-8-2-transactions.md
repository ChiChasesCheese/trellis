---
nodes:
- eos.transactions
title: 事务：跨分区的原子写入
corpus: kafka-2e
section: 079-8-2
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 事务：跨分区的原子写入

本节讲解Kafka事务如何让一次写入跨越多个分区保持原子性，介绍事务ID的作用、read_committed与read_uncommitted两种隔离级别的区别，以及事务能解决哪些问题(如流式处理的精确一次)、不能解决哪些问题(如无法保证消费端的幂等)。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
