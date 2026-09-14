---
id: mcw-maximized-vs-autoscale
node: warehouse.multi-cluster-scaling-policy
type: qa
source: snowflake-docs
---
## Q
多集群仓库（multi-cluster warehouse）的 Maximized 与 Auto-scale 两种模式如何通过 MIN/MAX 集群数区分？伸缩策略（scaling policy）对哪种模式有效？各自适合什么负载？

## A
Maximized：最小集群数 = 最大集群数（且 >1），仓库启动时就拉起全部集群，适合并发用户/查询量大且波动不大的负载，静态控制容量。Auto-scale：最大集群数 > 最小集群数，Snowflake 在查询因资源不足开始排队时自动加集群、负载下降时自动减集群，适合并发量波动的负载。伸缩策略只对 Auto-scale 生效，因为 Maximized 模式下所有集群始终同时运行，没有启停决策可做。
