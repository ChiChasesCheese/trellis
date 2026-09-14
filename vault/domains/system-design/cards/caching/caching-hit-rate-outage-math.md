---
id: caching-hit-rate-outage-math
node: caching.placement
type: cloze
---
Second-order dependency math: at a 99% hit rate, losing the cache multiplies database read load by {{c1::100× (1 ÷ miss rate)}} — so either the DB is provisioned for full miss-storm traffic (almost never) or the cache is a **hard dependency** that needs {{c2::HA (replication/failover) plus warmed, gradual recovery — never a cold restart into live traffic}}. The trap: every hit-rate improvement quietly shrinks DB headroom, until a "cache" the database cannot survive without is really {{c3::a serving tier, not an optimization}}.

## zh
二阶依赖数学：在 99% 命中率下，丢失缓存将数据库读负载乘以 {{c1::100× (1 ÷ miss rate)}} — 所以要么 DB 为完整的 miss 风暴流量配置（几乎从不），要么缓存是一个 **硬依赖** 需要 {{c2::HA（复制/故障转移）加上预热、渐进式恢复 — 绝不能冷启动直接迎接实时流量}}。陷阱：每个命中率改进悄悄地缩小 DB 余量，直到数据库无法生存的"缓存"真的是 {{c3::一个服务层，而不是一个优化}}。
