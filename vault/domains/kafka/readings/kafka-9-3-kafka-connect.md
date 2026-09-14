---
nodes:
- connect.connect-basics
- connect.smt
title: Kafka Connect：worker、连接器与单一消息转换
corpus: kafka-2e
section: 085-9-3-kafkaconnect
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# Kafka Connect：worker、连接器与单一消息转换

本节讲解Connect如何以worker集群形式运行source/sink连接器插件来移动数据，通过文件和MySQL到ElasticSearch的例子说明连接器的实际用法，并介绍单一消息转换(SMT)如何在不写代码的情况下对流经Connect的记录做轻量加工，如过滤字段、重命名主题等。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
