---
id: hi-c-sd-data-modeling-n04-kv
node: sd.core-concepts.data-modeling.notes
type: qa
step: 4
---
## Q
**数据建模 · 键值存储**｜摘要 · 必会
键值存储适合什么，为什么说"相对 SQL"这个说法有误导？它让数据模型变成什么样？

## A
- **能力：** 按精确的键取值，极快，但除此之外几乎没有查询能力。
- **适用：** 缓存、会话存储、功能开关，以及只需按单一标识查询、写入量极高的场景。
- **常见搭配而非二选一：** 实际上多是 SQL 做事实来源（source of truth），前面放 Redis 之类的键值缓存存热数据，既快又不放弃持久性和复杂查询。
- **对模型的影响：** 模型很扁平，为支持不同访问方式会在多个键下重复存同一份数据，因为无法联接或跨关系查询。读很快，但数据变化时一致性很难维持。例：Redis、DynamoDB、Memcached。
- **2026 亮点：** 说 Redis 时顺带说 Valkey：Redis 2024 年改为源码可用许可，Linux Foundation 下的 Valkey 分叉协议兼容，应用代码基本不用改；托管服务（如 ElastiCache）两者都提供，Valkey 更便宜。选型看许可证合规、云厂商支持和需要的功能。
