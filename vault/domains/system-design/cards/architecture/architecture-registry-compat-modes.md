---
id: architecture-registry-compat-modes
node: architecture.discovery
type: cloze
---
A schema registry's compatibility mode dictates **deploy order**: BACKWARD (new schema can read old data) means upgrade {{c1::consumers first}}, then producers; FORWARD (old schema can read new data) means upgrade {{c2::producers first}}; FULL allows {{c3::either order}}. Kafka-style event streams default to BACKWARD because consumers must be able to reprocess {{c4::old events retained in the log}} — the registry rejects an incompatible schema at publish/CI time, before it can strand data. See [[architecture-schema-compat-rules]].

## zh
一个 schema 注册表的兼容模式决定**部署顺序**：BACKWARD（新 schema 可以读旧数据）意味着升级 {{c1::consumers first}}，然后生产者；FORWARD（旧 schema 可以读新数据）意味着升级 {{c2::producers first}}；FULL 允许 {{c3::either order}}。Kafka 风格事件流默认 BACKWARD 因为消费者必须能够重处理 {{c4::old events retained in the log}} ——注册表在发布/CI 时拒绝不兼容的 schema，在它可以搁浅数据之前。见 [[architecture-schema-compat-rules]]。
