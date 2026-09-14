---
id: storage-keyvalue-fit
node: storage.nosql
type: qa
---
## Q
A pure key-value store (DynamoDB used as KV, Redis, Riak-style) is the simplest NoSQL family. What access pattern justifies choosing it as the system of record, and what capabilities do you knowingly give up?

## A
Choose it when **every access is by primary key** and the value is opaque to the store: sessions, shopping carts, user preferences, device state, feature flags. That contract is what makes it easy to run at scale — keys hash across partitions with no hot coordination, giving predictable single-digit-ms lookups almost regardless of dataset size.

You give up, by design:

- **Secondary access paths** — "find all carts containing item X" needs a separate index you build and keep in sync yourself.
- **Cross-key operations** — no joins, and usually no multi-key transactions; consistency across two keys is your application's problem.
- **Rich queries** — no ad-hoc filtering/aggregation; analytics means exporting the data elsewhere.

The failure smell: if you catch yourself scanning all keys or encoding query logic into key names, the access pattern has outgrown the model.

## Q zh
纯 key-value 存储（当 KV 用的 DynamoDB、Redis、Riak 风格）是最简单的 NoSQL 家族。什么访问模式能证明选它做系统记录源（system of record）是对的，你又主动放弃了哪些能力？

## A zh
当**每次访问都通过主键**、且 value 对存储引擎不透明时选它：会话、购物车、用户偏好、设备状态、feature flag。正是这个契约让它容易大规模运行 — key 哈希分布到各分区，没有热点协调，无论数据集多大都能给出可预测的个位数毫秒查找。

你有意放弃的：

- **二级访问路径** — "找出所有包含商品 X 的购物车"需要你自己构建并维护同步的独立索引。
- **跨 key 操作** — 没有 join，通常也没有多 key 事务；两个 key 之间的一致性是你应用层的问题。
- **丰富查询** — 没有临时过滤/聚合；做分析意味着把数据导出到别处。

选错的气味：如果你发现自己在扫描全部 key，或把查询逻辑编码进 key 的命名里，说明访问模式已经超出了这个模型。
