---
id: kafka-producer-idempotence-config-cloze
node: producer.idempotence-ordering
type: cloze
source: kafka-2e
---
开启幂等生产者（`enable.idempotence=true`）要求同时满足三个条件：{{c1::max.in.flight.requests.per.connection ≤ 5}}、{{c2::retries > 0}}、{{c3::acks = all}}，否则 Kafka 会抛出 ConfigException（配置不合法异常）拒绝启动。
