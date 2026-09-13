---
nodes:
- monitoring.lag-e2e
title: 滞后监控：消费者落后了多少
corpus: kafka-2e
section: 118-13-5
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 滞后监控：消费者落后了多少

本节讲解消费滞后(consumer lag)的含义——分区最后一条消息与消费者已读取消息之间的差值，并说明为什么用外部监控工具比单纯依赖客户端自带的滞后指标更可靠，避免只看到滞后最大的那个分区而误判整体情况。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
