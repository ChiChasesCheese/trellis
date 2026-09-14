---
nodes:
- internals.request-handling
title: broker如何处理请求
corpus: kafka-2e
section: 066-6-4
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# broker如何处理请求

本节讲解broker内部处理生产请求和获取请求的路径，包括网络线程与IO线程如何协作、请求队列如何组织，以及其他类型请求的处理方式。是诊断性能瓶颈、理解broker内部并发模型的基础。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
