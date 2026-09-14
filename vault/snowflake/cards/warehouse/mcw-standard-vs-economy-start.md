---
id: mcw-standard-vs-economy-start
node: warehouse.multi-cluster-scaling-policy
type: qa
source: snowflake-docs
---
## Q
多集群仓库（multi-cluster warehouse）在 Auto-scale 模式下，Standard 与 Economy 两种伸缩策略（scaling policy）分别在什么条件下启动新集群？各自偏向什么？

## A
Standard（默认）偏向避免排队：只要有查询排队，或 Snowflake 估计当前运行的集群已无余力接新查询，就增加集群——最大集群数 ≤10 时一次加一个，>10 时可一次启动多个以应对负载陡增。Economy 偏向省 credit（信用点）：只有估计新增负载足以让一个新集群至少忙 6 分钟时才启动，宁可让现有集群满载，代价是查询可能排队、完成更慢。
