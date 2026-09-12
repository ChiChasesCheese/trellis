---
nodes:
- eos.transactions-perf
title: 事务的性能开销
corpus: kafka-2e
section: 080-8-3
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 事务的性能开销

本节分析启用事务后引入的额外开销：事务ID注册、分区加入事务的注册、提交请求与提交标记写入都会增加延迟，事务初始化和提交都是同步操作。是在采用精确一次语义前权衡性能代价的必读内容。
