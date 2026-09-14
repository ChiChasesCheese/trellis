---
id: scale-out-min-clusters-for-ha
node: warehouse.scaling-up-vs-out
type: qa
source: snowflake-docs
---
## Q
配置多集群仓库（multi-cluster warehouse）时，最小集群数什么时候保留默认的 1，什么时候应该设得大于 1？

## A
默认保留 1：这样额外集群只在需要时才启动，不为闲置容量付费。若非常在意仓库的高可用，就设为大于 1：万一某个集群发生故障（虽然少见），仍有其他集群在运行，保证仓库的可用性和连续性。代价是这些常驻集群在低负载时也持续消耗 credit（信用点）。
