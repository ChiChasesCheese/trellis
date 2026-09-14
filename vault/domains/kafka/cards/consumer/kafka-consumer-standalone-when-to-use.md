---
id: kafka-consumer-standalone-when-to-use
node: consumer.standalone
type: qa
source: kafka-2e
---
## Q
什么情况下适合让一个消费者不加入任何消费者群组、以「独立消费者」（standalone consumer）的方式直接读取某个主题的全部或部分分区，而不是走消费者群组和再均衡那一套机制？

## A
当只需要用单独一个消费者读取某个主题的全部分区、或者读取某几个已经明确知道的固定分区时，就不需要消费者群组自动分配分区、自动再均衡这些机制带来的复杂性——只要把这些分区直接分配给这个消费者，让它开始读取消息并适时提交偏移量即可，做法更简单直接。
