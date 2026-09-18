%% trellis:begin %%
# 消费者：从Kafka读取数据

掌握消费者群组协作模型、拉取与提交语义，以及新一代消费者协议的演进方向。

## Topics
- [[domains/kafka/map/consumer.groups-rebalance|消费者群组（consumer group）与再均衡（rebalance）]]
- [[domains/kafka/map/consumer.client-basics|创建消费者、订阅与轮询循环]]
- [[domains/kafka/map/consumer.poll-config|拉取与存活相关配置]]
- [[domains/kafka/map/consumer.offset-commit|提交与偏移量管理]]
- [[domains/kafka/map/consumer.seek-and-replay|定位读取位置：seek、按时间戳查找与重放（replay）]]
- [[domains/kafka/map/consumer.deserialization|反序列化器与Avro反序列化]]
- [[domains/kafka/map/consumer.standalone|独立消费者：脱离消费者群组的场景]]
- [[domains/kafka/map/consumer.kafka4-protocol-changes|新一代消费者协议：增量再均衡（KIP-848）与共享群组（KIP-932）]]
%% trellis:end %%

## Notes
