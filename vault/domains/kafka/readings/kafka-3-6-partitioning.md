---
nodes:
- producer.extensibility
title: 分区：默认策略与自定义分区器
corpus: kafka-2e
section: 034-3-6
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 分区：默认策略与自定义分区器

本节讲解ProducerRecord如何携带主题、键、值，键在默认分区策略(哈希取模)中的作用，以及如何实现自定义分区器让业务规则决定消息落到哪个分区。适合需要精细控制消息分布(如按客户重要性分区)的场景。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
