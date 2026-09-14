---
nodes:
- reliability.broker-config
title: broker配置：复制系数、不彻底首领选举与最少同步副本
corpus: kafka-2e
section: 072-7-3-broker
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# broker配置：复制系数、不彻底首领选举与最少同步副本

本节讲解三个决定消息存储可靠性的broker配置参数：复制系数决定容错能力；不彻底的首领选举(unclean leader election)在牺牲一致性换取可用性之间做取舍；min.insync.replicas与acks=all配合，确保至少多少个副本确认写入才算成功。是可靠性配置的核心一节。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
