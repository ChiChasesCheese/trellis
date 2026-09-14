---
id: async-delivery-semantics-cloze
node: async.delivery.guarantees
type: cloze
---
Delivery semantics follow from when you ack: acking **before** processing gives {{c1::at-most-once}} (crash loses the message), acking **after** processing gives {{c2::at-least-once}} (crash causes redelivery), and "exactly-once" in practice means {{c3::at-least-once delivery plus idempotent (deduplicating) processing}}.

## zh
投递语义取决于何时 ack：处理**之前** ack 会给出 {{c1::at-most-once}}（崩溃会丢失消息），处理**之后** ack 会给出 {{c2::at-least-once}}（崩溃会导致重投递），实践中"exactly-once"意味着 {{c3::at-least-once 投递加幂等（去重）处理}}。
