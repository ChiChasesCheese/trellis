%% trellis:begin %%
# 消息队列
*B 其余知识点*

Kafka 为主，RabbitMQ / RocketMQ 对照：可靠性、顺序、积压、重试、延迟消息。

## Topics
- [[domains/bagu/map/b.mq.kafka-throughput|Kafka 为什么吞吐这么高（顺序写、零拷贝、批量、压缩）]]
- [[domains/bagu/map/b.mq.partition-count|分区数怎么确定（Partition Count）]]
- [[domains/bagu/map/b.mq.no-duplicate|重复消费与恰好一次（Exactly Once）]]
- [[domains/bagu/map/b.mq.rebalance|消费者组重平衡（Rebalance）为什么卡、怎么避免]]
- [[domains/bagu/map/b.mq.dlq-retry|死信队列与重试设计（Dead Letter Queue）]]
- [[domains/bagu/map/b.mq.delay-message|延迟消息怎么实现（Delayed Message）]]
- [[domains/bagu/map/b.mq.selection|Kafka、RabbitMQ、RocketMQ 怎么选（含 RocketMQ 架构）]]
- [[domains/bagu/map/b.mq.why-mq|为什么用消息队列：削峰、解耦、异步与代价（Why MQ）]]
- [[domains/bagu/map/b.mq.rabbitmq|RabbitMQ 模型与可靠性（Exchange, Confirm, Ack）]]
%% trellis:end %%

## Notes
