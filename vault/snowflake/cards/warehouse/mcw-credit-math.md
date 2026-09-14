---
id: mcw-credit-math
node: warehouse.multi-cluster-scaling-policy
type: qa
source: snowflake-docs
---
## Q
一个 Medium（每集群每小时 4 credit）多集群仓库（multi-cluster warehouse），最大 3 个集群，运行 2 小时。Maximized 模式与 Auto-scale 模式（集群 1 全程、集群 2 仅第 2 小时、集群 3 在第 2 小时跑 30 分钟）各花多少 credit？

## A
每小时最高费用 = 规格费率 × 最大集群数 = 4 × 3 = 12 credit。Maximized 两小时 3 个集群全开：24 credit。Auto-scale：第 1 小时只有集群 1，4 credit；第 2 小时 4 + 4 + 2 = 10 credit；合计 14 credit。实际费用取决于每小时内实际运行的集群数（按秒计费）；若中途调整规格，新规格会同时作用于所有正在运行和之后启动的集群。
