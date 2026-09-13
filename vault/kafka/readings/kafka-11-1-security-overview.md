---
nodes:
- security.protocols-auth-encryption
title: 锁住Kafka：安全模型总览
corpus: kafka-2e
section: 089-11-1-kafka
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 锁住Kafka：安全模型总览

本节以Alice向Bob发送订单消息为例，逐步说明数据在Kafka集群中流动的每一步(写入首领、复制到跟随者、被消费)需要保证客户端真实性、服务器端真实性、数据隐私、数据完整性、访问控制、可审计性和可用性。是理解整章安全特性(身份验证、授权、加密、审计、配额)如何组合成完整安全模型的总纲。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
