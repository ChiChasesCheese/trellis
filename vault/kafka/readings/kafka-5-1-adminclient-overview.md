---
nodes:
- admin.topic-ops
title: AdminClient概览：异步且最终一致的管理API
corpus: kafka-2e
section: 053-5-1-adminclient
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# AdminClient概览：异步且最终一致的管理API

本节介绍AdminClient的设计原则——它是异步的，每个方法调用会立即返回一个Future，操作结果具有最终一致性；还讲解了它扁平的方法结构和配置参数。理解这些设计原则，是正确使用AdminClient编程式管理主题、避免误判操作是否已生效的前提。
