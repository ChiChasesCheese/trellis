---
id: kafka-admin-alterconfigop-types
node: admin.dynamic-config
type: cloze
source: kafka-2e
---
用 AdminClient 的 incrementalAlterConfigs 修改配置时，每个修改操作都要指定一个操作类型（AlterConfigOp.OpType），Kafka 支持四种：{{c1::SET（设置一个新值）}}、{{c2::DELETE（删除该配置值，重置为默认值）}}、{{c3::APPEND（仅用于 List 类型配置，向列表追加值）}}、{{c4::SUBTRACT（仅用于 List 类型配置，从列表移除值）}}；APPEND 和 SUBTRACT 的意义在于不用每次都把整个列表重新发送给 Kafka。
