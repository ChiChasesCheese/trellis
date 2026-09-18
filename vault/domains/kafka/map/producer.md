%% trellis:begin %%
# 生产者：向Kafka写入数据

掌握生产者的发送模型、关键配置权衡（确认、批处理、超时重试、幂等性）与可扩展点。

## Topics
- [[domains/kafka/map/producer.client-basics|创建生产者与同步/异步发送]]
- [[domains/kafka/map/producer.acks-durability|acks与生产端持久性保证]]
- [[domains/kafka/map/producer.batching-throughput|批处理、linger.ms与压缩（compression）对吞吐量的影响]]
- [[domains/kafka/map/producer.timeouts-retries|消息传递超时与重试（max.in.flight.requests.per.connection）]]
- [[domains/kafka/map/producer.idempotence-ordering|幂等生产者开关（enable.idempotence）与顺序保证]]
- [[domains/kafka/map/producer.serialization|序列化器与使用Avro序列化数据]]
- [[domains/kafka/map/producer.extensibility|分区策略、消息标头（headers）与拦截器]]
- [[domains/kafka/map/producer.schema-registry|Schema Registry实践：模式演进与兼容性]]
%% trellis:end %%

## Notes
