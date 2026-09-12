---
id: kafka-consumer-one-thread-per-consumer-rule
node: consumer.client-basics
type: qa
source: kafka-2e
---
## Q
能不能在同一个线程里跑多个属于同一个消费者群组的 KafkaConsumer？能不能让多个线程共享同一个 KafkaConsumer 实例？

## A
都不行。Kafka 消费者的使用规则是「一个消费者对应一个线程」：既不能在同一线程里同时运行多个属于同一群组的消费者，也不能保证多个线程安全地共享同一个消费者对象去并发调用它的方法。如果应用要在同一个消费者群组里跑多个消费者做并行处理，正确做法是把每个消费者的逻辑封装起来，各自独立运行在自己的线程中（比如用 ExecutorService 启动多个线程）。
