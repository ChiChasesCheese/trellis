---
nodes: [problems.foundations.message-queue]
url: https://engineering.linkedin.com/kafka/running-kafka-scale
tags: []
---
# Reflecting on One Year (and 1 Trillion Messages) with Kafka at LinkedIn

值得读：LinkedIn 生产环境的真实披露数字——日均超 8,000 亿条消息、峰值每秒超 1,300 万
条、1,100 多台 broker、60 多个集群、日消费超 650 TB。本题解容量估算部分用的是独立
设定的假设场景（3 亿 DAU、日均 600 亿事件），量级比这篇文章披露的真实规模小一个数量级
左右，此文用于校验本题解算出的 broker 数、存储量级是否落在同一个合理区间，而不是作为
本题场景本身的数据来源。

%% trellis:begin %%
## Source
[Open the original ↗](https://engineering.linkedin.com/kafka/running-kafka-scale)

## Archived copy
![[src-linkedin-message-queue-clip]]
%% trellis:end %%
