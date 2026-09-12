---
nodes:
- internals.controller
title: 集群的成员关系：broker如何注册与被发现
corpus: kafka-2e
section: 063-6-1
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 集群的成员关系：broker如何注册与被发现

本节讲解Kafka如何借助ZooKeeper临时节点维护broker的成员信息——broker启动时注册自己的ID，断开连接时节点自动消失并通知其他组件。这是理解控制器如何感知broker加入/退出集群的前置知识。
