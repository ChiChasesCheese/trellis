---
id: kafka-internals-delete-and-compact-combo
node: internals.compaction
type: qa
step: 6
source: kafka-2e
---
## Q
如果既想「只保留每个键的最新值」，又想「超过一定时间的数据无论新旧都必须被删除」（比如出于合规要求），单独用 `compact` 策略够吗？Kafka 提供了什么组合方案？

## A
单独用 `compact` 不够：它只保证同一个键只留一条最新记录，但不会因为时间到了就把这条最新记录删掉，所以压实主题理论上可以无限增长（只要键不断变化）。Kafka 提供了 `delete.and.compact` 组合策略：一方面像 `compact` 一样为每个键只保留最新值，另一方面像 `delete` 一样把超过保留时间的消息删除——即使这条消息的键对应的值仍然是「最新的」。这样既控制了压实主题的总体大小，也满足了「数据存在时间不能超过某个上限」的业务/合规要求。
