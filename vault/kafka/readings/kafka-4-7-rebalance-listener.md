---
nodes:
- consumer.groups-rebalance
title: 再均衡监听器
corpus: kafka-2e
section: 046-4-7
url: https://www.ituring.com.cn/book/2937
tags:
- book
---

# 再均衡监听器

本节讲解ConsumerRebalanceListener接口如何让消费者在即将失去分区所有权前完成收尾工作(如提交偏移量、关闭资源)，以及在获得新分区时执行初始化逻辑。是将再均衡这一群组级事件与应用层清理逻辑结合起来的关键机制。
