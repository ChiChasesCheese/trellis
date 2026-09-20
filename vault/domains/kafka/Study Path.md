%% trellis:begin %%
# Kafka — study path

## Core

*14 of 66 topics: the declared Core and what it requires. Anki deals these first.*

**核心架构：主题、分区与副本模型**
- [ ] [[core.pubsub-why|发布/订阅模型与Kafka的定位（为何选择Kafka）]] — 6 cards
- [ ] [[core.topics-partitions|主题（topic）、分区（partition）与数据模型]] — 5 cards
- [ ] [[core.offsets|偏移量（offset）：仅追加日志中的位置]] — 5 cards
- [ ] [[core.replication-isr|副本、首领/追随者与同步副本集合（ISR）]] — 5 cards
- [ ] [[core.cluster-roles|broker、集群与多集群架构中的角色分工]] — 5 cards
**生产者：向Kafka写入数据**
- [ ] [[producer.acks-durability|acks与生产端持久性保证]] — 5 cards; needs: 副本、首领/追随者与同步副本集合（ISR）
- [ ] [[producer.batching-throughput|批处理、linger.ms与压缩（compression）对吞吐量的影响]] — 5 cards
- [ ] [[producer.idempotence-ordering|幂等生产者开关（enable.idempotence）与顺序保证]] — 5 cards
**消费者：从Kafka读取数据**
- [ ] [[consumer.groups-rebalance|消费者群组（consumer group）与再均衡（rebalance）]] — 6 cards
- [ ] [[consumer.offset-commit|提交与偏移量管理]] — 6 cards; needs: 偏移量（offset）：仅追加日志中的位置
**集群内部机制：控制器、复制协议与存储**
- [ ] [[internals.compaction|日志压实（log compaction）]] — 6 cards
**可靠的数据传递**
- [ ] [[reliability.guarantees|Kafka的可靠性保证及其边界]] — 5 cards
**精确一次语义（exactly-once semantics）**
- [ ] [[eos.transactions|事务：应用场景、隔离与实现原理]] — 6 cards
**监控Kafka**
- [ ] [[monitoring.lag-e2e|消费滞后监控与端到端监控]] — 6 cards
## The rest

**生产者：向Kafka写入数据**
- [ ] [[producer.client-basics|创建生产者与同步/异步发送]] — 5 cards
- [ ] [[producer.timeouts-retries|消息传递超时与重试（max.in.flight.requests.per.connection）]] — 5 cards
- [ ] [[producer.serialization|序列化器与使用Avro序列化数据]] — 5 cards
- [ ] [[producer.extensibility|分区策略、消息标头（headers）与拦截器]] — 5 cards
- [ ] [[producer.schema-registry|Schema Registry实践：模式演进与兼容性]] — 0 cards
**消费者：从Kafka读取数据**
- [ ] [[consumer.client-basics|创建消费者、订阅与轮询循环]] — 5 cards
- [ ] [[consumer.poll-config|拉取与存活相关配置]] — 6 cards
- [ ] [[consumer.seek-and-replay|定位读取位置：seek、按时间戳查找与重放（replay）]] — 4 cards; needs: 提交与偏移量管理
- [ ] [[consumer.deserialization|反序列化器与Avro反序列化]] — 4 cards
- [ ] [[consumer.standalone|独立消费者：脱离消费者群组的场景]] — 4 cards
- [ ] [[consumer.kafka4-protocol-changes|新一代消费者协议：增量再均衡（KIP-848）与共享群组（KIP-932）]] — 0 cards
**集群内部机制：控制器、复制协议与存储**
- [ ] [[internals.controller|控制器（controller）的角色与选举]] — 5 cards; needs: broker、集群与多集群架构中的角色分工
- [ ] [[internals.replication-protocol|复制协议：首领/追随者同步与副本滞后]] — 5 cards; needs: 副本、首领/追随者与同步副本集合（ISR）
- [ ] [[internals.request-handling|broker如何处理生产请求与获取请求]] — 6 cards
- [ ] [[internals.storage-segments|物理存储：分区分配与日志片段（log segment）]] — 6 cards
- [ ] [[internals.indexes|索引：偏移量索引与时间索引]] — 4 cards
- [ ] [[internals.kraft-mode|KRaft模式与ZooKeeper的移除]] — 5 cards
- [ ] [[internals.tiered-storage|分层存储（tiered storage, KIP-405）]] — 5 cards
**可靠的数据传递**
- [ ] [[reliability.broker-config|broker层可靠性配置]] — 6 cards; needs: 副本、首领/追随者与同步副本集合（ISR）
- [ ] [[reliability.producer-reliable|在可靠系统中配置生产者]] — 6 cards; needs: acks与生产端持久性保证
- [ ] [[reliability.consumer-reliable|在可靠系统中配置消费者]] — 6 cards; needs: 提交与偏移量管理
- [ ] [[reliability.validation|验证系统可靠性]] — 6 cards
**精确一次语义（exactly-once semantics）**
- [ ] [[eos.idempotent-producer|幂等生产者的工作原理与局限性]] — 6 cards; needs: 幂等生产者开关（enable.idempotence）与顺序保证
- [ ] [[eos.transactions-perf|事务的性能开销]] — 4 cards
**数据管道与Kafka Connect**
- [ ] [[connect.pipeline-design|构建数据管道的设计考量]] — 6 cards
- [ ] [[connect.connect-basics|Kafka Connect：适用场景与架构]] — 6 cards
- [ ] [[connect.smt|单一消息转换（SMT）与Connect内部机制]] — 6 cards
- [ ] [[connect.alternatives|Connect之外的数据集成选择]] — 4 cards
**跨集群数据镜像**
- [ ] [[mirroring.architectures|跨集群镜像的应用场景与多集群架构]] — 6 cards
- [ ] [[mirroring.mirrormaker|MirrorMaker：配置、拓扑与调优]] — 6 cards; needs: Kafka Connect：适用场景与架构
- [ ] [[mirroring.alternatives|其他跨集群镜像方案]] — 6 cards
**保护Kafka**
- [ ] [[security.protocols-auth-encryption|安全协议、身份验证（SSL/SASL）与加密]] — 7 cards
- [ ] [[security.authorization|授权：ACL与自定义授权]] — 6 cards
- [ ] [[security.audit-hardening|审计与平台整体加固]] — 6 cards
**管理与运维工具**
- [ ] [[admin.topic-ops|主题运维：AdminClient与命令行工具]] — 6 cards
- [ ] [[admin.consumer-group-ops|消费者群组管理与偏移量运维]] — 6 cards; needs: 消费者群组（consumer group）与再均衡（rebalance）
- [ ] [[admin.dynamic-config|动态配置变更]] — 6 cards
- [ ] [[admin.partition-reassignment|分区管理与应急操作]] — 6 cards
**监控Kafka**
- [ ] [[monitoring.metrics-and-slo|指标基础与服务级别目标（SLO）]] — 6 cards
- [ ] [[monitoring.broker-metrics|broker指标与集群问题诊断]] — 6 cards
- [ ] [[monitoring.client-metrics|客户端监控：生产者、消费者指标与配额]] — 6 cards
- [ ] [[monitoring.observability-otel|用OpenTelemetry构建现代可观测性]] — 0 cards
**流式处理（Kafka Streams）**
- [ ] [[streams.concepts|流式处理核心概念]] — 6 cards; needs: 主题（topic）、分区（partition）与数据模型
- [ ] [[streams.design-patterns|流式处理设计模式]] — 6 cards
- [ ] [[streams.streams-api|Kafka Streams API与拓扑构建]] — 6 cards
- [ ] [[streams.streams-architecture|Kafka Streams架构]] — 6 cards
- [ ] [[streams.choosing-framework|流式处理的应用场景与框架选型]] — 6 cards
**生产实践：容量、部署与生态定位**
- [ ] [[practice.sizing-tuning|容量规划与生产环境调优]] — 6 cards
- [ ] [[practice.cloud-deployment|在云端运行Kafka]] — 5 cards
- [ ] [[practice.other-clients|非JVM语言客户端生态]] — 4 cards
- [ ] [[practice.positioning|Kafka与Pulsar/RabbitMQ/Redpanda等的定位取舍]] — 0 cards
- [ ] [[practice.kubernetes-strimzi|在Kubernetes上运行Kafka（Strimzi）]] — 5 cards
%% trellis:end %%

## Notes
