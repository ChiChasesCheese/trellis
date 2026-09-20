---
id: problems-message-queue-pull-based-consumer-model
node: problems.foundations.message-queue
type: qa
step: 2
tags: [grown]
---
## Q
In a Kafka-class message queue, why do consumers pull records from brokers (via long-polling fetch requests) rather than brokers pushing records to consumers, and what does this design choice give the system for free?

## A
A push-based broker has to guess each consumer's processing capacity and either overwhelm a slow consumer or under-utilize a fast one, requiring a separate flow-control protocol layered on top. With a pull model, each consumer requests data at whatever rate it can actually process, so backpressure is inherent in the protocol itself rather than a bolted-on feature -- a slow consumer simply polls less often or requests smaller batches, and the broker never needs to track per-consumer send rates or implement throttling logic of its own.

## Q zh
在一个 Kafka 一类的消息队列里，为什么消费者是主动向 broker 拉取（pull，通过长轮询的 fetch 请求）记录，而不是 broker 主动推送给消费者？这个设计选择白白带来了什么好处？

## A zh
推送模型下 broker 必须猜测每个消费者的处理能力，结果要么压垮慢消费者，要么浪费快消费者的能力，还需要在协议之上再叠加一层独立的流控机制。而在拉取模型下，每个消费者按自己实际能处理的速率主动发起请求，背压天然内建在协议本身里，不是额外加装的功能——慢消费者只需要更少地轮询或请求更小的批次，broker 完全不需要为每个消费者维护发送速率或实现自己的限流逻辑。
