---
nodes:
- producer.client-basics
title: 同步发送与异步发送
corpus: kafka-2e
section: 031-3-3-kafka
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 同步发送与异步发送

本节对比三种消息发送方式：即发即忘、同步发送(阻塞等待Future结果)和异步发送(通过回调处理结果)，分析它们在延迟、吞吐量和错误处理复杂度上的差异。理解这三种方式的取舍，是后续设置acks、重试等可靠性相关配置的前提。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
