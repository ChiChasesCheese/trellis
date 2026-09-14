---
id: queuing-three-remedies
node: warehouse.query-queuing
type: qa
source: snowflake-docs
---
## Q
一个虚拟仓库（virtual warehouse）上查询排队（queuing）超出预期，有哪三种缓解手段？各自的局限是什么？

## A
① 另建一个仓库，把部分查询手动改到新仓库——有效但需要人工分流和事后收缩。② 调大仓库规格——能在一定程度上缓解并发排队，但调整规格主要用于提升单条查询性能，不是为并发设计的。③ 使用多集群仓库（multi-cluster warehouse）——效果基本等同于自动地增加仓库并分流查询，无需人工干预，是 Snowflake 推荐的全自动并发扩展方式，但需要 Enterprise 版及以上。
