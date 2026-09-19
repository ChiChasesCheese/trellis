%% trellis:begin %%
# Datastream（兼容 Kafka 协议的摄取）
*数据加载与摄取*

一个原生流式服务，直接用 Kafka 线上协议（wire protocol）向表中写入数据，并继承 RBAC、血缘（lineage）与时间旅行（Time Travel）能力。

**Requires:** [[domains/snowflake/map/ingestion.snowpipe-streaming-offset-tokens|Snowpipe Streaming 与偏移量令牌（offset token）]]

## Cards (5)
1. [[datastream-inherits-governance]]
2. [[datastream-maturity-status]]
3. [[datastream-vs-connector-plus-streaming]]
4. [[datastream-when-not-to-choose]]
5. [[datastream-wire-protocol-not-kafka]]
%% trellis:end %%

## Notes
