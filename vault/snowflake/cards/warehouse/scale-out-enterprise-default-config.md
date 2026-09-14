---
id: scale-out-enterprise-default-config
node: warehouse.scaling-up-vs-out
type: qa
source: snowflake-docs
---
## Q
在 Snowflake Enterprise 版（及以上）账户里，仓库的“横向扩展”默认该怎么配置？Maximized 模式什么时候才用？

## A
所有仓库都应配置为多集群仓库（multi-cluster warehouse），并运行在 Auto-scale 模式，让 Snowflake 按需自动启停集群；这样平时只跑最少集群，并发上来时自动扩出。只有在确有特定需求时才用 Maximized 模式（最小 = 最大集群数，启动即拉起全部集群），例如并发量大且稳定、需要静态固定容量的场景。
