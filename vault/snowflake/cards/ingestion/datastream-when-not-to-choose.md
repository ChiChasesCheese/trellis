---
id: datastream-when-not-to-choose
node: ingestion.datastream-kafka-compatible
type: qa
tags: [grown]
---
## Q
一家公司的 Kafka 除了向 Snowflake 供数，还承载着大量微服务之间的事件通信。这种情况下直接用 Datastream 替换 Kafka 需要考虑什么？

## A
Datastream 的定位是面向「数据最终要进入 Snowflake」的场景，用来替换以入仓为主要目的的 Kafka 基础设施。如果 Kafka 同时是服务间通信的事件总线，全部迁移意味着把在线系统的消息链路也依赖到数据平台上，需要评估延迟、可用性和其他 Kafka 生态特性的兼容程度；更稳妥的做法往往是只把入仓链路切到 Datastream，或继续用连接器从现有 Kafka 导入。
