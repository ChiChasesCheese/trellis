---
nodes:
- reliability.producer-reliable
title: 在可靠的系统中使用生产者
corpus: kafka-2e
section: 073-7-4
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 在可靠的系统中使用生产者

本节讲解为保证可靠传递需要设置的生产者确认(acks)与重试参数，以及需要额外处理的错误场景(如不可重试的错误)。是把broker端的可靠性配置落实到生产者代码里的关键一步。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
