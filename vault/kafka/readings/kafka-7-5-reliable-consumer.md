---
nodes:
- reliability.consumer-reliable
title: 在可靠的系统中使用消费者
corpus: kafka-2e
section: 074-7-5
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 在可靠的系统中使用消费者

本节讲解消费者的可靠性配置(如enable.auto.commit、auto.offset.reset)以及手动提交偏移量的正确时机，避免消息在处理前就被标记为已消费而造成丢失，或重复消费同一条消息。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
