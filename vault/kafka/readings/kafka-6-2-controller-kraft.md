---
nodes:
- internals.controller
- internals.kraft-mode
title: 控制器的选举与职责，以及KRaft带来的变革
corpus: kafka-2e
section: 064-6-2
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 控制器的选举与职责，以及KRaft带来的变革

本节详细讲解控制器如何通过ZooKeeper临时节点选举产生、如何用epoch机制防止僵尸控制器和脑裂、控制器在broker加入退出时如何驱动首领选举与元数据分发。同时介绍Kafka 3.3+/4.0引入的基于Raft的KRaft控制器如何取代ZooKeeper，用日志化的元数据事件流替代原有架构，从根本上改变了元数据管理与选举方式。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.ituring.com.cn/book/2937)
%% trellis:end %%
